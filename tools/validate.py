"""Contrôle statique du périmètre public; exécutable hors réseau."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import csv
ROOT=Path(__file__).resolve().parents[1]
PAGES=["index.html","marches-prestataires.html","demarches.html","sources.html","charte-editoriale.html","privacy.html","affiche-qr-observatoire.html","audit-technique-sites.html","audit-technique-capevol.html","audit-technique-pollen.html","audit-technique-creagestion.html","audit-technique-ambitions.html","audit-technique-departement.html"]
BASE="https://muse-irs.github.io/ardeche-rsa-insertion-parcours-observatoire-public/"
class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        for prop in ("href","src"):
            if prop in a:
                self.links.append(a[prop])
for path in PAGES:
    data=(ROOT/path).read_text(encoding="utf-8")
    assert '<html lang="fr">' in data,path
    assert "no-referrer" in data,path
    assert all(s not in data for s in ("googletagmanager.com","google-analytics.com","facebook.net/en_US/fbevents.js")),path
    parser=Parser();parser.feed(data)
    for link in parser.links:
        split=urlsplit(link)
        if split.scheme or split.netloc or not split.path:continue
        if split.path in (".","./"):relative=ROOT/"index.html"
        else:relative=(ROOT/split.path).resolve()
        assert relative.is_relative_to(ROOT.resolve()),(path,link)
        assert relative.exists(),(path,link)
assert BASE in (ROOT/"affiche-qr-observatoire.html").read_text(encoding="utf-8")
svg=(ROOT/"assets/qr-observatoire.svg").read_text(encoding="utf-8")
assert BASE in svg and "<path" in svg and "<script" not in svg
assert (ROOT/"assets/affiche-qr-observatoire-a4.pdf").read_bytes().startswith(b"%PDF-")
with (ROOT/"data/sources.csv").open(encoding="utf-8",newline="") as f: sources=list(csv.DictReader(f))
with (ROOT/"data/claims.csv").open(encoding="utf-8",newline="") as f: claims=list(csv.DictReader(f))
ids={s["source_id"] for s in sources}
assert len(sources)>=8 and len(ids)==len(sources)
assert all(set(c["source_ids"].split(";")).issubset(ids) for c in claims)
assert "dossier individuel" in (ROOT/"privacy.html").read_text(encoding="utf-8") or "dossier personnel" in (ROOT/"privacy.html").read_text(encoding="utf-8")
print(f"OK — {len(PAGES)} pages, {len(sources)} sources, {len(claims)} affirmations et affiche QR A4")

# QR téléchargeable : compatibilité mobile et relation croisée entre observatoires
qr_page=(ROOT/"affiche-qr-observatoire.html").read_text(encoding="utf-8")
assert 'assets/qr-observatoire.png' in qr_page
assert 'download="observatoire-rsa-ardeche-qr-a4.pdf"' in qr_page
assert 'target="_blank"' in qr_page
assert 'ardeche-habitat-sc-amplitudes-observatoire-public/' in qr_page
assert "autre observatoire" not in qr_page.lower()
png=(ROOT/"assets/qr-observatoire.png").read_bytes()
assert png.startswith(b"\x89PNG\r\n\x1a\n") and len(png)>1000
assert "ardeche-habitat-sc-amplitudes-observatoire-public/" in (ROOT/"index.html").read_text(encoding="utf-8")

# Audit pages: no personal case facts, no active probe or external application scripts.
for audit in PAGES[7:]:
    text=(ROOT/audit).read_text(encoding="utf-8")
    assert "no-referrer" in text and "audit-technique-sites.html" in text,audit
    assert "<script" not in text,audit
    assert all(s not in text for s in ("catalogue_leads", "service_role", "boubekeurjeremy")),audit
assert all((ROOT/p).exists() for p in PAGES)

# Vérifier le rectificatif temporel apporté à la page Capévol.
cap=(ROOT/"audit-technique-capevol.html").read_text(encoding="utf-8")
assert "le 16 mai est la date éditoriale rapportée pour la politique actuelle" in cap
assert "aucune modification précise de ces documents après le 16 mai n'est démontrée" in cap
assert "Datation : quatre preuves distinctes" in cap

# Prépublication : périmètre départemental et attribution externe de la recherche.
cap = (ROOT/"audit-technique-capevol.html").read_text(encoding="utf-8")
assert "Apports de l'étude technique Perplexity" in cap
assert "Gemini" not in cap and "erreur de provenance" not in cap
assert "le 16 mai est la date éditoriale rapportée pour la politique actuelle" in cap
assert "aucune modification précise de ces documents après le 16 mai n'est démontrée" in cap
dep = (ROOT/"audit-technique-departement.html").read_text(encoding="utf-8")
assert "IONOS" in dep and "non réalisés par notre observatoire" in dep
assert "audit-technique-departement.html" in (ROOT/"audit-technique-sites.html").read_text(encoding="utf-8")
assert "audit-technique-departement.html" in (ROOT/"sitemap.xml").read_text(encoding="utf-8")
assert all("Gemini" not in (ROOT/p).read_text(encoding="utf-8") for p in PAGES)


# Contrôles complémentaires : couverture intégrale du sitemap, canoniques et minimisation.
import re
from xml.etree import ElementTree as ET

namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
sitemap_urls = {
    el.text for el in ET.parse(ROOT / "sitemap.xml").iter(namespace + "loc")
}
expected_urls = {BASE if p == "index.html" else BASE + p for p in PAGES}
assert sitemap_urls == expected_urls, (sitemap_urls ^ expected_urls)

# Un lien canonique unique doit correspondre à l'URL de chaque page servie.
for path in PAGES:
    html = (ROOT / path).read_text(encoding="utf-8")
    urls = re.findall(r'<link\s+rel="canonical"\s+href="([^"]+)"', html, re.I)
    expected = BASE if path == "index.html" else BASE + path
    assert urls == [expected], (path, urls, expected)

# Deux exports SVG, un seul contenu encodé : éviter une affiche pointant ailleurs.
svg_alt = (ROOT / "assets/qr-observatoire-rsa.svg").read_text(encoding="utf-8")
assert BASE in svg_alt and "<script" not in svg_alt
def qr_modules(markup):
    match = re.search(r'<path\b[^>]*\bd="([^"]+)"', markup)
    assert match
    return match.group(1)
assert qr_modules(svg) == qr_modules(svg_alt), "QR SVG incohérents"
assert (ROOT / "assets/affiche-qr-observatoire-rsa-a4.pdf").read_bytes().startswith(b"%PDF-")

# Éviter l'exposition nominale des référentiels privés dans les pages, CSV ou README.
public_text_paths = [ROOT / p for p in PAGES] + [ROOT / "README.md",
    ROOT / "data/sources.csv", ROOT / "data/claims.csv"]
private_markers = ("PGC-IA-Collaborative", "rsa-formation-data-evidence-control",
                   "boubekeurjeremy")
for path in public_text_paths:
    body = path.read_text(encoding="utf-8").lower()
    assert not any(marker.lower() in body for marker in private_markers), path
print("OK — sitemap/canoniques/QR cohérents ; références privées absentes des textes contrôlés")
