#!/usr/bin/env python3
"""Genera i PDF A4 da stampare in src/assets/download/. Uso: python3 make_schede.py"""
import pathlib, html as H
from playwright.sync_api import sync_playwright
R=pathlib.Path(__file__).parent; OUT=R/"src/assets/download"; OUT.mkdir(parents=True,exist_ok=True)
V="#1f4d3a"; G="#f5c518"; A="#e07a2f"; VC="#e4efe7"
CSS=f"""@page{{size:A4;margin:0}}*{{box-sizing:border-box}}body{{margin:0;font-family:'Nunito',Arial,sans-serif;color:#17332a}}
.p{{width:210mm;height:297mm;padding:14mm 15mm 12mm;position:relative;page-break-after:always;overflow:hidden}}
.top{{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:3px solid {G};padding-bottom:3mm;margin-bottom:6mm}}
h1{{font-family:Georgia,serif;font-size:25pt;margin:0;color:{V}}}h2{{font-family:Georgia,serif;font-size:14pt;margin:5mm 0 2mm;color:{V}}}
.k{{font-size:8.5pt;letter-spacing:2px;color:{A};font-weight:700}}
.f{{position:absolute;left:15mm;right:15mm;bottom:8mm;display:flex;justify-content:space-between;font-size:8.5pt;color:#5e6a63;border-top:1px solid #cfd8d2;padding-top:2mm}}
.f b{{font-family:Georgia,serif;color:{V}}}
.line{{border-bottom:1px solid #9fb3a8;height:8.5mm;font-size:9pt;color:#5e6a63}}
.row{{display:flex;gap:5mm}}.row>div{{flex:1}}
.box{{border:2px solid {V};border-radius:4mm;padding:3mm}}
.lab{{font-size:9pt;font-weight:700;color:{V}}}
.draw{{border:2px dashed #9fb3a8;border-radius:4mm;height:62mm;padding:2mm;font-size:9pt;color:#7b8a82}}
.chk span{{display:inline-block;margin-right:4mm;font-size:10pt}}.chk i{{display:inline-block;width:3.6mm;height:3.6mm;border:1.5px solid {V};border-radius:1mm;vertical-align:-0.5mm;margin-right:1.5mm}}
.cover{{background:{VC};text-align:center;padding-top:50mm;height:271mm;margin:-14mm -15mm;padding-left:15mm;padding-right:15mm;padding-top:64mm}}.cover h1{{font-size:38pt;line-height:1.1}}
.cover .big{{width:60mm;height:60mm;margin:12mm auto;border-radius:50%;background:{G};display:flex;align-items:center;justify-content:center;font-size:42pt}}
.card{{border:3px solid {V};border-radius:5mm;padding:4mm;width:86mm;background:#fff}}
.card h3{{margin:0 0 2mm;text-align:center;font-family:Georgia,serif;color:{V};font-size:12pt}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:2mm}}
.c{{border:1.5px solid {V};border-radius:2.5mm;height:30mm;display:flex;align-items:center;justify-content:center;text-align:center;font-weight:800;font-size:10.5pt;padding:1mm;background:{VC}}}
.c.s{{background:#fff7d1;border-color:{A};font-size:8.5pt}}
"""
def page(body): return f'<div class="p">{body}</div>'
def foot(t): return f'<div class="f"><span><b>Piume e Becchi</b> · {t}</span><span>piumeebecchi.it · uso libero in famiglia e a scuola</span></div>'
def lines(n): return '<div class="line"></div>'*n

# ---- Taccuino ----
def log_page(i):
    return page(f'''<div class="top"><div><div class="k">IL MIO TACCUINO DEL BIRDWATCHER</div><h1>Oggi ho visto…</h1></div><div class="lab">Pagina {i}</div></div>
<div class="row"><div><div class="lab">Data</div><div class="line"></div></div><div><div class="lab">Ora</div><div class="line"></div></div><div><div class="lab">Dove ero</div><div class="line"></div></div></div>
<div class="lab" style="margin-top:3mm">Com'era il tempo?</div><div class="chk"><span><i></i>Sole</span><span><i></i>Nuvoloso</span><span><i></i>Pioggia</span><span><i></i>Vento</span><span><i></i>Freddo</span></div>
<h2>L'uccello che ho visto</h2>
<div class="row"><div><div class="lab">Come lo chiamo (anche se non so il nome)</div><div class="line"></div></div></div>
<div class="lab" style="margin-top:3mm">Quanto è grande? Come un…</div><div class="chk"><span><i></i>Passero</span><span><i></i>Merlo</span><span><i></i>Piccione</span><span><i></i>Gabbiano</span><span><i></i>Più grande</span></div>
<div class="lab" style="margin-top:3mm">Di che colori è?</div>{lines(1)}
<div class="lab" style="margin-top:2mm">Cosa stava facendo?</div><div class="chk"><span><i></i>Mangiava</span><span><i></i>Cantava</span><span><i></i>Volava</span><span><i></i>Beveva</span><span><i></i>Riposava</span></div>
<h2>Il mio disegno</h2><div class="draw">Disegna l'uccello e scrivi i colori con le frecce.</div>
<h2>Le mie osservazioni</h2>{lines(3)}
<div class="lab" style="margin-top:3mm">Ho scoperto che il suo nome è… (cerca sulle schede di piumeebecchi.it)</div>{lines(1)}{foot("Taccuino del birdwatcher")}''')
tacc = page(f'''<div class="cover"><div class="k">PIUME E BECCHI</div><h1>Il mio taccuino<br>del birdwatcher</h1><div class="big">🐦</div>
<div class="lab" style="font-size:13pt">Questo taccuino appartiene a</div><div class="line" style="width:110mm;margin:0 auto;height:12mm"></div>
<p style="margin-top:12mm;font-size:11pt">Stampa le pagine, ritagliale o pinzale insieme<br>e porta il taccuino in giardino, al parco o sul balcone.</p>{foot("Taccuino del birdwatcher")}</div>''') \
 + page(f'''<div class="top"><div><div class="k">PRIMA DI COMINCIARE</div><h1>5 regole del birdwatcher</h1></div></div>
<ol style="font-size:13pt;line-height:1.7"><li><b>Sta' fermo e in silenzio.</b> Gli uccelli si spaventano dei movimenti bruschi.</li><li><b>Guarda da lontano.</b> Non avvicinarti ai nidi e non toccare mai uova o piccoli.</li><li><b>Usa gli occhi e le orecchie.</b> Molti uccelli si sentono prima di vederli.</li><li><b>Scrivi subito quello che vedi.</b> Dopo qualche minuto i dettagli si dimenticano.</li><li><b>Se trovi un uccello ferito, non portarlo a casa.</b> Chiedi aiuto a un adulto: sul sito trovi chi chiamare (piumeebecchi.it/aiuto-uccello-ferito/).</li></ol>
<h2>Idee per cominciare</h2><p style="font-size:12pt;line-height:1.6">Il momento migliore è la mattina presto o verso sera. Siediti dieci minuti vicino a un albero, a una siepe o a una mangiatoia e conta quanti uccelli diversi arrivano.</p>
<div class="box" style="margin-top:6mm;background:#fff7d1;border-color:{A}"><b>Sfida:</b> riesci a riempire tutte le pagine del taccuino? Per ogni uccello prova a scoprire il nome con le schede di ricerca del sito.</div>{foot("Taccuino del birdwatcher")}''') \
 + "".join(log_page(i) for i in (1,2,3))

# ---- Bingo ----
BIRDS=["Passero","Merlo","Pettirosso","Cinciallegra","Piccione","Gabbiano","Rondine","Storno","Cornacchia","Tortora","Fringuello","Gazza","Cardellino","Ghiandaia","Picchio","Rondone","Gheppio","Germano reale","Cigno","Airone"]
import itertools, random
random.seed(7)
cards=[]
for n in range(8):
    b=random.sample(BIRDS,8); b.insert(4,"★ Un uccello che canta"); cards.append(b)
def card(n,b):
    cells="".join(f'<div class="c{" s" if "★" in x else ""}">{H.escape(x)}</div>' for x in b)
    return f'<div class="card"><h3>Bingo n. {n}</h3><div class="grid">{cells}</div></div>'
bingo = page(f'''<div class="top"><div><div class="k">GIOCO DA FARE ALL'APERTO</div><h1>Il bingo degli uccelli</h1></div></div>
<h2>Come si gioca</h2><ol style="font-size:12.5pt;line-height:1.65"><li>Ogni giocatore prende una cartella e una matita.</li><li>Uscite in giardino, al parco o guardate dalla finestra.</li><li>Quando vedi o senti uno degli uccelli sulla tua cartella, fai una croce sulla casella.</li><li>Vince chi completa per primo una riga, una colonna o una diagonale. Gridate <b>"Bingo!"</b></li><li>Per vincere il gioco grande: riempi tutta la cartella!</li></ol>
<div class="box" style="background:#fff7d1;border-color:{A};margin-top:4mm"><b>Regole d'oro:</b> si gioca a distanza dagli uccelli e senza fare rumore. Non serve vedere tutti gli uccelli: alcuni dipendono dal posto e dalla stagione.</div>
<h2>Per chi vuole saperne di più</h2><p style="font-size:12pt;line-height:1.6">Dopo il gioco, scegli un uccello della tua cartella e scopri com'è fatto, cosa mangia e dove fa il nido con le schede di ricerca su <b>piumeebecchi.it</b>.</p>{foot("Bingo degli uccelli")}''') \
 + page(f'<div class="top"><div><div class="k">RITAGLIA E GIOCA</div><h1>Cartelle 1-4</h1></div></div><div style="display:grid;grid-template-columns:1fr 1fr;gap:8mm 6mm">'+"".join(card(i+1,cards[i]) for i in range(4))+f'</div>{foot("Bingo degli uccelli")}') \
 + page(f'<div class="top"><div><div class="k">RITAGLIA E GIOCA</div><h1>Cartelle 5-8</h1></div></div><div style="display:grid;grid-template-columns:1fr 1fr;gap:8mm 6mm">'+"".join(card(i+1,cards[i]) for i in range(4,8))+f'</div>{foot("Bingo degli uccelli")}')

# ---- Scheda di ricerca da compilare ----
ric = page(f'''<div class="top"><div><div class="k">LA MIA RICERCA SUGLI UCCELLI</div><h1>Scheda da compilare</h1></div></div>
<div class="row"><div><div class="lab">Il mio nome e la mia classe</div><div class="line"></div></div><div><div class="lab">Data</div><div class="line"></div></div></div>
<div class="row" style="margin-top:2mm"><div><div class="lab">L'uccello che ho scelto</div><div class="line"></div></div><div><div class="lab">Nome scientifico</div><div class="line"></div></div></div>
<div class="row" style="margin-top:3mm"><div class="draw" style="height:60mm">Qui il mio disegno o la mia foto</div><div><div class="lab">Carta d'identità</div><div class="line">Lunghezza: </div><div class="line">Peso: </div><div class="line">Vive: </div><div class="line">Quanto vive: </div><div class="line">Famiglia: </div></div></div>
<h2>Com'è fatto</h2>{lines(3)}<h2>Dove vive</h2>{lines(2)}<h2>Cosa mangia</h2>{lines(2)}<h2>Come fa il nido e i piccoli</h2>{lines(3)}{foot("Scheda di ricerca")}''') \
 + page(f'''<div class="top"><div><div class="k">LA MIA RICERCA SUGLI UCCELLI</div><h1>Curiosità e conclusione</h1></div></div>
<h2>Tre curiosità che ho scoperto</h2>{lines(5)}<h2>È in pericolo? Cosa possiamo fare per aiutarlo?</h2>{lines(3)}
<h2>Una parola difficile che ho imparato</h2><div class="row"><div><div class="lab">Parola</div><div class="line"></div></div><div style="flex:2"><div class="lab">Cosa vuol dire</div><div class="line"></div></div></div>
<h2>Le mie fonti (dove ho cercato)</h2>{lines(3)}
<div class="box" style="margin-top:5mm;background:#fff7d1;border-color:{A}"><b>Consiglio per la ricerca:</b> scrivi con parole tue, non copiare. Trovi le schede di ricerca già pronte e la guida "Come fare una ricerca sugli uccelli" su <b>piumeebecchi.it</b>.</div>{foot("Scheda di ricerca")}''')

def build(name, body):
    html=f'<!doctype html><html lang="it"><meta charset="utf-8"><style>{CSS}</style><body>{body}</body></html>'
    f=R/"schede"/f"{name}.html"; f.write_text(html,encoding="utf-8")
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page(); pg.goto(f.as_uri()); pg.wait_for_timeout(300)
        pg.pdf(path=str(OUT/f"{name}.pdf"),format="A4",print_background=True,prefer_css_page_size=True); b.close()
    f.unlink()
build("taccuino-del-birdwatcher",tacc); build("bingo-degli-uccelli",bingo); build("scheda-ricerca-uccelli",ric)
print("ok")
