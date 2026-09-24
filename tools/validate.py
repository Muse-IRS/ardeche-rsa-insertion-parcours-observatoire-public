"""Contrôle statique du périmètre public; exécutable hors réseau."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import csv
ROOT=Path(__file__).resolve().parents[1]
PAGES=["index.html","marches-prestataires.html","demarches.html","sources.html","charte-editoriale.html","privacy.html","affiche-qr-observatoire.html"]
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
