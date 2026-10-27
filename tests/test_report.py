"""Tests for src/report.py: layout only, no new judgements or evidence."""

from __future__ import annotations

import re
import unittest

from src.evaluator import evaluate
from src.models import Evidence, EvidenceGrade, Status
from src.parser import load_assessment, parse_cv, parse_job_description
from src.report import NO_EVIDENCE, NONE_LINE, SECTION_TITLES, render_report
from support import FIXTURE_ASSESSMENT, FIXTURE_CV, FIXTURE_JD, assessment, submission


class TestReport(unittest.TestCase):
    def setUp(self) -> None:
        self.job = parse_job_description(FIXTURE_JD)
        self.cv = parse_cv(FIXTURE_CV)
        self.submission = load_assessment(FIXTURE_ASSESSMENT)
        self.report = render_report(evaluate(self.job, self.cv, self.submission))

    def test_all_eight_sections_in_order(self) -> None:
        headings = re.findall(r"^## (.+)$", self.report, flags=re.MULTILINE)
        self.assertEqual(headings, list(SECTION_TITLES))

    def test_every_requirement_id_has_a_row(self) -> None:
        for req in self.job.requirements:
            with self.subTest(req=req.id):
                self.assertRegex(self.report, re.compile(rf"^\| {req.id} \| ", re.MULTILINE))

    def test_score_and_band_shown(self) -> None:
        self.assertIn("**Total score:** 53.8 / 100", self.report)
        self.assertIn("**Fit band:** Weak fit", self.report)

    def test_only_supplied_quotes_appear(self) -> None:
        supplied = {e.quote for a in self.submission.assessments for e in a.evidence}
        rendered = set(re.findall(r"“([^”]+)”", self.report))
        self.assertEqual(rendered, supplied)

    def test_unsupported_row_cites_no_evidence(self) -> None:
        row = next(line for line in self.report.splitlines() if line.startswith("| P2 |"))
        self.assertIn(NO_EVIDENCE, row)
        self.assertNotIn("“", row)

    def test_narrative_reproduced_verbatim(self) -> None:
        self.assertIn(self.submission.positioning, self.report)
        self.assertIn(self.submission.application_brief, self.report)

    def test_no_mandatory_gap_banner_when_none(self) -> None:
        self.assertNotIn("⚠ MANDATORY GAP:", self.report)

    def test_rendering_is_deterministic(self) -> None:
        again = render_report(evaluate(self.job, self.cv, self.submission))
        self.assertEqual(self.report, again)


def _gaps_section(report: str) -> str:
    return report.split("## 4. Genuine gaps", 1)[1].split("## 5.", 1)[0]


def _render_with_unsupported(*unsupported: str) -> str:
    job = parse_job_description(FIXTURE_JD)
    cv = parse_cv(FIXTURE_CV)
    alpha = Evidence("Experience", "Used Tool Alpha daily in production.")
    ids = ("M1", "M2", "M3", "M4", "P1", "P2")
    items = [
        assessment(i, Status.UNSUPPORTED, EvidenceGrade.C) if i in unsupported
        else assessment(i, Status.SUPPORTED, EvidenceGrade.A, (alpha,))
        for i in ids
    ]
    return render_report(evaluate(job, cv, submission(*items)))


class TestNoMandatoryGap(unittest.TestCase):
    """Regression for CODE-1: no gap warning anywhere when no mandatory requirement is UNSUPPORTED."""

    def setUp(self) -> None:
        # A preferred gap must not trigger the mandatory warning either.
        self.report = _render_with_unsupported("P2")

    def test_no_warning_text_anywhere(self) -> None:
        self.assertNotIn("MANDATORY GAP", self.report)

    def test_mandatory_gaps_label_is_plain(self) -> None:
        gaps = _gaps_section(self.report)
        self.assertIn("**Mandatory:**\n\n_None._", gaps)

    def test_preferred_gap_still_listed(self) -> None:
        self.assertIn("- **P2** — Experience with Tool Zeta.", _gaps_section(self.report))

    def test_fixture_report_has_no_warning_text(self) -> None:
        job = parse_job_description(FIXTURE_JD)
        cv = parse_cv(FIXTURE_CV)
        report = render_report(evaluate(job, cv, load_assessment(FIXTURE_ASSESSMENT)))
        self.assertNotIn("MANDATORY GAP", report)


class TestMandatoryGapMarking(unittest.TestCase):
    def setUp(self) -> None:
        self.report = _render_with_unsupported("M2")

    def test_banner_names_the_gap(self) -> None:
        self.assertIn("> **⚠ MANDATORY GAP:** unsupported mandatory requirement(s): M2.", self.report)

    def test_row_is_marked(self) -> None:
        row = next(line for line in self.report.splitlines() if line.startswith("| M2 |"))
        self.assertIn("**UNSUPPORTED** ⚠ MANDATORY GAP", row)

    def test_gap_listed_in_genuine_gaps(self) -> None:
        gaps = _gaps_section(self.report)
        self.assertIn("**Mandatory (⚠ MANDATORY GAP):**", gaps)
        self.assertIn("- **M2** — Experience with Tool Beta.", gaps)

    def test_only_the_gap_row_is_marked(self) -> None:
        marked = [line for line in self.report.splitlines() if line.startswith("| ") and "MANDATORY GAP" in line]
        self.assertEqual([line.split(" | ", 1)[0] for line in marked], ["| M2"])


class TestMultipleMandatoryGaps(unittest.TestCase):
    def setUp(self) -> None:
        self.report = _render_with_unsupported("M2", "M4")

    def test_banner_names_every_gap(self) -> None:
        self.assertIn("> **⚠ MANDATORY GAP:** unsupported mandatory requirement(s): M2, M4.", self.report)

    def test_every_gap_row_is_marked(self) -> None:
        for req_id in ("M2", "M4"):
            with self.subTest(req=req_id):
                row = next(line for line in self.report.splitlines() if line.startswith(f"| {req_id} |"))
                self.assertIn("**UNSUPPORTED** ⚠ MANDATORY GAP", row)

    def test_gaps_section_labelled_once_and_lists_all(self) -> None:
        gaps = _gaps_section(self.report)
        self.assertEqual(gaps.count("**Mandatory (⚠ MANDATORY GAP):**"), 1)
        self.assertIn("- **M2** — Experience with Tool Beta.", gaps)
        self.assertIn("- **M4** — Experience with Tool Delta.", gaps)
        self.assertNotIn(NONE_LINE, gaps.split("**Preferred:**", 1)[0])

    def test_pipe_in_text_is_escaped(self) -> None:
        job = parse_job_description(FIXTURE_JD)
        cv = parse_cv(FIXTURE_CV)
        alpha = Evidence("Experience", "Used Tool Alpha daily in production.")
        items = [assessment(i, Status.SUPPORTED, EvidenceGrade.A, (alpha,)) for i in ("M2", "M3", "M4", "P1", "P2")]
        piped = assessment("M1", Status.SUPPORTED, EvidenceGrade.A, (alpha,))
        items.append(piped.__class__(**{**piped.__dict__, "rationale": "a | b\nc"}))
        report = render_report(evaluate(job, cv, submission(*items)))
        row = next(line for line in report.splitlines() if line.startswith("| M1 |"))
        self.assertIn("a \\| b<br>c", row)


if __name__ == "__main__":
    unittest.main()
