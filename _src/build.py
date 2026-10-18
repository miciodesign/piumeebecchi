#!/usr/bin/env python3
"""Generatore statico di Piume e Becchi.
Uso: python3 build.py  -> genera la cartella dist/
I contenuti stanno in content/<categoria>/<slug>.html con intestazione JSON tra --- ---.
"""
import json, re, shutil, html, datetime
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
CONTENT = ROOT / "content"
DIST = ROOT / "dist"

SITE = {
    "name": "Piume e Becchi",
    "domain": "piumeebecchi.it",
    "url": "https://www.piumeebecchi.it",
    "tagline": "Il mondo degli uccelli spiegato a bambini, genitori e insegnanti",
    "description": "Ricerche per la scuola primaria, guide per osservare gli uccelli in giardino, binocoli per famiglie, libri, giochi e i posti dove vederli in Italia.",
}

CATEGORIES = [
    {"slug": "ricerche-scuola", "name": "Ricerche per la scuola", "short": "Schede sulle specie, migrazione, nido, volo", "img": "ricerche.svg",
     "intro": "Schede chiare e corrette sulle specie e sui grandi temi del mondo degli uccelli, scritte per la scuola primaria: lunghezza giusta, parole spiegate, domande per ripassare."},
    {"slug": "giardino-balcone", "name": "Uccelli in giardino e sul balcone", "short": "Mangiatoie, casette-nido, cosa dare da mangiare", "img": "giardino.svg",
     "intro": "Come trasformare un giardino, un terrazzo o un davanzale in un posto dove gli uccelli vengono davvero: mangiatoie, cibo giusto, casette-nido, acqua, errori da evitare."},
    {"slug": "birdwatching-famiglie", "name": "Birdwatching per famiglie", "short": "Primo binocolo, guide, app, taccuino", "img": "birdwatching.svg",
     "intro": "Osservare gli uccelli con i bambini: quale binocolo scegliere, come riconoscere le specie più comuni, le app che funzionano, cosa portare e come non annoiarsi."},
    {"slug": "libri-giochi", "name": "Libri e giochi", "short": "Atlanti illustrati, albi, kit, puzzle", "img": "libri.svg",
     "intro": "I libri sugli uccelli che i bambini rileggono, gli atlanti che servono davvero per una ricerca, i giochi e i kit scientifici che insegnano qualcosa."},
    {"slug": "dove-vederli", "name": "Dove vederli in Italia", "short": "Oasi, parchi, fenicotteri, escursioni", "img": "dove.svg",
     "intro": "I posti in Italia dove vedere uccelli con i bambini senza fatica: oasi attrezzate, parchi con torrette, fenicotteri a due passi dalla strada, escursioni guidate."},
    {"slug": "uccelli-in-casa", "name": "Uccelli in casa", "short": "Canarini, cocorite, pappagallini", "img": "casa.svg",
     "intro": "Vivere con un canarino, una cocorita o un pappagallino: gabbia giusta, alimentazione, giochi, cosa serve davvero e cosa no."},
]
CAT = {c["slug"]: c for c in CATEGORIES}

TODAY = datetime.date.today()
MONTHS = ["gennaio","febbraio","marzo","aprile","maggio","giugno","luglio","agosto","settembre","ottobre","novembre","dicembre"]
def it_date(d): return f"{d.day} {MONTHS[d.month-1]} {d.year}"

def slugify(s):
    s = html.unescape(re.sub(r"<[^>]+>", "", s)).lower()
    s = s.replace("à","a").replace("è","e").replace("é","e").replace("ì","i").replace("ò","o").replace("ù","u")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s

# ---------- template ----------
def nav():
    return "".join(f'<a href="/{c["slug"]}/">{c["name"]}</a>' for c in CATEGORIES)

def head(title, desc, url, og_type="website", image="og-default.png"):
    full = f"{title} · {SITE['name']}" if title != SITE['name'] else f"{SITE['name']} · {SITE['tagline']}"
    return f"""<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(full)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{SITE['url']}{url}">
<meta property="og:site_name" content="{SITE['name']}">
<meta property="og:locale" content="it_IT">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{html.escape(full)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{SITE['url']}{url}">
<meta property="og:image" content="{SITE['url']}/assets/img/{image}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700&family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css">
</head>
<body>
<a class="skip" href="#main">Vai al contenuto</a>
<header class="site-header">
  <div class="wrap">
    <a class="logo" href="/">Piume <em>e</em> Becchi</a>
    <button class="menu-btn" aria-expanded="false" aria-controls="nav" onclick="this.setAttribute('aria-expanded',this.getAttribute('aria-expanded')==='true'?'false':'true');document.getElementById('nav').classList.toggle('open')">Menu</button>
    <nav id="nav" class="nav">{nav()}</nav>
  </div>
</header>
<main id="main">
"""

def footer():
    cats = "".join(f'<li><a href="/{c["slug"]}/">{c["name"]}</a></li>' for c in CATEGORIES)
    return f"""</main>
<footer class="site-footer">
  <div class="wrap grid-3">
    <div>
      <a class="logo" href="/">Piume <em>e</em> Becchi</a>
      <p>Il mondo degli uccelli spiegato a bambini, genitori e insegnanti. Schede per la scuola, guide per osservarli, prodotti scelti con cura.</p>
      <p class="muted">Non siamo veterinari né ornitologi professionisti: per un uccello ferito o malato rivolgiti a un centro di recupero o a un veterinario.</p>
    </div>
    <div>
      <h4>Categorie</h4>
      <ul>{cats}</ul>
    </div>
    <div>
      <h4>Piume e Becchi</h4>
      <ul>
        <li><a href="/chi-siamo/">Chi siamo</a></li>
        <li><a href="/contatti/">Contatti</a></li>
        <li><a href="/affiliazione/">Come ci sosteniamo</a></li>
        <li><a href="/privacy/">Privacy e cookie</a></li>
        <li><a href="https://www.instagram.com/piumeebecchi.it/" rel="noopener">Instagram</a></li>
        <li><a href="https://www.pinterest.com/piumeebecchiit/" rel="noopener">Pinterest</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap copy">© {TODAY.year} Piume e Becchi · piumeebecchi.it · Alcuni link sono di affiliazione: se compri tramite questi link riceviamo una piccola commissione, senza costi per te. <a href="/affiliazione/">Come funziona</a>.</div>
</footer>
</body>
</html>
"""

AFF_NOTE = '<p class="aff-note">Alcuni link in questa pagina sono di affiliazione: se compri tramite questi link riceviamo una piccola commissione, senza costi per te. <a href="/affiliazione/">Come funziona</a>.</p>'

# ---------- content loading ----------
def load_articles():
    arts = []
    for f in sorted(CONTENT.glob("*/*.html")):
        txt = f.read_text(encoding="utf-8")
        m = re.match(r"^---\s*(\{.*?\})\s*---\s*(.*)$", txt, re.S)
        if not m:
            raise SystemExit(f"Intestazione mancante in {f}")
        meta = json.loads(m.group(1))
        meta["body"] = m.group(2)
        meta.setdefault("slug", f.stem)
        meta.setdefault("date", TODAY.isoformat())
        meta["category"] = meta.get("category") or f.parent.name
        meta["url"] = f"/{meta['category']}/{meta['slug']}/"
        meta["image"] = meta.get("image") or CAT[meta["category"]]["img"]
        meta["minutes"] = meta.get("minutes") or max(3, round(len(re.sub(r'<[^>]+>','',meta['body']).split())/180))
        arts.append(meta)
    arts.sort(key=lambda a: (a["date"], a["slug"]), reverse=True)
    return arts

def add_ids_and_toc(body):
    toc = []
    def repl(m):
        level, attrs, inner = m.group(1), m.group(2), m.group(3)
        sid = slugify(inner)
        toc.append((int(level), sid, re.sub(r"<[^>]+>","",inner)))
        return f'<h{level} id="{sid}"{attrs}>{inner}</h{level}>'
    body = re.sub(r"<h([23])([^>]*)>(.*?)</h\1>", repl, body, flags=re.S)
    if not toc: return body, ""
    out = ['<nav class="toc" aria-label="Sommario"><p class="toc-title">In questa pagina</p><ul>']
    open_sub = False
    for lvl, sid, text in toc:
        if lvl == 2:
            if open_sub: out.append("</ul></li>"); open_sub = False
            else:
                if len(out) > 1: out.append("</li>")
            out.append(f'<li><a href="#{sid}">{text}</a>')
        else:
            if not open_sub: out.append("<ul>"); open_sub = True
            out.append(f'<li><a href="#{sid}">{text}</a></li>')
    if open_sub: out.append("</ul>")
    out.append("</li></ul></nav>")
    return body, "".join(out)

def card(a, big=False):
    c = CAT[a["category"]]
    kind = "Ricerca" if a.get("type") == "ricerca" else "Guida"
    return f"""<article class="card{' big' if big else ''}">
  <a class="card-img" href="{a['url']}"><img src="/assets/img/{a['image']}" alt="" loading="lazy"></a>
  <div class="card-body">
    <p class="meta"><a href="/{c['slug']}/">{c['name']}</a> · {kind} · {a['minutes']} min</p>
    <h3><a href="{a['url']}">{a['title']}</a></h3>
    <p>{a['description']}</p>
  </div>
</article>"""

def related(arts, a, n=3):
    same = [x for x in arts if x["category"] == a["category"] and x["slug"] != a["slug"]]
    other = [x for x in arts if x["category"] != a["category"]]
    pick = (same + other)[:n]
    if not pick: return ""
    return '<section class="related wrap-narrow"><h2>Da leggere anche</h2><div class="cards">' + "".join(card(x) for x in pick) + "</div></section>"

def write(path, content):
    p = DIST / path.strip("/") / "index.html" if path != "/" else DIST / "index.html"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")

# ---------- pages ----------
def build_article(a, arts):
    c = CAT[a["category"]]
    body, toc = add_ids_and_toc(a["body"])
    is_ric = a.get("type") == "ricerca"
    d = datetime.date.fromisoformat(a["date"])
    byline = f"Redazione Piume e Becchi · Aggiornato il {it_date(d)} · {a['minutes']} minuti di lettura"
    closing = ('<p class="disclaimer">Questa scheda è pensata per la scuola primaria: i numeri sono arrotondati e le parole difficili sono spiegate. Per una ricerca delle medie o superiori, verifica i dati su un atlante aggiornato.</p>'
               if is_ric else
               '<p class="disclaimer">Questo articolo parla di oggetti, abitudini e posti. Per un uccello ferito, malato o caduto dal nido rivolgiti a un centro di recupero fauna selvatica (CRAS) o a un veterinario.</p>')
    if a.get("closing"): closing = f'<p class="disclaimer">{a["closing"]}</p>'
    schema = json.dumps({
        "@context":"https://schema.org","@type":"Article","headline":a["title"],"description":a["description"],
        "datePublished":a["date"],"dateModified":a["date"],"inLanguage":"it",
        "author":{"@type":"Organization","name":SITE["name"]},"publisher":{"@type":"Organization","name":SITE["name"]},
        "mainEntityOfPage":SITE["url"]+a["url"]}, ensure_ascii=False)
    page = head(a["title"], a["description"], a["url"], "article", a["image"].replace(".svg",".png") if False else a["image"]) + f"""
<article class="article wrap-narrow{' ricerca' if is_ric else ''}">
  <p class="crumbs"><a href="/">Home</a> › <a href="/{c['slug']}/">{c['name']}</a></p>
  <h1>{a['title']}</h1>
  <p class="lead">{a['description']}</p>
  <p class="byline">{byline}</p>
  {'' if is_ric else AFF_NOTE}
  <figure class="hero"><img src="/assets/img/{a['image']}" alt="{html.escape(a['title'])}"></figure>
  {toc}
  <div class="prose">
  {body}
  </div>
  {closing}
</article>
{related(arts, a)}
<script type="application/ld+json">{schema}</script>
""" + footer()
    write(a["url"], page)

def build_category(c, arts):
    mine = [a for a in arts if a["category"] == c["slug"]]
    pillar = next((a for a in mine if a.get("pillar")), None)
    others = [a for a in mine if a is not pillar]
    url = f"/{c['slug']}/"
    page = head(c["name"], c["intro"], url, image=c["img"]) + f"""
<section class="cat-hero wrap">
  <p class="crumbs"><a href="/">Home</a> › {c['name']}</p>
  <div class="cat-hero-grid">
    <div><h1>{c['name']}</h1><p class="lead">{c['intro']}</p></div>
    <img src="/assets/img/{c['img']}" alt="">
  </div>
</section>
"""
    if pillar:
        page += f"""<section class="wrap"><h2 class="section-title">Da dove cominciare</h2><div class="cards">{card(pillar, big=True)}</div></section>"""
    if others:
        page += f"""<section class="wrap"><h2 class="section-title">Tutti gli articoli</h2><div class="cards">{''.join(card(a) for a in others)}</div></section>"""
    if not mine:
        page += '<section class="wrap"><p class="lead">Stiamo scrivendo le prime guide di questa sezione. Torna tra qualche giorno.</p></section>'
    write(url, page + footer())

def build_home(arts):
    pillars = []
    for c in CATEGORIES:
        p = next((a for a in arts if a["category"] == c["slug"] and a.get("pillar")), None)
        href = p["url"] if p else f"/{c['slug']}/"
        pillars.append(f'<a class="start" href="{href}"><img src="/assets/img/{c["img"]}" alt=""><span><strong>{c["name"]}</strong><small>{c["short"]}</small><em>Leggi la guida completa →</em></span></a>')
    ricerche = [a for a in arts if a.get("type") == "ricerca"][:4]
    latest = [a for a in arts if a.get("type") != "ricerca"][:6]
    page = head(SITE["name"], SITE["description"], "/") + f"""
<section class="hero wrap">
  <p class="eyebrow">Per bambini curiosi, genitori e insegnanti</p>
  <h1>Il mondo degli uccelli, spiegato bene.</h1>
  <p class="lead">Schede pronte per le ricerche di scuola, guide per far venire gli uccelli sul balcone, il primo binocolo, i libri giusti e i posti dove vederli dal vivo. Niente nozioni da ornitologo, solo cose chiare e verificate.</p>
  <p class="chips">{"".join(f'<a href="/{c["slug"]}/">{c["name"]}</a>' for c in CATEGORIES)}</p>
</section>
<section class="wrap">
  <h2 class="section-title">Da dove cominciare</h2>
  <p class="section-sub">Sei sezioni, sei guide complete. Ogni guida è il punto di partenza della sua categoria.</p>
  <div class="starts">{"".join(pillars)}</div>
</section>
<section class="wrap ricerche-band">
  <div class="band-head"><h2 class="section-title">Ricerche per la scuola</h2><a class="more" href="/ricerche-scuola/">Tutte le schede →</a></div>
  <p class="section-sub">Schede di una pagina, scritte per la primaria: cosa mangia, dove vive, quanto vive, le curiosità che restano in mente e tre domande per ripassare.</p>
  <div class="cards">{"".join(card(a) for a in ricerche)}</div>
</section>
<section class="wrap">
  <h2 class="section-title">Ultimi articoli</h2>
  <div class="cards">{"".join(card(a) for a in latest)}</div>
</section>
<section class="wrap how">
  <h2 class="section-title">Come scegliamo quello che consigliamo</h2>
  <div class="grid-3">
    <div><strong>Prodotti reali, prezzi verificati.</strong><p>Ogni confronto nasce da schede tecniche, recensioni di chi li usa e, quando possibile, prova diretta. I prezzi sono indicativi e li aggiorniamo ogni tre mesi.</p></div>
    <div><strong>Scritto per la scuola, letto dai genitori.</strong><p>Le schede sono corrette ma semplici: lunghezza da ricerca di quarta, parole difficili spiegate tra parentesi, nessuna fonte inventata.</p></div>
    <div><strong>Gli uccelli selvatici restano selvatici.</strong><p>Spieghiamo come aiutarli e osservarli senza disturbarli. Un uccello ferito va a un centro di recupero, non in una scatola in casa.</p></div>
  </div>
</section>
""" + footer()
    write("/", page)

def build_static(arts):
    pages = {
        "/chi-siamo/": ("Chi siamo", "Chi scrive Piume e Becchi e perché.", """
<h1>Chi siamo</h1>
<p class="lead">Piume e Becchi nasce da una cosa semplice: una ricerca sul gufo da fare per lunedì e nessun sito che la spiegasse bene a un bambino di nove anni.</p>
<div class="prose">
<p>Siamo una piccola redazione di genitori e appassionati di natura. Non siamo ornitologi professionisti e non fingiamo di esserlo: controlliamo quello che scriviamo su guide di riconoscimento aggiornate, sui siti delle associazioni (LIPU, EBN Italia, ISPRA) e, per i prodotti, su schede tecniche e recensioni di chi li ha usati davvero.</p>
<h2>Cosa trovi qui</h2>
<ul>
<li><strong>Schede per la scuola</strong>: una pagina per specie o per tema, scritta per la primaria. Si possono stampare e usare in classe.</li>
<li><strong>Guide pratiche</strong>: mangiatoie, binocoli, libri, gabbie, oasi da visitare. Diciamo cosa comprare e cosa evitare.</li>
<li><strong>Posti</strong>: dove andare a vedere gli uccelli con i bambini senza camminare quattro ore.</li>
</ul>
<h2>Cosa non trovi</h2>
<p>Consigli veterinari. Se un uccello è ferito, malato o caduto dal nido, la risposta giusta è sempre un centro di recupero della fauna selvatica (CRAS) o un veterinario, non un articolo su internet.</p>
<h2>Per insegnanti</h2>
<p>Le schede sono libere per l'uso in classe. Se le stampi o le proietti, ci fa piacere una citazione del sito. Se trovi un errore, <a href="/contatti/">scrivici</a>: correggiamo in giornata.</p>
</div>"""),
        "/contatti/": ("Contatti", "Come scrivere alla redazione di Piume e Becchi.", """
<h1>Contatti</h1>
<p class="lead">Per segnalare un errore, proporre un argomento o parlarci di collaborazioni.</p>
<div class="prose">
<p>Scrivi a <a href="mailto:redazione@piumeebecchi.it">redazione@piumeebecchi.it</a>. Rispondiamo di solito entro due giorni lavorativi.</p>
<h2>Insegnanti e scuole</h2>
<p>Se usi le nostre schede in classe e vorresti una scheda su una specie che non abbiamo ancora, dillo: le richieste delle scuole hanno la precedenza.</p>
<h2>Aziende e negozi</h2>
<p>Lavoriamo con programmi di affiliazione e, in casi selezionati, con prodotti inviati in prova. Non pubblichiamo articoli a pagamento non segnalati e non modifichiamo i giudizi. Leggi <a href="/affiliazione/">come ci sosteniamo</a> prima di scriverci.</p>
<h2>Uccelli feriti</h2>
<p>Non possiamo aiutare in questi casi. Cerca il <strong>CRAS</strong> (Centro Recupero Animali Selvatici) della tua provincia o chiama la LIPU: hanno le persone e i permessi per intervenire.</p>
</div>"""),
        "/affiliazione/": ("Come ci sosteniamo", "Come funzionano i link di affiliazione su Piume e Becchi e cosa cambia per te.", """
<h1>Come ci sosteniamo</h1>
<p class="lead">Piume e Becchi è gratuito e senza abbonamenti. Si sostiene con i link di affiliazione: ecco cosa significa, in parole semplici.</p>
<div class="prose">
<h2>Cos'è un link di affiliazione</h2>
<p>Quando in una guida trovi un link a un prodotto (una mangiatoia, un binocolo, un libro) e lo compri, il negozio ci riconosce una piccola percentuale sul prezzo. <strong>Per te non cambia nulla</strong>: il prezzo è lo stesso che pagheresti arrivando al negozio da soli.</p>
<h2>Con chi lavoriamo</h2>
<p>Partecipiamo al Programma Affiliazione Amazon EU e a programmi di altri negozi (librerie online, negozi di giardinaggio e per animali, ottiche, piattaforme di escursioni). Le pagine con link di affiliazione hanno sempre la nota in alto.</p>
<h2>Cosa non facciamo</h2>
<ul>
<li>Non consigliamo un prodotto perché paga di più: la scelta nasce dal confronto, poi cerchiamo il link.</li>
<li>Non pubblichiamo recensioni positive a pagamento.</li>
<li>Non mettiamo link nelle schede per la scuola. Quelle restano pulite: se vuoi approfondire con un libro o un binocolo, trovi un rimando in fondo alla pagina, segnalato.</li>
</ul>
<h2>Prezzi</h2>
<p>I prezzi indicati sono quelli visti al momento della scrittura e li ricontrolliamo ogni tre mesi. Il prezzo vero è sempre quello sulla pagina del negozio.</p>
<p>In qualità di Affiliato Amazon, riceviamo un guadagno dagli acquisti idonei.</p>
</div>"""),
        "/privacy/": ("Privacy e cookie", "Informativa privacy e cookie di piumeebecchi.it.", f"""
<h1>Privacy e cookie</h1>
<p class="lead">Raccogliamo il minimo indispensabile. Qui trovi cosa e perché.</p>
<div class="prose">
<h2>Titolare</h2>
<p>Il titolare del trattamento è la redazione di Piume e Becchi, contattabile a <a href="mailto:redazione@piumeebecchi.it">redazione@piumeebecchi.it</a>.</p>
<h2>Dati raccolti</h2>
<p>Il sito non ha registrazione né commenti. Il server registra automaticamente i log di accesso (indirizzo IP, pagina richiesta, data e ora, browser) per sicurezza e statistiche aggregate, conservati per il tempo tecnico necessario.</p>
<p>Se ci scrivi via e-mail, conserviamo il messaggio per il tempo necessario a risponderti.</p>
<h2>Cookie</h2>
<p>Il sito usa solo cookie tecnici. I link verso negozi partner (Amazon e altri) possono impostare cookie sui loro domini per attribuire l'eventuale acquisto: sono gestiti dai rispettivi siti secondo le loro informative. Se in futuro aggiungeremo strumenti di statistica o pubblicità, aggiorneremo questa pagina e chiederemo il consenso dove richiesto.</p>
<h2>I tuoi diritti</h2>
<p>Puoi chiedere accesso, rettifica o cancellazione dei dati che ti riguardano scrivendo all'indirizzo sopra. Puoi anche rivolgerti al Garante per la protezione dei dati personali.</p>
<p class="muted">Ultimo aggiornamento: {it_date(TODAY)}.</p>
</div>"""),
    }
    for url, (title, desc, body) in pages.items():
        write(url, head(title, desc, url) + f'<article class="article wrap-narrow"><p class="crumbs"><a href="/">Home</a> › {title}</p>{body}</article>' + footer())

def build_sitemap(arts):
    urls = ["/"] + [f"/{c['slug']}/" for c in CATEGORIES] + [a["url"] for a in arts] + ["/chi-siamo/","/contatti/","/affiliazione/","/privacy/"]
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    xml += "".join(f"  <url><loc>{SITE['url']}{u}</loc><lastmod>{TODAY.isoformat()}</lastmod></url>\n" for u in urls) + "</urlset>\n"
    (DIST/"sitemap.xml").write_text(xml, encoding="utf-8")
    (DIST/"robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE['url']}/sitemap.xml\n", encoding="utf-8")

def main():
    if DIST.exists(): shutil.rmtree(DIST)
    DIST.mkdir()
    shutil.copytree(SRC/"assets", DIST/"assets")
    arts = load_articles()
    for a in arts: build_article(a, arts)
    for c in CATEGORIES: build_category(c, arts)
    build_home(arts)
    build_static(arts)
    build_sitemap(arts)
    shutil.copy(SRC/"htaccess.txt", DIST/".htaccess")
    (DIST/"404.html").write_text(head("Pagina non trovata","Questa pagina non esiste.","/404.html")+'<article class="article wrap-narrow"><p class="crumbs"><a href="/">Home</a></p><h1>Pagina non trovata</h1><p class="lead">Questa pagina è volata via. Torna alla <a href="/">home</a> o scegli una sezione dal menu.</p></article>'+footer(), encoding="utf-8")
    print(f"OK: {len(arts)} articoli, {len(CATEGORIES)} categorie -> {DIST}")

if __name__ == "__main__":
    main()
