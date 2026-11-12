"""Pure helpers for Orca i18n catalogs: flattening, protected copy, string rules."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

PLURAL_SUFFIX_RE = re.compile(r"_(?:zero|one|two|few|many|other)$")
PROTECTED_ROOT = "auto.components.settings."
PROTECTED_MODULE_RE = re.compile(r"plugin", re.IGNORECASE)
CHROME_PATH_RE = re.compile(r"'(auto\.components\.settings\.[A-Za-z0-9_.]+)'")

# i18next interpolation, nesting, and Trans component tags.
PLACEHOLDER_RE = re.compile(r"\{\{[^}]*\}\}|\$t\([^)]*\)|(?<!\{)\{[A-Za-z_][\w.-]*\}(?!\})")
TAG_RE = re.compile(r"</?[A-Za-z0-9][A-Za-z0-9_-]*\s*/?>")

MAX_CHARACTERS = 8192
SOURCE_LENGTH_FLOOR = 64
SOURCE_LENGTH_MULTIPLIER = 4

# Orca refuses: C0 except LF, DEL and C1, line/paragraph separators, BOM, bidi controls.
FORBIDDEN_CHAR_RE = re.compile(
    "[\u0000-\u0009\u000b-\u001f\u007f-\u009f  ﻿"
    "؜‎‏‪-‮⁦-⁩]"
)
ELISION_RE = re.compile(r"(?<=[A-Za-zÀ-ÿ])'(?=[A-Za-zÀ-ÿ{<“\"«(])")
TRAILING_APOSTROPHE_RE = re.compile(r"\b(po|mo|di|fa|va|sta|da)'(?=[\s.,;:!?)]|$)")


def load_json(path: Path) -> dict:
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, data: object) -> None:
    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    Path(path).write_text(text, encoding="utf-8")


def flatten(catalog: dict, prefix: str = "") -> dict[str, str]:
    """Dotted path -> string for every string leaf, in catalog order."""
    flat: dict[str, str] = {}
    for key, value in catalog.items():
        path = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            flat.update(flatten(value, path))
        elif isinstance(value, str):
            flat[path] = value
    return flat


def unflatten(flat: dict[str, str]) -> dict:
    """Inverse of flatten. Raises ValueError when a path is both a leaf and a container."""
    root: dict = {}
    for path, value in flat.items():
        node = root
        parts = path.split(".")
        for part in parts[:-1]:
            child = node.setdefault(part, {})
            if not isinstance(child, dict):
                raise ValueError(f"path {path} crosses the string at {part}")
            node = child
        if isinstance(node.get(parts[-1]), dict):
            raise ValueError(f"path {path} is also a container")
        node[parts[-1]] = value
    return root


def parse_chrome_paths(typescript_source: str) -> frozenset[str]:
    """Exempt plugin-chrome paths listed in Orca's plugin-translatable-chrome.ts."""
    return frozenset(CHROME_PATH_RE.findall(typescript_source))


class ProtectedCopy:
    """Mirror of Orca's isProtectedPluginTranslationPath."""

    def __init__(self, keys: frozenset[str], prefixes: tuple[str, ...], chrome: frozenset[str]):
        self._keys = keys
        self._prefixes = prefixes
        self._chrome = chrome

    def _is_protected_copy(self, path: str) -> bool:
        if any(path.startswith(prefix) for prefix in self._prefixes):
            return True
        candidate = path
        while candidate:
            if candidate in self._keys or PLURAL_SUFFIX_RE.sub("", candidate) in self._keys:
                return True
            cut = candidate.rfind(".")
            candidate = "" if cut == -1 else candidate[:cut]
        return False

    def is_protected(self, path: str) -> bool:
        if self._is_protected_copy(path):
            return True
        if not path.startswith(PROTECTED_ROOT) or path in self._chrome:
            return False
        return PROTECTED_MODULE_RE.match(path[len(PROTECTED_ROOT):]) is not None


def translatable(english: dict[str, str], protected: ProtectedCopy) -> dict[str, str]:
    """English strings a language pack may translate (non-empty, not protected)."""
    return {k: v for k, v in english.items() if v and not protected.is_protected(k)}


def tokens(text: str) -> Counter:
    """Multiset of placeholders and tags that must survive translation untouched."""
    return Counter(PLACEHOLDER_RE.findall(text)) + Counter(TAG_RE.findall(text))


IDENTIFIER_RE = re.compile(r"[\w.~-]*[/:.][\w./:?=&~-]+")


def prose(text: str) -> str:
    """Text with placeholders, tags, paths, URLs and file names removed, for glossary checks."""
    text = PLACEHOLDER_RE.sub(" ", text)
    text = TAG_RE.sub(" ", text)
    return IDENTIFIER_RE.sub(" ", text)


def length_limit(source: str) -> int:
    return min(MAX_CHARACTERS, max(SOURCE_LENGTH_FLOOR, SOURCE_LENGTH_MULTIPLIER * len(source)))


def edge_whitespace(text: str) -> tuple[str, str]:
    stripped = text.strip()
    if not stripped:
        return text, ""
    start = text.index(stripped[0])
    return text[:start], text[start + len(stripped):]


def string_problems(source: str, target: str) -> list[str]:
    """Hard errors for one translated string. Empty list means the string is acceptable."""
    problems: list[str] = []
    if not target.strip():
        return ["empty translation"]
    if FORBIDDEN_CHAR_RE.search(target):
        problems.append("control or bidirectional character")
    if "\n" in target and "\n" not in source:
        problems.append("adds a line break the English text does not have")
    if target.count("\n") != source.count("\n"):
        problems.append("line break count differs from English")
    if len(target) > length_limit(source):
        problems.append(f"longer than {length_limit(source)} characters")
    if tokens(source) != tokens(target):
        missing = tokens(source) - tokens(target)
        extra = tokens(target) - tokens(source)
        problems.append(f"placeholders/tags differ (missing {sorted(missing)}, extra {sorted(extra)})")
    if edge_whitespace(source) != edge_whitespace(target):
        problems.append("leading/trailing whitespace differs from English")
    if ELISION_RE.search(target) or TRAILING_APOSTROPHE_RE.search(target):
        problems.append("straight apostrophe in Italian text (use ’)")
    return problems


def normalize_typography(source: str, target: str) -> str:
    """Typographic apostrophes; mirror the English choice between … and three dots."""
    text = ELISION_RE.sub("’", target)
    text = TRAILING_APOSTROPHE_RE.sub(lambda m: m.group(1) + "’", text)
    if "…" in source and "..." not in source:
        text = text.replace("...", "…")
    elif "..." in source and "…" not in source:
        text = text.replace("…", "...")
    return text
