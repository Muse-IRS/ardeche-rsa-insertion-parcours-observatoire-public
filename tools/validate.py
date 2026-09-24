"""Contrôles hors réseau du dépôt public et de ses frontières."""
from pathlib import Path
from html.parser import HTMLParser
import csv
from urllib.parse import urlsplit
ROOT=Path(__file__).resolve().parents[1]
PAGES=["index.html","marches-prestataires.html","demarches.html","sources.html","charte-editoriale.html","privacy.html","affiche-qr-observatoire.html"]
BASE="https://muse-irs.github.io/ardeche-rsa-insertion-parcours-observatoire-public/"
class Parser(HTMLParser):
 def __init__(self): super().__init__(); self.links=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  for prop in ["href","src"]:
   if prop in a:self.links.append(a[prop])
for path in PAGES:
 text=(ROOT/path).read_text(encoding="utf-8")
 assert '<html lang="fr">' in text,path
 assert 'no-referrer' in text,path
 assert all(x not in text for x in ["googletagmanager.com","google-analytics.com","facebook.net/en_US/fbevents.js"]),path
 parser=Parser(); parser.feed(text)
 for link in parser.links:
  parsed=urlsplit(link)
  if not parsed.scheme and not parsed.netloc and parsed.path:
   relative=ROOT/parsed.path
   if parsed.path in ["./","."]: relative=ROOT/"index.html"
   assert relative.exists(),(path,link)
assert BASE in (ROOT/"affiche-qr-observatoire.html").read_text(encoding="utf-8")
assert BASE in (ROOT/"assets/qr-observatoire-rsa.svg").read_text(encoding="utf-8")
assert "ardeche-habitat" not in (ROOT/"affiche-qr-observatoire.html").read_text(encoding="utf-8")
assert (ROOT/"assets/affiche-qr-observatoire-rsa-a4.pdf").read_bytes().startswith(b"%PDF-")
with (ROOT/"data/sources.csv").open(encoding="utf-8",newline="") as f:
 refs=list(csv.DictReader(f))
with (ROOT/"data/claims.csv").open(encoding="utf-8",newline="") as f:
 claims=list(csv.DictReader(f))
ids={r["source_id"] for r in refs}
assert len(refs)>=8 and len(ids)==len(refs)
assert all(claim["source_id"] in ids for claim in claims)
print(f"OK — {len(PAGES)} pages, {len(refs)} sources, {len(claims)} affirmations, QR et PDF présents")
