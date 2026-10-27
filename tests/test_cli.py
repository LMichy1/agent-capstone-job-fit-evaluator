"""End-to-end tests for scripts/run_evaluation.py, run as a subprocess."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from support import CONTEXT, FIXTURE_ASSESSMENT, FIXTURE_CV, FIXTURE_JD, MALFORMED_ASSESSMENT, ROOT

SCRIPT = ROOT / "scripts" / "run_evaluation.py"


def run_cli(*args: str | Path, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *map(str, args)], capture_output=True, text=True, cwd=cwd, check=False
    )


def fixture_args(assessment: Path = FIXTURE_ASSESSMENT) -> list[str | Path]:
    return ["--job", FIXTURE_JD, "--cv", FIXTURE_CV, "--assessment", assessment]


class TestCLI(unittest.TestCase):
    def test_prints_report(self) -> None:
        result = run_cli(*fixture_args(), "--standard", CONTEXT / "evaluation_standard.md")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("**Total score:** 53.8 / 100", result.stdout)

    def test_writes_report_from_any_working_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "report.md"
            result = run_cli(*fixture_args(), "--output", output, cwd=Path(tmp))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("total 53.8, Weak fit", result.stdout)
            self.assertTrue(output.read_text(encoding="utf-8").startswith("# Job Fit Assessment — Fixture Candidate"))

    def test_malformed_assessment_fails_with_every_error(self) -> None:
        result = run_cli(*fixture_args(MALFORMED_ASSESSMENT))
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        for expected in ("MOSTLY_SUPPORTED", "invalid evidence_grade 'E'", "unknown field 'evidense'"):
            self.assertIn(expected, result.stderr)

    def test_semantic_validation_failures_exit_nonzero(self) -> None:
        # Structurally valid JSON whose fabricated quote, unknown ID and missing items fail evaluation.
        text = MALFORMED_ASSESSMENT.read_text(encoding="utf-8")
        text = text.replace('"MOSTLY_SUPPORTED"', '"SUPPORTED"').replace('"E"', '"B"').replace('"evidense"', '"evidence"')
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "assessment.json"
            path.write_text(text, encoding="utf-8")
            result = run_cli(*fixture_args(path))
        self.assertEqual(result.returncode, 1)
        for expected in ("quote not found verbatim", "M9: unknown requirement ID", "M3: missing assessment",
                         "requires a verification_question"):
            self.assertIn(expected, result.stderr)

    def test_missing_input_file_fails(self) -> None:
        result = run_cli("--job", "absent.md", "--cv", FIXTURE_CV, "--assessment", FIXTURE_ASSESSMENT)
        self.assertEqual(result.returncode, 1)
        self.assertIn("File not found", result.stderr)

    def test_missing_argument_is_usage_error(self) -> None:
        result = run_cli("--job", FIXTURE_JD)
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
