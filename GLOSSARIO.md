# Glossario e regole di stile

Queste regole valgono per ogni stringa di `locales/it.json`. Chi traduce o corregge le applica senza eccezioni: la coerenza conta più della preferenza personale.

## Voce

- Dai del **tu**. Istruzioni e pulsanti all'imperativo: «Apri», «Scegli», «Riprova». Mai «Lei», mai infinito per i comandi («Salva», non «Salvare»).
- Italiano naturale e asciutto, come un'app Apple ben localizzata. Niente calchi («Questo pubblica il file» → «Pubblica il file»), niente verbi inglesi italianizzati («pushato», «committare», «mergiare», «switchare»).
- Stessa lunghezza dell'inglese, o poco più. Le etichette dei pulsanti restano di una o due parole.
- Maiuscola solo alla prima parola e ai nomi propri: «Cronologia sessioni», non «Cronologia Sessioni».
- **Orca** è maschile: «Orca non è riuscito». Dove puoi, evita l'accordo: «Impossibile salvare».
- Errori: «Could not / Couldn't / Failed to / Unable to X» → «Impossibile X». «X failed» → «X non riuscito/a».
- Conferme: «Are you sure you want to X?» → «Vuoi davvero X?».
- Stati in corso: «Loading…» → «Caricamento…», «Saving…» → «Salvataggio…» (sostantivo, non gerundio).

## Cosa non si tocca

- Segnaposto `{{nome}}`, `$t(...)` e tag `<0>…</0>`, `<bold>…</bold>`: identici all'inglese, stessa quantità. Si possono spostare nella frase, mai rinominare o tradurre.
- Numero di a capo (`\n`) uguale all'inglese. Spazi iniziali e finali uguali all'inglese.
- Punteggiatura finale come l'inglese (punto, due punti, puntini, nessuna).
- `…` o `...`, virgolette `“ ”` o `" "`: come nell'inglese. Apostrofo sempre tipografico: `l’host`, `un po’`.
- Nomi di prodotto e marchi: Orca, Orca Relay, Computer Use, Claude, Codex, GitHub, GitLab, Linear, Jira, macOS, Windows, Linux, WSL, SSH, VS Code, e ogni nome di agente o modello.
- Comandi, flag, percorsi, nomi di file, variabili, URL, codice: `git push`, `--agent`, `~/.orca`, `orca.yaml`.
- Tasti: Cmd, Ctrl, Shift, Alt, Option, Tab, Esc restano. «Enter/Return» → «Invio», «Space» → «Spazio», «Backspace» resta, «Delete» (tasto) → «Canc», frecce → «Freccia su/giù».
- Stringhe che sono solo un identificatore o un nome proprio (`github`, `zellij`, `WebSocket`) restano uguali.

## Termini git e di sviluppo: restano in inglese

| Inglese | Italiano | Note |
| --- | --- | --- |
| branch | branch (m.) | «il branch», plurale invariato |
| commit | commit (m.) | verbo: «eseguire il commit»; pulsante «Commit» |
| push / pull / fetch | push / pull / fetch (m.) | verbo: «eseguire il push»; pulsante «Push». «pushed» → «già inviato con push» |
| merge | merge (m.) | verbo: «unire»; stato «Merged» → «Unita» (pull request), «Unito» (branch) |
| rebase, stash, checkout, diff, tag, HEAD, upstream, remote | invariati | «eseguire il rebase», «il remote» |
| pull request, PR | pull request (f.), PR | «la pull request» |
| merge request, MR | merge request (f.), MR | |
| issue | issue (f.) | «la issue» |
| repository, repo | repository (m.), repo (m.) | |
| worktree | worktree (m.) | |
| staged / unstaged | in stage / non in stage | «Stage» verbo: «Aggiungi allo stage» |
| clone | clonare, clone | |
| hook, plugin, skill (f.), runtime, shell, token, prompt, host, provider, CLI (f.), API (f.), URL (m.) | invariati | |
| scrollback | scrollback | |

## Termini dell'interfaccia: in italiano

| Inglese | Italiano |
| --- | --- |
| workspace | area di lavoro (pl. aree di lavoro) |
| project | progetto |
| agent / coding agent | agente / agente di coding |
| session | sessione |
| chat | chat (f., invariato) |
| model | modello |
| effort (reasoning) | impegno |
| pane | riquadro |
| panel | pannello |
| tab | scheda |
| sidebar | barra laterale |
| status bar / toolbar / title bar / menu bar | barra di stato / barra degli strumenti / barra del titolo / barra dei menu |
| command palette | palette dei comandi |
| picker | selettore |
| dropdown | menu a discesa |
| toggle | interruttore |
| checkbox | casella di controllo |
| dialog | finestra di dialogo |
| tooltip | suggerimento |
| Settings | Impostazioni |
| Appearance / General / Advanced | Aspetto / Generali / Avanzate |
| keyboard shortcut, shortcut, keybinding | scorciatoia da tastiera, scorciatoia |
| theme / font | tema / font |
| folder, directory | cartella |
| path | percorso |
| file | file |
| environment | ambiente |
| recipe (environment, generation) | ricetta (di ambiente, di generazione) |
| automation | automazione |
| run (noun) | esecuzione |
| task / Tasks | attività / Attività |
| board | bacheca |
| terminal | terminale |
| clipboard | appunti |
| profile | profilo |
| device | dispositivo |
| emulator / simulator | emulatore / simulatore |
| notification | notifica |
| usage | utilizzo |
| plan (subscription) | piano |
| credentials | credenziali |
| API key | chiave API |
| keychain, keyring | portachiavi |
| permission (macOS privacy) | autorizzazione |
| permissions (file) | permessi |
| pair, paired, pairing | associare, associato, associazione |
| pairing code | codice di associazione |
| source control | controllo del codice sorgente |
| changes | modifiche |
| review (noun) / reviewer | revisione / revisore |
| checks (CI) | controlli |
| comment / draft | commento / bozza |
| dictation | dettatura |
| speech-to-text | riconoscimento vocale |
| timeout / timed out | timeout / tempo scaduto |
| warning / error | avviso / errore |
| default / custom | predefinito / personalizzato |
| optional / required | facoltativo / obbligatorio |
| enabled / disabled | attivo / disattivato |
| AI | IA |
| snapshot | istantanea |
| setup (script, step) | setup |
| subagent | subagente |
| to-do, todo | to-do |
| work item | elemento di lavoro |
| thread | thread (m.) |
| source (task/data source) | origine |
| onboarding | configurazione iniziale |
| dashboard | dashboard (f.) |
| feature | funzionalità |
| preview | anteprima |
| history | cronologia |
| log, logs | log |
| setting | impostazione |
| layout | layout |
| account | account |
| password | password |
| link | link |
| cookie | cookie |
| output / input | output / input |

## Verbi dei comandi

| Inglese | Italiano |
| --- | --- |
| Cancel / Undo | Annulla |
| Redo | Ripristina |
| Save / Close / Open / Edit | Salva / Chiudi / Apri / Modifica |
| Delete / Remove | Elimina / Rimuovi |
| Rename / Copy / Paste / Duplicate | Rinomina / Copia / Incolla / Duplica |
| Retry, Try again | Riprova |
| Dismiss | Ignora |
| Refresh / Reload | Aggiorna / Ricarica |
| Update (software) | Aggiorna, aggiornamento |
| Install / Uninstall | Installa / Disinstalla |
| Enable, Turn on / Disable, Turn off | Attiva / Disattiva |
| Search / Find / Filter / Sort | Cerca / Trova / Filtra / Ordina |
| Select / Choose, Pick | Seleziona / Scegli |
| Share / Download / Upload | Condividi / Scarica / Carica |
| Import / Export | Importa / Esporta |
| Start, Launch / Stop / Pause / Resume | Avvia / Interrompi / Metti in pausa / Riprendi |
| Run (verb) | Esegui |
| Restart / Quit | Riavvia / Esci |
| Sign in, Log in / Sign out, Log out | Accedi / Esci |
| Connect / Disconnect / Reconnect | Connetti / Disconnetti / Riconnetti |
| Approve / Reject | Approva / Rifiuta |
| Learn more | Scopri di più |
| Got it | Ho capito |
| Done (button) / Done (state) | Fine / Completato |
| Continue / Back / Next / Skip | Continua / Indietro / Avanti / Salta |
| Show / Hide | Mostra / Nascondi |
| Expand / Collapse | Espandi / Comprimi |
| Add / Create / New | Aggiungi / Crea / Nuovo |
| Reset | Reimposta |
| Apply / Confirm | Applica / Conferma |
| Send / Submit | Invia |
| Attach / Detach | Allega / Scollega |
| Pin / Unpin | Fissa / Rimuovi dai fissati |
| Archive / Restore | Archivia / Ripristina |

## Nomi di funzioni e scelte fissate

Decisi una volta, valgono ovunque.

| Inglese | Italiano |
| --- | --- |
| rate limit | limite di richieste |
| artifact / Artifacts | artefatto / Artefatti |
| floating workspace | area di lavoro fluttuante |
| child / parent workspace | area di lavoro figlia / padre |
| Remote Orca Servers | Server Orca remoti |
| Session History | Cronologia sessioni |
| Agent Session Search | Ricerca nelle sessioni degli agenti |
| Chat UI | Interfaccia chat |
| Source Control AI | IA per il controllo del codice sorgente |
| Explorer (pannello file di Orca) | Esplora risorse |
| File Explorer (Windows) / Finder | Esplora file / Finder |
| Task Sources | Origini delle attività |
| Runtime Environments | Ambienti runtime |
| Mobile Emulator | Emulatore mobile |
| Onboarding checklist | Checklist iniziale |
| setup script | script di setup |
| Space (uso del disco) | Spazio |
| rich editor / rich mode | editor avanzato / modalità avanzata |
| pet | mascotte |
| worker, fork, preset, sparse checkout, Git Graph, Vault | invariati |
| steer / Steer | indirizzare / Indirizza |
| side chat | chat parallela |
| goal | obiettivo |
| hand off (verbo) / handoff | passare a / passaggio di consegne |
| sleep (area di lavoro, agenti) | sospendere, sospensione |
| keep awake | tenere attivo il computer |
| kill (sessione, processo) | terminare |
| pop out / pop-out | apri in finestra separata / finestra separata |
| system tray | area di notifica |
| park (terminale) | parcheggiare |
| Force Delete | Forza eliminazione |
| Discard | Scarta |
| Re-check, Check again | Ricontrolla |
| Checking… | Verifica… |
| No matches / Next match / Previous match | Nessun risultato / Risultato successivo / Risultato precedente |
| just now | adesso |
| Zoom in / Zoom out | Aumenta zoom / Riduci zoom |
| On / Off (interruttore) | Attivo / Disattivato |
| Auto | Auto |
| login (sostantivo) | accesso |
| Toggle X | Mostra/nascondi X |
| release page / release notes | pagina delle versioni / note di versione |
| provisioning | preparazione |
| compaction | compattazione |
| turn (chat) | turno |
| hosted review (PR o MR) | revisione ospitata |
| cursor (testo) / Cursor (prodotto) | cursore / Cursor |
| background (processo) / background (grafica) | in background / sfondo |
| Ahead / Behind (commit) | Avanti / Indietro |
| unità di tempo brevi (m, h, d, w, mo) | min, h, g, sett., mesi |

Accordi: una parola isolata («Open», «Closed», «Failed», «All») prende genere e numero della cosa a cui si riferisce, che si ricava dalla chiave: pull request e issue sono femminili, area di lavoro è femminile, worktree, branch, commit, agente, terminale sono maschili.
