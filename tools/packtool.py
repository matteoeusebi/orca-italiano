#!/usr/bin/env python3
"""Maintenance tool for the Italian Orca language pack.

  fetch   <version>            download Orca's English catalog and protected-copy rules
  pending <version> [--old V]  write chunks of strings that still need translating
  merge   <version>            fold translated chunks into locales/it.json
  check   <version>            verify locales/it.json against the English catalog
  chunk   <number>             verify one translated chunk (.work/out/NNN.json)

Standard library only. Run from the repository root.
"""

from __future__ import annotations

import argparse
import re
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import catalog  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PACK_PATH = ROOT / "locales" / "it.json"
CACHE_DIR = ROOT / ".cache"
WORK_DIR = ROOT / ".work"
LINT_PATH = ROOT / "tools" / "glossary_lint.json"
EXCEPTIONS_PATH = ROOT / "tools" / "exceptions.json"
RAW_BASE = "https://raw.githubusercontent.com/stablyai/orca"
SOURCE_FILES = {
    "en.json": "src/renderer/src/i18n/locales/en.json",
    "protected-copy-keys.json": "src/shared/plugins/languages/protected-copy-keys.json",
    "plugin-translatable-chrome.ts": "src/shared/plugins/languages/plugin-translatable-chrome.ts",
}
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")
CHUNK_MAX_ITEMS = 320
CHUNK_MAX_CHARS = 22_000


class ToolError(Exception):
    """A problem the user can act on; printed without a traceback."""


def source_dir(version: str) -> Path:
    if not VERSION_RE.match(version):
        raise ToolError(f"version must look like 1.4.257, got {version!r}")
    return CACHE_DIR / version


def fetch(version: str) -> Path:
    target = source_dir(version)
    target.mkdir(parents=True, exist_ok=True)
    for name, repo_path in SOURCE_FILES.items():
        destination = target / name
        if destination.exists():
            continue
        url = f"{RAW_BASE}/v{version}/{repo_path}"
        try:
            with urllib.request.urlopen(url, timeout=60) as response:
                destination.write_bytes(response.read())
        except OSError as error:
            raise ToolError(f"could not download {url}: {error}") from error
    return target


def load_source(version: str) -> tuple[dict[str, str], catalog.ProtectedCopy]:
    folder = source_dir(version)
    if not (folder / "en.json").exists():
        raise ToolError(f"no cached source for {version}; run: packtool.py fetch {version}")
    keys = catalog.load_json(folder / "protected-copy-keys.json")
    chrome = catalog.parse_chrome_paths(
        (folder / "plugin-translatable-chrome.ts").read_text(encoding="utf-8")
    )
    protected = catalog.ProtectedCopy(
        frozenset(keys["keys"]), tuple(keys["prefixes"]), chrome
    )
    return catalog.flatten(catalog.load_json(folder / "en.json")), protected


def load_pack() -> dict[str, str]:
    return catalog.flatten(catalog.load_json(PACK_PATH)) if PACK_PATH.exists() else {}


def pending_keys(
    english: dict[str, str], pack: dict[str, str], previous: dict[str, str] | None
) -> list[str]:
    """Keys with no translation yet, or whose English text changed since `previous`."""
    changed = previous is not None
    return [
        key
        for key, text in english.items()
        if key not in pack or (changed and key in previous and previous[key] != text)
    ]


def split_chunks(items: list[dict]) -> list[list[dict]]:
    chunks: list[list[dict]] = []
    current: list[dict] = []
    size = 0
    for item in items:
        cost = len(item["en"]) + 20
        if current and (len(current) >= CHUNK_MAX_ITEMS or size + cost > CHUNK_MAX_CHARS):
            chunks.append(current)
            current, size = [], 0
        current.append(item)
        size += cost
    if current:
        chunks.append(current)
    return chunks


def cmd_fetch(args: argparse.Namespace) -> int:
    print(f"source cached in {fetch(args.version)}")
    return 0


def cmd_pending(args: argparse.Namespace) -> int:
    fetch(args.version)
    english, protected = load_source(args.version)
    wanted = catalog.translatable(english, protected)
    previous = None
    if args.old:
        fetch(args.old)
        previous = load_source(args.old)[0]
    keys = pending_keys(wanted, load_pack(), previous)
    in_dir = WORK_DIR / "in"
    in_dir.mkdir(parents=True, exist_ok=True)
    (WORK_DIR / "out").mkdir(parents=True, exist_ok=True)
    for stale in in_dir.glob("*.json"):
        stale.unlink()
    items = [{"id": index, "key": key, "en": wanted[key]} for index, key in enumerate(keys)]
    chunks = split_chunks(items)
    for number, chunk in enumerate(chunks):
        catalog.write_json(in_dir / f"{number:03d}.json", chunk)
    print(f"{len(keys)} strings to translate in {len(chunks)} chunks under {in_dir}")
    return 0


def read_translations() -> dict[str, str]:
    """key -> Italian from every .work/out chunk, matched to its .work/in chunk by id."""
    translated: dict[str, str] = {}
    for in_path in sorted((WORK_DIR / "in").glob("*.json")):
        out_path = WORK_DIR / "out" / in_path.name
        if not out_path.exists():
            print(f"warning: {out_path.name} not translated yet", file=sys.stderr)
            continue
        answers = catalog.load_json(out_path)
        for item in catalog.load_json(in_path):
            answer = answers.get(str(item["id"]))
            if isinstance(answer, str) and answer.strip():
                translated[item["key"]] = answer
            else:
                print(f"warning: {in_path.name} id {item['id']} missing", file=sys.stderr)
    return translated


def cmd_merge(args: argparse.Namespace) -> int:
    english, protected = load_source(args.version)
    wanted = catalog.translatable(english, protected)
    merged = {**load_pack(), **read_translations()}
    ordered = {
        key: catalog.normalize_typography(wanted[key], merged[key])
        for key in wanted
        if key in merged
    }
    dropped = len(merged) - len(ordered)
    PACK_PATH.parent.mkdir(parents=True, exist_ok=True)
    catalog.write_json(PACK_PATH, catalog.unflatten(ordered))
    print(f"{len(ordered)}/{len(wanted)} strings in {PACK_PATH} ({dropped} stale or protected dropped)")
    return 0


def lint_warnings(key: str, source: str, target: str, rules: list[dict]) -> list[str]:
    """Glossary rules: `forbid` a pattern in Italian, or `expect` one when English matches `when`."""
    warnings: list[str] = []
    # Placeholder names, tags, paths and URLs are identifiers, not prose.
    source, target = catalog.prose(source), catalog.prose(target)
    for rule in rules:
        flags = 0 if rule.get("caseSensitive") else re.IGNORECASE
        if "when" in rule and not re.search(rule["when"], source, re.IGNORECASE):
            continue
        if "forbid" in rule and re.search(rule["forbid"], target, flags):
            warnings.append(rule["message"])
        if "expect" in rule and not re.search(rule["expect"], target, re.IGNORECASE):
            warnings.append(rule["message"])
    return warnings


def collect_report(
    wanted: dict[str, str], pack: dict[str, str], rules: list[dict], exceptions: dict
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    for key in pack:
        if key not in wanted:
            errors.append(f"{key}: not a translatable English key (stale or protected)")
    for key, source in wanted.items():
        if key not in pack:
            errors.append(f"{key}: missing")
            continue
        allowed = exceptions.get(key, [])
        for problem in catalog.string_problems(source, pack[key]):
            if not any(problem.startswith(prefix) for prefix in allowed):
                errors.append(f"{key}: {problem}")
        warnings.extend(f"{key}: {text}" for text in lint_warnings(key, source, pack[key], rules))
    return errors, warnings


def cmd_check(args: argparse.Namespace) -> int:
    english, protected = load_source(args.version)
    wanted = catalog.translatable(english, protected)
    rules = catalog.load_json(LINT_PATH) if LINT_PATH.exists() else []
    exceptions = catalog.load_json(EXCEPTIONS_PATH) if EXCEPTIONS_PATH.exists() else {}
    pack = load_pack()
    errors, warnings = collect_report(wanted, pack, rules, exceptions)
    for line in errors:
        print(f"ERROR {line}")
    if args.warnings:
        for line in warnings:
            print(f"WARN  {line}")
    covered = sum(1 for key in wanted if key in pack)
    print(
        f"coverage {covered}/{len(wanted)} ({covered * 100 // max(len(wanted), 1)}%), "
        f"{len(errors)} errors, {len(warnings)} glossary warnings"
    )
    return 1 if errors else 0


def chunk_errors(items: list[dict], answers: dict, rules: list[dict]) -> list[str]:
    """Problems in one translated chunk; glossary warnings are reported as errors to fix."""
    errors: list[str] = []
    known = {str(item["id"]) for item in items}
    errors.extend(f"id {extra}: not in the input chunk" for extra in answers if extra not in known)
    for item in items:
        answer = answers.get(str(item["id"]))
        if not isinstance(answer, str):
            errors.append(f"id {item['id']}: missing")
            continue
        fixed = catalog.normalize_typography(item["en"], answer)
        problems = catalog.string_problems(item["en"], fixed)
        problems += lint_warnings(item["key"], item["en"], fixed, rules)
        errors.extend(f"id {item['id']}: {problem}" for problem in problems)
    return errors


def cmd_chunk(args: argparse.Namespace) -> int:
    name = f"{int(args.number):03d}.json"
    in_path, out_path = WORK_DIR / "in" / name, WORK_DIR / "out" / name
    if not in_path.exists() or not out_path.exists():
        raise ToolError(f"need both {in_path} and {out_path}")
    try:
        answers = catalog.load_json(out_path)
    except ValueError as error:
        raise ToolError(f"{out_path} is not valid JSON: {error}") from error
    rules = catalog.load_json(LINT_PATH) if LINT_PATH.exists() else []
    errors = chunk_errors(catalog.load_json(in_path), answers, rules)
    for line in errors:
        print(line)
    print(f"chunk {name}: {len(errors)} problems")
    return 1 if errors else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True)
    for name, handler in (("fetch", cmd_fetch), ("pending", cmd_pending), ("merge", cmd_merge), ("check", cmd_check)):
        sub = commands.add_parser(name)
        sub.add_argument("version", help="Orca version, e.g. 1.4.257")
        sub.set_defaults(handler=handler)
        if name == "pending":
            sub.add_argument("--old", help="version the pack was last aligned to; changed English text is re-queued")
        if name == "check":
            sub.add_argument("--warnings", action="store_true", help="also print glossary warnings")
    chunk = commands.add_parser("chunk")
    chunk.add_argument("number", help="chunk number, e.g. 7")
    chunk.set_defaults(handler=cmd_chunk)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.handler(args)
    except ToolError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
