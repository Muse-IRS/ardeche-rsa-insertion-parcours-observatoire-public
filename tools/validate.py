"""Contrôles reproductibles, sans réseau et sans collecte des visiteurs."""
from pathlib import Path
import csv, re
ROOT=Path(__file__).resolve().parents[1]
pages=["index.html","marches-prestataires.html","demarches.html","charte-editoriale.html","privacy.html","affiche-qr-observatoire.html"]
for p in pages:
    content=(ROOT/p).read_text(encoding="utf-8")
    assert '<html lang="fr">' in content, p
    assert 'no-referrer' in content, p
    assert "https://www.googletagmanager.com" not in content, p
    assert "google-analytics.com" not in content, p
home=(ROOT/"affiche-qr-observatoire.html").read_text(encoding="utf-8")
assert 'href="./"' in home
assert "href=\"assets/qr-observatoire-rsa.svg\"" in home
assert "ardeche-habitat" not in home
assert "ardeche-rsa-insertion-parcours-observatoire-public" in home
assert (ROOT/"assets/qr-observatoire-rsa.svg").exists()
with (ROOT/"data/sources.csv").open(encoding="utf-8") as f:
    assert len(list(csv.DictReader(f))) >= 5
print(f"OK — {len(pages)} pages, liens QR et registre public")
