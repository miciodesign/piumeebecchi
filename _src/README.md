# Piume e Becchi — piumeebecchi.it

Sito statico (solo HTML/CSS, nessun database) sul mondo degli uccelli per bambini, genitori e insegnanti.

## Struttura della cartella
- `dist/` → **il sito pronto**: è questa cartella che va caricata online.
- `content/<categoria>/<slug>.html` → gli articoli (testo + intestazione JSON). Per aggiungere un articolo basta creare un file qui e rilanciare il build.
- `src/assets/` → CSS e immagini.
- `build.py` → genera `dist/` da `content/` e `src/`. Si lancia con `python3 build.py`.
- `make_svg.py` → rigenera le illustrazioni di categoria (non serve toccarlo).
- `CONTENT_SPEC.md` → regole di formato per scrivere nuovi articoli.

## Pubblicare su Hostinger
1. Nel pannello Hostinger apri **Gestione file** (o usa FTP).
2. Entra in `public_html/` e svuotala (o lascia solo `.htaccess` se già presente).
3. Carica **il contenuto** di `dist/` (non la cartella `dist` stessa): `index.html`, `assets/`, le cartelle delle categorie, `sitemap.xml`, `robots.txt`.
4. Carica anche il file `.htaccess` incluso in `dist/` (forza https e www, pagine senza `.html`).
5. Verifica che `https://www.piumeebecchi.it/` apra la home e `https://www.piumeebecchi.it/ricerche-scuola/rondine/` apra la scheda.

## Secondo dominio (piumebecchi.it)
Non creare un secondo sito. In Hostinger → Domini → piumebecchi.it → **Reindirizzamenti**: aggiungi un redirect 301 da `piumebecchi.it` (e `www.piumebecchi.it`) a `https://www.piumeebecchi.it`. Così chi sbaglia a scrivere arriva comunque sul sito e Google non vede contenuti duplicati.

## Dopo la pubblicazione
- **Google Search Console**: aggiungi la proprietà e invia `https://www.piumeebecchi.it/sitemap.xml`.
- **Amazon Associates**: una volta ottenuto il tag (es. `piumeebecchi-21`), sostituisci in blocco i link `amazon.it/s?k=...` con `amazon.it/s?k=...&tag=piumeebecchi-21`. Si può fare in `build.py` aggiungendo una riga di `replace` prima di scrivere le pagine.
- **Altri programmi**: ManoMano, Zooplus, Feltrinelli, Decathlon, GetYourGuide si trovano su Awin/TradeDoubler; i link vanno sostituiti con quelli tracciati forniti dalla rete.

## Aggiungere un articolo
1. Crea `content/<categoria>/<nuovo-slug>.html` seguendo `CONTENT_SPEC.md`.
2. `python3 build.py`
3. Ricarica su Hostinger la cartella generata in `dist/<categoria>/<nuovo-slug>/`, la home (`index.html`), la pagina della categoria e `sitemap.xml`.
