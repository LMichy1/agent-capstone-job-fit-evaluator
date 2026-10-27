"""Guards for the architectural boundary: stdlib only, no network or model clients."""

from __future__ import annotations

import ast
import sys
import unittest

from support import ROOT

FRAMEWORK_FILES = sorted((ROOT / "src").glob("*.py")) + [ROOT / "scripts" / "run_evaluation.py"]


def imported_modules(path) -> set[str]:  # type: ignore[no-untyped-def]
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            names.add(node.module.split(".")[0])
    return names


class TestBoundaries(unittest.TestCase):
    def test_framework_imports_only_stdlib_and_itself(self) -> None:
        for path in FRAMEWORK_FILES:
            with self.subTest(file=path.name):
                third_party = imported_modules(path) - set(sys.stdlib_module_names) - {"src", "__future__"}
                self.assertEqual(third_party, set())

    def test_no_network_or_subprocess_modules(self) -> None:
        forbidden = {"socket", "http", "urllib", "subprocess", "requests", "anthropic", "openai"}
        for path in FRAMEWORK_FILES:
            with self.subTest(file=path.name):
                self.assertEqual(imported_modules(path) & forbidden, set())

    def test_framework_sources_parse_as_python_310(self) -> None:
        for path in FRAMEWORK_FILES:
            with self.subTest(file=path.name):
                ast.parse(path.read_text(encoding="utf-8"), feature_version=(3, 10))


if __name__ == "__main__":
    unittest.main()
