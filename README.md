# Calendario Promo

Web app per consultare la Lista promo (file Excel) per mese o per anno, sul periodo Sell-Out.

## Uso
Apri `Calendario_Promo.html` con Chrome o Edge (doppio clic). Funziona anche offline.
Carica la Lista promo con **Carica Excel** o trascinando il file nella pagina: l'app ricorda l'ultimo file caricato.

## Sviluppo
- `src/app.html`: codice dell'app (HTML, CSS, JavaScript).
- `tools/build.py`: crea `Calendario_Promo.html` (versione unica con libreria e dati di esempio inclusi).
- `tools/xlsx.full.min.js`: libreria SheetJS 0.18.5 per leggere i file Excel.
- `tools/sample.json`: dati di esempio (file mock, dati fittizi).

```
python3 tools/build.py
```
