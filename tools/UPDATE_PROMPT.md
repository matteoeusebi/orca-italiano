# Daily alignment of the Italian pack to Orca

You are working in the repository of the unofficial Italian language pack for Orca
(`orca-plugin.json`, `locales/it.json`). Your job: if Orca has released a newer version than the
one this pack is aligned to, translate what changed, verify it, and publish. Work alone, without
asking questions; if something blocks you, stop and report it.

## Steps

1. `git status --short` must be empty and the branch must be `main`. If not, stop and report.
   Then `git pull --ff-only`.
2. `python3 tools/packtool.py status`. It prints the pack version and Orca's latest version.
   Exit 1 means aligned: say so in one line and stop. Exit 0 means an update is needed; call the
   two versions OLD (pack) and NEW (Orca). Any other exit: stop and report the error.
3. `python3 tools/packtool.py pending NEW --old OLD` writes the new and changed English strings
   to `.work/in/NNN.json` (first delete any stale `.work/out/*.json`).
4. Read `GLOSSARIO.md` fully. It is binding: terminology, informal "tu", what stays untouched.
5. For each `.work/in/NNN.json` (array of `{"id","key","en"}`; the key is context), write
   `.work/out/NNN.json` as `{"<id>": "<Italian>"}` with every id. Translate meaning, not words;
   keep placeholders `{{x}}`, `{x}`, `$t(...)` and tags identical; same line breaks, edge spaces
   and final punctuation as English; identifiers, commands and product names stay as they are.
   To stay consistent, search `locales/it.json` for how the same English term or a sibling key
   was already translated before choosing a wording. When a string is a sentence fragment or its
   role is unclear, read how Orca uses the key:
   `https://github.com/stablyai/orca/tree/vNEW/src` (search for the key literal).
   Then run `python3 tools/packtool.py chunk N` and fix until it prints `0 problems`. A glossary
   warning may stay only when it is a proven false positive.
6. `python3 tools/packtool.py merge NEW`, then all of these must succeed:
   - `python3 tools/packtool.py check NEW` → `0 errors` and coverage 100%
   - `python3 -m unittest discover -s tests`
   - `orca plugin validate .` → exit 0
   If any fails and you cannot fix the translation so that it passes, run `git checkout -- .`,
   publish nothing, and report what failed.
7. `python3 tools/packtool.py bump NEW`.
8. Commit only `locales/it.json` and `orca-plugin.json`:
   `git commit -m "feat: align to Orca NEW"` with a body giving the number of new, changed and
   removed strings. Then `git tag -a vNEW -m vNEW`, `git push origin main`, `git push origin vNEW`.
9. Final message, in Italian, three lines at most: versions, how many strings were translated,
   and anything a human should look at (unclear strings, warnings left in place).

## Never

- Never change `tools/`, `tests/`, `GLOSSARIO.md`, `README.md` or anything outside this repository.
- Never force-push, delete or move a tag, or rewrite history.
- Never publish when a check fails, and never weaken a check or add an exception to make it pass.
- Never drive a GUI or change Orca settings.
