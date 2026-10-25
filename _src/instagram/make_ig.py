#!/usr/bin/env python3
"""Immagini Instagram 1080x1350 (4:5). Uso: python3 make_ig.py"""
import pathlib, re, html as H, subprocess
R=pathlib.Path(__file__).parent; img=R.parent/"src/assets/img"
V="#1f4d3a"; VS="#153627"; G="#f5c518"; A="#e07a2f"; W="#fff"; VC="#e4efe7"; CR="#fbf8f1"
def inner(n): return re.sub(r'^<svg[^>]*>','',(img/f"{n}.svg").read_text().strip()).replace('</svg>','')
def wrap(t,m):
    o,c=[],""
    for w in t.split():
        if len(c)+len(w)+1>m and c: o.append(c); c=w
        else: c=(c+" "+w).strip()
    return o+[c]
P=[("01-benvenuto","ricerche","BENVENUTI","Piume e Becchi: gli uccelli, spiegati bene","Schede di ricerca e guide per genitori e insegnanti della scuola primaria"),
("02-pettirosso","giardino","LO SAPEVI?","Il petto del pettirosso è arancione, non rosso","Maschio e femmina sono uguali. Scheda per la scuola primaria"),
("03-cinciallegra","giardino","SCHEDA DI RICERCA","La cinciallegra, prima ospite delle mangiatoie","Com'è fatta, cosa mangia e dove fa il nido"),
("04-civetta","dove","SCHEDA DI RICERCA","Civetta, gufo o barbagianni?","Come distinguerli. Era l'uccello sacro della dea Atena"),
("05-pinguino","ricerche","SCHEDA DI RICERCA","Il papà pinguino tiene l'uovo sulle zampe per due mesi","Il pinguino imperatore, per la scuola primaria"),
("06-inverno","giardino","GUIDA PRATICA","Cosa dare da mangiare agli uccelli in inverno (e cosa no)","Semi, grassi, frutta e gli errori più comuni")]
names=[]
for n,ill,k,t,s in P:
    L=wrap(t,20); fs=76 if len(L)<=3 else 66; y=720
    ts="".join(f'<tspan x="70" dy="{0 if i==0 else int(fs*1.12)}">{H.escape(l)}</tspan>' for i,l in enumerate(L))
    sy=y+int((len(L)-1)*fs*1.12)+85
    ss="".join(f'<tspan x="70" dy="{0 if i==0 else 42}">{H.escape(l)}</tspan>' for i,l in enumerate(wrap(s,40)))
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1350"><rect width="1080" height="1350" fill="{CR}"/>
<rect width="1080" height="500" fill="{VC}"/><g transform="translate(180,20) scale(1.7)">{inner(ill)}</g><rect y="500" width="1080" height="14" fill="{G}"/>
<text x="70" y="600" font-family="Arial,sans-serif" font-size="28" font-weight="700" fill="{A}" letter-spacing="5">{k}</text>
<text x="70" y="{y}" font-family="Georgia,serif" font-size="{fs}" font-weight="700" fill="{VS}">{ts}</text>
<text x="70" y="{sy}" font-family="Arial,sans-serif" font-size="32" fill="#5e6a63">{ss}</text>
<rect y="1200" width="1080" height="150" fill="{V}"/>
<text x="70" y="1292" font-family="Georgia,serif" font-size="52" font-weight="700" fill="{W}">Piume <tspan fill="{G}" font-style="italic" font-weight="400">e</tspan> Becchi</text>
<text x="1010" y="1292" text-anchor="end" font-family="Arial,sans-serif" font-size="30" fill="{VC}">piumeebecchi.it</text></svg>'''
    (R/f"{n}.svg").write_text(svg); names.append(n)
js="const sharp=require('sharp');(async()=>{for(const s of process.argv.slice(1)){await sharp(s+'.svg').resize(1080,1350).png().toFile(s+'.png');}})()"
subprocess.run(["node","-e",js,*names],cwd=R,check=True)
for n in names: (R/f"{n}.svg").unlink()
