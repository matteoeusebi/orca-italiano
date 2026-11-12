# Italiano

An Orca language pack. Keys mirror the English catalog of Orca; add translated strings to `locales/pt-BR.json`, or change the locale in `orca-plugin.json`.

## Develop

```sh
orca plugin validate .
orca plugin dev watch .    # loads this folder into Orca and prints its logs and reloads; Ctrl-C unloads it
```

Orca names the publisher after where the plugin is installed from: the GitHub or GitLab owner of
its repository, or `local` for a folder. See
https://github.com/stablyai/orca/blob/main/docs/reference/plugin-authoring.md.
