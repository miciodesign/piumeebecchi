#!/usr/bin/env python3
"""Genera le illustrazioni SVG di categoria (stile flat, palette del sito)."""
from pathlib import Path
OUT = Path(__file__).parent / "src/assets/img"
OUT.mkdir(parents=True, exist_ok=True)

V="#1f4d3a"; VS="#153627"; VC="#e4efe7"; G="#f5c518"; GC="#fff4c2"; A="#e07a2f"; W="#ffffff"; B="#1d2520"; AZ="#6fb3d6"; R="#d9534f"; P="#f4a5b9"

def wrap(inner, bg=VC):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" role="img">\n<rect width="400" height="300" rx="28" fill="{bg}"/>\n{inner}\n</svg>\n'

def bird(x,y,s=1,body=G,wing=A,beak=A,flip=False):
    t = f'translate({x},{y}) scale({-s if flip else s},{s})'
    return f'''<g transform="{t}">
<ellipse cx="0" cy="0" rx="42" ry="30" fill="{body}"/>
<circle cx="36" cy="-18" r="20" fill="{body}"/>
<path d="M-10 -8 q-30 -30 -5 -40 q10 25 28 32 z" fill="{wing}"/>
<path d="M-40 6 l-28 -14 l6 24 z" fill="{wing}"/>
<polygon points="54,-18 72,-12 54,-8" fill="{beak}"/>
<circle cx="42" cy="-22" r="3.5" fill="{B}"/>
<path d="M-8 28 l-4 14 M4 28 l4 14" stroke="{A}" stroke-width="3" stroke-linecap="round"/>
</g>'''

# 1. Ricerche per la scuola: quaderno + uccellino + matita
ricerche = f'''
<rect x="70" y="60" width="200" height="190" rx="10" fill="{W}" stroke="{V}" stroke-width="4"/>
<rect x="70" y="60" width="26" height="190" rx="10" fill="{V}"/>
{"".join(f'<circle cx="83" cy="{y}" r="5" fill="{G}"/>' for y in range(85,240,30))}
{"".join(f'<rect x="115" y="{y}" width="{w}" height="6" rx="3" fill="{VC}"/>' for y,w in [(95,120),(113,100),(131,130),(149,90)])}
<path d="M118 175 h130 M118 193 h110 M118 211 h125" stroke="{VC}" stroke-width="6" stroke-linecap="round"/>
{bird(300,110,0.75)}
<g transform="translate(300,235) rotate(-35)"><rect x="-70" y="-10" width="110" height="20" rx="4" fill="{G}"/><polygon points="40,-10 62,0 40,10" fill="#f0c9a0"/><polygon points="55,-3 62,0 55,3" fill="{B}"/><rect x="-70" y="-10" width="16" height="20" rx="4" fill="{P}"/></g>
'''
# 2. Giardino e balcone: mangiatoia a casetta appesa + uccelli
giardino = f'''
<path d="M200 20 v40" stroke="{VS}" stroke-width="4"/>
<polygon points="200,55 110,120 290,120" fill="{A}"/>
<rect x="125" y="118" width="150" height="80" rx="6" fill="{W}" stroke="{V}" stroke-width="4"/>
<rect x="160" y="128" width="80" height="48" rx="4" fill="{VS}"/>
<rect x="110" y="195" width="180" height="16" rx="6" fill="{V}"/>
<rect x="140" y="188" width="120" height="10" rx="3" fill="#c89b5a"/>
{"".join(f'<circle cx="{x}" cy="192" r="3" fill="{B}"/>' for x in range(150,250,12))}
{bird(90,210,0.55,flip=True)}
{bird(305,215,0.55,body=AZ,wing=V)}
<ellipse cx="200" cy="270" rx="150" ry="14" fill="{V}" opacity=".35"/>
'''
# 3. Birdwatching famiglie: binocolo + uccello lontano
bw = f'''
<g transform="translate(200,170)">
<rect x="-110" y="-40" width="80" height="110" rx="24" fill="{VS}"/>
<rect x="30" y="-40" width="80" height="110" rx="24" fill="{VS}"/>
<rect x="-40" y="-20" width="80" height="50" rx="10" fill="{V}"/>
<rect x="-100" y="-60" width="60" height="40" rx="14" fill="{V}"/>
<rect x="40" y="-60" width="60" height="40" rx="14" fill="{V}"/>
<circle cx="-70" cy="55" r="22" fill="{AZ}"/><circle cx="70" cy="55" r="22" fill="{AZ}"/>
<circle cx="-78" cy="48" r="7" fill="{W}" opacity=".8"/><circle cx="62" cy="48" r="7" fill="{W}" opacity=".8"/>
<rect x="-18" y="-12" width="36" height="14" rx="4" fill="{G}"/>
</g>
{bird(330,60,0.5,body=P,wing=A)}
<path d="M40 60 q20 -14 40 0 M70 40 q15 -10 30 0" stroke="{V}" stroke-width="4" fill="none" stroke-linecap="round"/>
'''
# 4. Libri e giochi: pila di libri + uccellino sopra
libri = f'''
<rect x="90" y="200" width="220" height="34" rx="6" fill="{V}"/>
<rect x="110" y="166" width="200" height="34" rx="6" fill="{A}"/>
<rect x="95" y="132" width="190" height="34" rx="6" fill="{AZ}"/>
<rect x="120" y="98" width="170" height="34" rx="6" fill="{G}"/>
{"".join(f'<rect x="{x}" y="{y}" width="70" height="8" rx="4" fill="{W}" opacity=".8"/>' for x,y in [(150,213),(160,179),(140,145),(165,111)])}
{bird(205,70,0.6)}
<circle cx="340" cy="80" r="26" fill="{W}" stroke="{V}" stroke-width="4"/>
<text x="340" y="90" text-anchor="middle" font-family="Georgia,serif" font-weight="700" font-size="30" fill="{V}">?</text>
'''
# 5. Dove vederli: fenicottero in acqua + sole
dove = f'''
<circle cx="320" cy="70" r="34" fill="{G}"/>
<path d="M0 230 q100 -30 200 0 t200 0 v70 h-400 z" fill="{AZ}"/>
<path d="M0 250 q100 -25 200 0 t200 0 v50 h-400 z" fill="#4f9ac4"/>
<g transform="translate(170,150)">
<ellipse cx="0" cy="0" rx="48" ry="30" fill="{P}"/>
<path d="M-10 -10 q-30 -25 -10 -40 q12 20 30 28 z" fill="#e8859e"/>
<path d="M-20 25 v70 M10 25 v70" stroke="#e8859e" stroke-width="5" stroke-linecap="round"/>
<path d="M40 -10 q 35 -40 25 -90 q-5 -20 15 -25" stroke="{P}" stroke-width="14" fill="none" stroke-linecap="round"/>
<circle cx="82" cy="-125" r="15" fill="{P}"/>
<path d="M92 -118 q20 2 22 22 q-12 2 -20 -8 z" fill="{B}"/>
<circle cx="86" cy="-128" r="3" fill="{B}"/>
</g>
<path d="M40 215 l10 -30 l10 30 M70 220 l8 -24 l8 24" fill="{V}"/>
'''
# 6. Uccelli in casa: gabbia con canarino
casa = f'''
<path d="M200 30 v20" stroke="{VS}" stroke-width="5" stroke-linecap="round"/>
<path d="M110 150 a90 90 0 0 1 180 0 v90 h-180 z" fill="{W}" stroke="{V}" stroke-width="5"/>
{"".join(f'<line x1="{x}" y1="{y}" x2="{x}" y2="240" stroke="{V}" stroke-width="3"/>' for x,y in [(135,98),(160,74),(185,62),(215,62),(240,74),(265,98)])}
<rect x="100" y="238" width="200" height="22" rx="8" fill="{V}"/>
<path d="M130 200 h140" stroke="{A}" stroke-width="5" stroke-linecap="round"/>
{bird(200,172,0.55)}
<circle cx="340" cy="230" r="22" fill="{G}"/><rect x="320" y="200" width="40" height="30" rx="6" fill="{A}"/>
<path d="M40 240 q10 -40 40 -20 q20 -40 40 10" stroke="{V}" stroke-width="5" fill="none" stroke-linecap="round"/>
'''
for name, inner in [("ricerche",ricerche),("giardino",giardino),("birdwatching",bw),("libri",libri),("dove",dove),("casa",casa)]:
    (OUT/f"{name}.svg").write_text(wrap(inner), encoding="utf-8")

# favicon
(OUT/"favicon.svg").write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="{V}"/>{bird(28,34,0.42)}</svg>', encoding="utf-8")

# OG image (SVG; da convertire in PNG se possibile)
og = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630">
<rect width="1200" height="630" fill="{V}"/>
<rect x="0" y="600" width="1200" height="30" fill="{G}"/>
{bird(930,300,2.6)}
<text x="80" y="300" font-family="Georgia,serif" font-weight="700" font-size="92" fill="{W}">Piume <tspan fill="{G}" font-style="italic" font-weight="400">e</tspan> Becchi</text>
<text x="84" y="370" font-family="Arial,Helvetica,sans-serif" font-size="36" fill="{VC}">Il mondo degli uccelli spiegato a bambini,</text>
<text x="84" y="420" font-family="Arial,Helvetica,sans-serif" font-size="36" fill="{VC}">genitori e insegnanti</text>
<text x="84" y="520" font-family="Arial,Helvetica,sans-serif" font-size="28" fill="{G}">piumeebecchi.it</text>
</svg>'''
(OUT/"og-default.svg").write_text(og, encoding="utf-8")
print("SVG generati in", OUT)
