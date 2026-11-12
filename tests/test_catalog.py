import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import catalog  # noqa: E402
import packtool  # noqa: E402


class FlattenTest(unittest.TestCase):
    def test_round_trip_keeps_order_and_values(self):
        nested = {"a": {"b": "one", "c": {"d": "two"}}, "e": "three"}
        flat = catalog.flatten(nested)
        self.assertEqual(list(flat), ["a.b", "a.c.d", "e"])
        self.assertEqual(catalog.unflatten(flat), nested)

    def test_non_string_leaves_are_ignored(self):
        self.assertEqual(catalog.flatten({"a": 1, "b": ["x"], "c": "ok"}), {"c": "ok"})

    def test_unflatten_rejects_leaf_and_container_clash(self):
        with self.assertRaises(ValueError):
            catalog.unflatten({"a": "x", "a.b": "y"})
        with self.assertRaises(ValueError):
            catalog.unflatten({"a.b": "y", "a": "x"})


class ProtectedCopyTest(unittest.TestCase):
    def setUp(self):
        self.protected = catalog.ProtectedCopy(
            frozenset({"dialogs.delete", "trust.count"}),
            ("native.",),
            frozenset({"auto.components.settings.PluginsSettingsSection.title"}),
        )

    def test_exact_child_and_plural_of_protected_key(self):
        self.assertTrue(self.protected.is_protected("dialogs.delete"))
        self.assertTrue(self.protected.is_protected("dialogs.delete.confirm"))
        self.assertTrue(self.protected.is_protected("trust.count_other"))
        self.assertFalse(self.protected.is_protected("dialogs.deleted"))

    def test_prefix(self):
        self.assertTrue(self.protected.is_protected("native.quit"))

    def test_plugin_settings_namespace_is_protected_except_chrome(self):
        root = "auto.components.settings."
        self.assertTrue(self.protected.is_protected(root + "PluginRemoveDialog.title"))
        self.assertTrue(self.protected.is_protected(root + "plugins.search.logs"))
        self.assertFalse(self.protected.is_protected(root + "PluginsSettingsSection.title"))
        self.assertFalse(self.protected.is_protected(root + "TerminalPane.title"))

    def test_translatable_drops_empty_and_protected(self):
        english = {"a": "A", "b": "", "native.x": "X"}
        self.assertEqual(catalog.translatable(english, self.protected), {"a": "A"})

    def test_parse_chrome_paths(self):
        source = "new Set([\n 'auto.components.settings.PluginsSettingsSection.title',\n 'other']"
        self.assertEqual(
            catalog.parse_chrome_paths(source),
            frozenset({"auto.components.settings.PluginsSettingsSection.title"}),
        )


class StringProblemsTest(unittest.TestCase):
    def assert_problem(self, source, target, fragment):
        problems = catalog.string_problems(source, target)
        self.assertTrue(any(fragment in p for p in problems), problems)

    def test_clean_translation_has_no_problems(self):
        self.assertEqual(
            catalog.string_problems("Open <0>{{name}}</0> now…", "Apri <0>{{name}}</0> ora…"), []
        )

    def test_empty(self):
        self.assert_problem("Save", "  ", "empty")

    def test_placeholder_renamed_or_dropped(self):
        self.assert_problem("Hi {{name}}", "Ciao {{nome}}", "placeholders/tags differ")
        self.assert_problem("Hi {{name}}", "Ciao", "placeholders/tags differ")

    def test_tag_renamed(self):
        self.assert_problem("From <file>{{s}}</file>", "Da <source>{{s}}</source>", "placeholders/tags")

    def test_nesting_reference_must_survive(self):
        self.assert_problem("See $t(common.docs)", "Vedi la documentazione", "placeholders/tags")

    def test_added_line_break(self):
        self.assert_problem("One line", "Una\nriga", "adds a line break")

    def test_line_break_count(self):
        self.assert_problem("a\nb\nc", "a\nb c", "line break count")

    def test_length_limit_uses_floor_and_multiplier(self):
        self.assertEqual(catalog.length_limit("Retry"), 64)
        self.assertEqual(catalog.length_limit("x" * 100), 400)
        self.assertEqual(catalog.length_limit("x" * 5000), 8192)
        self.assert_problem("Retry", "r" * 65, "longer than 64")

    def test_forbidden_characters(self):
        self.assert_problem("Tab", "Sche\tda", "control")
        self.assert_problem("Name", "No‮me", "control")

    def test_edge_whitespace_must_match(self):
        self.assert_problem("Path: ", "Percorso:", "whitespace")
        self.assertEqual(catalog.string_problems(" and ", " e "), [])

    def test_straight_apostrophe_is_flagged(self):
        self.assert_problem("The host", "L'host", "straight apostrophe")
        self.assert_problem("A bit", "Un po' meno", "straight apostrophe")
        self.assertEqual(catalog.string_problems("The host", "L’host"), [])


class TypographyTest(unittest.TestCase):
    def test_elision_becomes_typographic(self):
        self.assertEqual(catalog.normalize_typography("x", "l'host e un po' d'aria"), "l’host e un po’ d’aria")

    def test_elision_before_placeholder(self):
        self.assertEqual(catalog.normalize_typography("x", "dell'{{name}}"), "dell’{{name}}")

    def test_quoted_code_is_left_alone(self):
        self.assertEqual(catalog.normalize_typography("x", "usa 'main' qui"), "usa 'main' qui")

    def test_ellipsis_mirrors_english(self):
        self.assertEqual(catalog.normalize_typography("Loading…", "Caricamento..."), "Caricamento…")
        self.assertEqual(catalog.normalize_typography("Loading...", "Caricamento…"), "Caricamento...")
        self.assertEqual(catalog.normalize_typography("Done", "Fatto..."), "Fatto...")


class PackToolTest(unittest.TestCase):
    def test_pending_lists_missing_keys(self):
        english = {"a": "A", "b": "B"}
        self.assertEqual(packtool.pending_keys(english, {"a": "x"}, None), ["b"])

    def test_pending_requeues_changed_english(self):
        english = {"a": "A2", "b": "B", "c": "C"}
        previous = {"a": "A", "b": "B"}
        pack = {"a": "x", "b": "y", "c": "z"}
        self.assertEqual(packtool.pending_keys(english, pack, previous), ["a"])

    def test_split_chunks_respects_item_and_size_caps(self):
        items = [{"id": i, "key": f"k{i}", "en": "x" * 100} for i in range(700)]
        chunks = packtool.split_chunks(items)
        self.assertEqual(sum(len(c) for c in chunks), 700)
        self.assertTrue(all(len(c) <= packtool.CHUNK_MAX_ITEMS for c in chunks))
        self.assertTrue(
            all(sum(len(i["en"]) + 20 for i in c) <= packtool.CHUNK_MAX_CHARS for c in chunks)
        )

    def test_lint_forbid_and_expect(self):
        rules = [
            {"forbid": r"spazi?o? di lavoro", "message": "use area di lavoro"},
            {"when": r"\bworktrees?\b", "expect": r"worktree", "message": "keep worktree"},
        ]
        self.assertEqual(
            packtool.lint_warnings("k", "Open workspace", "Apri spazio di lavoro", rules),
            ["use area di lavoro"],
        )
        self.assertEqual(
            packtool.lint_warnings("k", "New worktree", "Nuovo albero", rules), ["keep worktree"]
        )
        self.assertEqual(packtool.lint_warnings("k", "New worktree", "Nuovo worktree", rules), [])

    def test_lint_ignores_placeholder_names(self):
        rules = [{"forbid": r"\\bshortcut\\b", "message": "shortcut"}]
        self.assertEqual(packtool.lint_warnings("k", "x", "{{shortcut}} per inviare.", rules), [])

    def test_lint_case_sensitive_rule(self):
        rules = [{"forbid": r"\bLei\b", "caseSensitive": True, "message": "tu"}]
        self.assertEqual(packtool.lint_warnings("k", "x", "Scegli lei o lui", rules), [])
        self.assertEqual(packtool.lint_warnings("k", "x", "Lei può", rules), ["tu"])

    def test_lint_ignores_tags_paths_and_placeholder_only_terms(self):
        rules = [
            {"forbid": r"\bshortcut\b|\bkeybinding|\bsidebar\b", "message": "f"},
            {"when": r"\bbranch\b", "expect": "branch", "message": "e"},
        ]
        self.assertEqual(packtool.lint_warnings("k", "x", "Vai con <shortcut/>", rules), [])
        self.assertEqual(packtool.lint_warnings("k", "x", "Apri ~/.orca/keybindings.json", rules), [])
        self.assertEqual(packtool.lint_warnings("k", "x", "{sidebar.toggle} apre", rules), [])
        self.assertEqual(packtool.lint_warnings("k", "On {{branch}}", "Su {{branch}}", rules), [])
        self.assertEqual(packtool.lint_warnings("k", "On branch x", "Sul ramo x", rules), ["e"])

    def test_single_brace_placeholder_must_survive(self):
        problems = catalog.string_problems("Open {host} now", "Apri ora")
        self.assertTrue(any("placeholders" in p for p in problems))
        self.assertEqual(catalog.string_problems("Open {host} now", "Apri {host} ora"), [])

    def test_report_flags_missing_stale_and_honours_exceptions(self):
        wanted = {"a": "Hi {{n}}", "b": "<question>", "c": "C"}
        pack = {"a": "Ciao", "b": "<domanda>", "old": "x"}
        errors, _ = packtool.collect_report(wanted, pack, [], {"b": ["placeholders/tags"]})
        self.assertEqual(len(errors), 3)
        self.assertTrue(any(e.startswith("old:") for e in errors))
        self.assertTrue(any(e.startswith("c: missing") for e in errors))
        self.assertTrue(any(e.startswith("a: placeholders") for e in errors))

    def test_chunk_errors_cover_missing_extra_and_string_rules(self):
        items = [
            {"id": 0, "key": "a", "en": "Hi {{n}}"},
            {"id": 1, "key": "b", "en": "The host"},
            {"id": 2, "key": "c", "en": "Save"},
        ]
        answers = {"0": "Ciao", "1": "L'host", "9": "x"}
        errors = packtool.chunk_errors(items, answers, [])
        self.assertEqual(len(errors), 3)
        self.assertTrue(any("id 9" in e for e in errors))
        self.assertTrue(any("id 0: placeholders" in e for e in errors))
        self.assertTrue(any("id 2: missing" in e for e in errors))

    def test_bad_version_is_a_tool_error(self):
        with self.assertRaises(packtool.ToolError):
            packtool.source_dir("../etc")


if __name__ == "__main__":
    unittest.main()
