# Specifiche contenuti — Piume e Becchi (piumeebecchi.it)

Sito italiano sugli uccelli per bambini, genitori e insegnanti. Stile: chiaro, concreto, caldo, mai infantile né accademico. Modello di riferimento: miciodesign.it (guide pratiche con tabelle comparative e link Amazon).

## Formato file
Ogni articolo è un file `content/<categoria>/<slug>.html`. Prima riga: intestazione JSON tra `---` e `---`, poi il corpo in HTML (solo frammento: niente <html>, <body>, <h1>).

```
---
{"title": "Titolo con parole chiave", "description": "Due frasi (max 160 caratteri circa) che riassumono cosa trova il lettore.", "type": "guida", "pillar": true, "minutes": 10}
---
<p>Intro...</p>
<h2>Sezione</h2>
...
```

- `type`: `"guida"` oppure `"ricerca"`.
- `pillar`: `true` solo per la guida principale della categoria (una per categoria).
- `minutes`: minuti di lettura (opzionale, stimati automaticamente).
- Le `<h2>` e `<h3>` NON devono avere id: il generatore li aggiunge e costruisce il sommario.
- Il generatore aggiunge da sé: titolo H1, lead, byline, nota affiliazione, immagine, sommario, disclaimer finale, correlati. NON scriverli.

## Categorie (cartelle)
- `ricerche-scuola` — schede per la primaria
- `giardino-balcone` — mangiatoie, casette-nido, cibo, acqua
- `birdwatching-famiglie` — binocoli, guide, app, uscite con bambini
- `libri-giochi` — libri, atlanti, kit, giochi
- `dove-vederli` — oasi, parchi, escursioni in Italia
- `uccelli-in-casa` — canarini, cocorite, pappagallini

## Elementi HTML disponibili (classi già stilate)
- Tabelle normali `<table><thead>…<tbody>…` (si usano per confronti).
- `<div class="box">…</div>` box neutro; `<div class="box box-gialla">` evidenziato; `<div class="box box-verde">` box scuro per i rimandi finali.
- `<a class="btn" href="…">Vedi su Amazon</a>` bottone; `btn btn-outline` variante.
- `<blockquote>` per la regola pratica.
- `<dl><dt>…</dt><dd>…</dd></dl` per glossari.
- Solo nelle schede-ricerca: `<div class="identikit"><div><b>Nome scientifico</b>Hirundo rustica</div>…</div>` (griglia di 4-6 caselle), `<div class="glossario">`, `<ol class="domande">`.

## Link di affiliazione (solo nelle GUIDE, mai nelle schede)
Usare link di ricerca Amazon.it: `https://www.amazon.it/s?k=parole+chiave` (il tag affiliato sarà aggiunto dopo). Per altri negozi usare la home del negozio o la pagina categoria: ManoMano (manomano.it), Zooplus (zooplus.it), Feltrinelli (lafeltrinelli.it), IBS (ibs.it), Decathlon (decathlon.it), GetYourGuide (getyourguide.it). Mai inventare URL di prodotto precisi.
Prezzi: sempre "indicativi", arrotondati, in fasce (es. "60-90 €"), con "da verificare al momento dell'acquisto". Modelli: citare solo prodotti realmente esistenti e noti (es. binocoli Nikon Aculon, Olympus 8x40 DPS, Kowa YF; mangiatoie da finestra con ventose; cibo Versele-Laga, Padovan).

## Struttura GUIDA (1400-1900 parole)
1. Intro di 2-3 paragrafi: il problema concreto, cosa troverà il lettore.
2. 5-7 `<h2>` con contenuto pratico; almeno 1 tabella comparativa (tipi o modelli) e 1 elenco numerato di consigli.
3. Una `<blockquote>` con la "regola pratica".
4. `<h2>Domande frequenti</h2>` con 5-7 `<h3>` domanda + risposta breve.
5. Chiudere con `<div class="box box-verde"><h3>Per saperne di più a scuola</h3>…</div>` che rimanda a 1-2 schede-ricerca con link relativi (es. `/ricerche-scuola/rondine/`).

## Struttura SCHEDA-RICERCA (650-900 parole, livello classe 3ª-5ª primaria)
1. Intro di un paragrafo semplice.
2. `<div class="identikit">` con: Nome scientifico, Famiglia, Lunghezza, Peso, Vita media, Dove vive.
3. `<h2>` nell'ordine: Com'è fatto/a · Dove vive · Cosa mangia · Come si riproduce (nido, uova) · Il viaggio (migrazione) se pertinente · Curiosità (elenco di 4-5 punti) · È in pericolo? (stato di conservazione, in parole semplici) · Parole difficili (`<div class="glossario"><dl>…`) · Domande per ripassare (`<ol class="domande">` 5 domande con la risposta in corsivo tra parentesi).
4. Chiudere con `<div class="box box-verde"><h3>Vuoi vederla dal vivo?</h3>…</div>` con rimandi alla guida binocoli (`/birdwatching-famiglie/`) e alla guida mangiatoie (`/giardino-balcone/`) o a `/dove-vederli/`, senza link affiliati.
Frasi corte. Numeri arrotondati. Nessuna fonte inventata; i dati devono essere quelli noti da guide ornitologiche standard. Scrivere "circa".

## Link interni
Usare solo URL relativi tra questi:
/ricerche-scuola/ /giardino-balcone/ /birdwatching-famiglie/ /libri-giochi/ /dove-vederli/ /uccelli-in-casa/
e gli articoli: /ricerche-scuola/rondine/ /ricerche-scuola/gufo/ /ricerche-scuola/fenicottero/ /ricerche-scuola/migrazione-uccelli/ /ricerche-scuola/come-fare-ricerca-uccelli/
/giardino-balcone/guida-mangiatoia-uccelli-giardino-balcone/ /birdwatching-famiglie/binocolo-birdwatching-bambini-famiglie/ /libri-giochi/libri-uccelli-bambini/ /dove-vederli/dove-vedere-uccelli-italia-bambini/ /uccelli-in-casa/canarino-cocorita-pappagallino-guida/

## Lingua
Italiano corretto, seconda persona singolare ("tu") per il lettore adulto nelle guide; nelle schede, terza persona con qualche "tu" leggero. Niente emoji. Niente "in questo articolo scopriremo".
