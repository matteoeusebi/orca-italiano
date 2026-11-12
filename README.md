# Italiano per Orca

L'interfaccia di [Orca](https://github.com/stablyai/orca) in italiano, come plugin di lingua. Solo dati: non esegue codice e non chiede autorizzazioni.

> Pacchetto **non ufficiale**, fatto dalla community. Non è affiliato né approvato da Stably.

L'icona riprende la mascotte di Orca, che è un disegno di Stably, con lo sfondo nei colori della bandiera italiana. È un omaggio: il disegno resta loro.

## Cosa lo distingue

- **Copertura completa.** Tutti i testi traducibili della versione di Orca a cui è allineato (oltre 18.000), nessuno lasciato in inglese per dimenticanza.
- **Un solo glossario.** Ogni termine ha una traduzione fissa, scritta in [`GLOSSARIO.md`](GLOSSARIO.md): «area di lavoro», «riquadro», «scheda», «associare». I termini git restano quelli che usi ogni giorno: branch, commit, worktree, pull request.
- **Controlli automatici a ogni modifica.** Segnaposto e tag identici all'inglese, stessi a capo, limiti di lunghezza di Orca, apostrofi tipografici, termini del glossario.
- **Riletto per intero** contro l'inglese, chiave per chiave, dopo la traduzione. I testi ambigui (frasi composte da più pezzi, parole che possono essere pulsante o stato) sono stati decisi guardando come li usa il codice di Orca.
- **Aggiornato ogni giorno.** Un controllo quotidiano allinea il pacchetto alla nuova versione di Orca, se ce n'è una.

I testi che Orca protegge (conferme distruttive, finestre di sicurezza, pagina dei plugin) restano in inglese con qualsiasi pacchetto di lingua: è una scelta di Orca, non una lacuna.

## Installazione

Da terminale:

```sh
orca plugin install matteoeusebi/orca-italiano
```

Oppure in Orca: **Settings → Plugins → Install**, incolla `https://github.com/matteoeusebi/orca-italiano`.

Poi scegli la lingua: **Settings → Appearance → Language → Italiano**.

Per aggiornare: `orca plugin update matteoeusebi.italiano`.

## Versioni

Il numero di versione è quello di Orca a cui la traduzione è allineata. Con un Orca più nuovo il pacchetto funziona lo stesso: i testi aggiunti dopo restano in inglese fino al prossimo allineamento.

## Segnalare un errore

Apri una issue con il testo che vedi, dove lo vedi e come lo scriveresti. Uno screenshot aiuta.

## Per chi contribuisce

Serve solo Python 3.9 o successivo, senza dipendenze.

```sh
python3 tools/packtool.py check 1.4.257 --warnings   # controlla locales/it.json contro l'inglese
python3 -m unittest discover -s tests                # test degli strumenti
orca plugin validate .                               # controllo di Orca
```

Allineare a una nuova versione di Orca:

```sh
python3 tools/packtool.py status                           # versione del pacchetto e ultima di Orca
python3 tools/packtool.py pending 1.4.260 --old 1.4.257   # scrive in .work/in/ solo i testi nuovi o cambiati
# traduci ogni .work/in/NNN.json in .work/out/NNN.json ({"id": "traduzione"}), seguendo GLOSSARIO.md
python3 tools/packtool.py chunk 0                          # controlla un blocco tradotto
python3 tools/packtool.py merge 1.4.260                    # unisce, toglie i testi che Orca non usa più
python3 tools/packtool.py check 1.4.260 --warnings
python3 tools/packtool.py bump 1.4.260                     # aggiorna orca-plugin.json
```

Poi commit e tag `v<versione>`. La procedura completa che segue l'agente dell'aggiornamento giornaliero è in [`tools/UPDATE_PROMPT.md`](tools/UPDATE_PROMPT.md).

Le eccezioni ai controlli, una per chiave e con il motivo evidente dal testo, stanno in `tools/exceptions.json`.

---

## English

Unofficial, community-made Italian UI language pack for [Orca](https://github.com/stablyai/orca). Data only; nothing runs. Covers every translatable string of the Orca version it is aligned to, with one enforced glossary and automated checks (placeholders, tags, line breaks, Orca's length limits). Not affiliated with or endorsed by Stably. The icon is a recoloured version of Orca's mascot, which is Stably's artwork. MIT licensed; the strings derive from Orca's MIT-licensed English catalog.

Install: `orca plugin install matteoeusebi/orca-italiano`, then Settings → Appearance → Language → Italiano.
