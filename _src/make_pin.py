#!/usr/bin/env python3
"""Genera i Pin Pinterest (1000x1500) per gli articoli in content/ e aggiorna pin/PIN.md.
Uso: python3 make_pin.py   (crea solo i PNG mancanti; con --all li rigenera tutti)"""
import json, re, pathlib, html as H, subprocess, sys
ROOT = pathlib.Path(__file__).parent
V="#1f4d3a"; VS="#153627"; G="#f5c518"; A="#e07a2f"; W="#ffffff"; VC="#e4efe7"; CR="#fbf8f1"
CAT = {"ricerche-scuola":("ricerche","Ricerche per la scuola"),"giardino-balcone":("giardino","Uccelli in giardino e sul balcone"),
       "birdwatching-famiglie":("birdwatching","Birdwatching con i bambini"),"libri-giochi":("libri","Libri sugli uccelli per bambini"),
       "dove-vederli":("dove","Dove vedere gli uccelli in Italia"),"uccelli-in-casa":("casa","Canarini e cocorite")}
img = ROOT/"src/assets/img"; out = ROOT/"pin"; out.mkdir(exist_ok=True)
def inner(name):
    s = (img/f"{name}.svg").read_text().strip()
    return re.sub(r'^<svg[^>]*>', '', s).replace('</svg>','')
def wrap(text, maxc):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur)+len(w)+1 > maxc and cur: lines.append(cur); cur = w
        else: cur = (cur+" "+w).strip()
    if cur: lines.append(cur)
    return lines
rows, todo = [], []
for f in sorted((ROOT/"content").glob("*/*.html")):
    m = re.match(r"^---\s*(\{.*?\})\s*---", f.read_text(encoding="utf-8"), re.S); meta = json.loads(m.group(1))
    cat = f.parent.name; ill, board = CAT[cat]; slug = f.stem
    url = f"https://www.piumeebecchi.it/{cat}/{slug}/"
    rows.append((board, meta["title"], meta["description"], url, slug, meta.get("type")))
    if (out/f"{slug}.png").exists() and "--all" not in sys.argv: continue
    short = meta["title"].split(":")[0].strip()
    lines = wrap(short, 21); fs = 84 if len(lines) <= 3 else 70; lines = lines[:5]; ty = 760
    tspans = "".join(f'<tspan x="80" dy="{0 if i==0 else int(fs*1.1)}">{H.escape(l)}</tspan>' for i,l in enumerate(lines))
    kicker = "RICERCA PER LA SCUOLA PRIMARIA" if meta.get("type")=="ricerca" else "GUIDA PRATICA"
    sub = wrap(meta["description"], 46)[:4]
    subs = "".join(f'<tspan x="80" dy="{0 if i==0 else 40}">{H.escape(l)}</tspan>' for i,l in enumerate(sub))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1500">
<rect width="1000" height="1500" fill="{CR}"/><rect x="0" y="0" width="1000" height="560" fill="{VC}"/>
<g transform="translate(140,40) scale(1.8)">{inner(ill)}</g>
<rect x="0" y="560" width="1000" height="16" fill="{G}"/>
<text x="80" y="670" font-family="Arial,Helvetica,sans-serif" font-size="26" font-weight="700" fill="{A}" letter-spacing="5">{kicker}</text>
<text x="80" y="{ty}" font-family="Georgia,'Times New Roman',serif" font-size="{fs}" font-weight="700" fill="{VS}">{tspans}</text>
<text x="80" y="{ty + int((len(lines)-1)*fs*1.1) + 90}" font-family="Arial,Helvetica,sans-serif" font-size="30" fill="#5e6a63">{subs}</text>
<rect x="0" y="1360" width="1000" height="140" fill="{V}"/>
<text x="80" y="1445" font-family="Georgia,'Times New Roman',serif" font-size="48" font-weight="700" fill="{W}">Piume <tspan fill="{G}" font-style="italic" font-weight="400">e</tspan> Becchi</text>
<text x="920" y="1445" text-anchor="end" font-family="Arial,Helvetica,sans-serif" font-size="30" fill="{VC}">piumeebecchi.it</text>
</svg>'''
    (out/f"{slug}.svg").write_text(svg, encoding="utf-8"); todo.append(slug)
if todo:
    js = "const sharp=require('sharp');(async()=>{for(const s of process.argv.slice(1)){await sharp(s+'.svg').resize(1000,1500).png().toFile(s+'.png');}})()"
    subprocess.run(["node","-e",js,*todo], cwd=out, check=True)
    for s in todo: (out/f"{s}.svg").unlink()
rows.sort()
md = ["# Pin Pinterest — Piume e Becchi\n", "Per ogni Pin: carica l'immagine `pin/<slug>.png`, incolla titolo, descrizione e link, scegli la bacheca.\n"]
cur=None
for board,title,desc,url,slug,typ in rows:
    if board!=cur: md.append(f"\n## Bacheca: {board}\n"); cur=board
    tags = "#uccelli #bambini #scuolaprimaria #ricercascuola" if typ=="ricerca" else "#uccelli #birdwatching #natura #bambini"
    md.append(f"### {slug}\n- **Immagine**: pin/{slug}.png\n- **Titolo**: {title[:100]}\n- **Descrizione**: {desc} {tags}\n- **Link**: {url}\n")
(out/"PIN.md").write_text("\n".join(md), encoding="utf-8")
print(f"Pin: {len(rows)} totali, {len(todo)} nuovi")
