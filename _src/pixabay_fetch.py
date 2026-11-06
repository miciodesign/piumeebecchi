"""Scarica foto da Pixabay (chiave in env PIXABAY_KEY) e le registra in photos.json."""
import json, os, sys, urllib.request, urllib.parse, pathlib
ROOT = pathlib.Path(__file__).parent
key = os.environ.get("PIXABAY_KEY")
if not key:
    sys.exit("PIXABAY_KEY mancante")
req = json.loads((ROOT/"pixabay.json").read_text(encoding="utf-8"))
photos = json.loads((ROOT/"photos.json").read_text(encoding="utf-8"))
out = ROOT/"src/assets/foto"; out.mkdir(parents=True, exist_ok=True)
for slug, r in req.items():
    if slug.startswith("_"): continue
    local = out/f"{slug}.jpg"
    if local.exists() and slug in photos: continue
    qs = {"key": key, "image_type": "photo", "safesearch": "true", "per_page": 5}
    if r.get("id"): qs["id"] = r["id"]
    else: qs["q"] = r["q"]; qs["orientation"] = "horizontal"; qs["min_width"] = 960
    data = json.load(urllib.request.urlopen("https://pixabay.com/api/?" + urllib.parse.urlencode(qs), timeout=30))
    if not data.get("hits"):
        print("nessun risultato:", slug); continue
    h = data["hits"][0]
    img = urllib.request.urlopen(urllib.request.Request(h["largeImageURL"], headers={"User-Agent": "piumeebecchi-build"}), timeout=60).read()
    local.write_bytes(img)
    photos[slug] = {"url": f"/assets/foto/{slug}.jpg", "page": h["pageURL"], "caption": r.get("caption") or f"Foto di {h['user']} da Pixabay"}
    print("ok:", slug, h["pageURL"])
(ROOT/"photos.json").write_text(json.dumps(photos, ensure_ascii=False, indent=1), encoding="utf-8")
