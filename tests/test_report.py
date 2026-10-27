"""Tests for src/report.py: layout only, no new judgements or evidence."""

from __future__ import annotations

import re
import unittest

from src.evaluator import evaluate
from src.models import Evidence, EvidenceGrade, Status
from src.parser import load_assessment, parse_cv, parse_job_description
from src.report import NO_EVIDENCE, SECTION_TITLES, render_report
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


class TestMandatoryGapMarking(unittest.TestCase):
    def setUp(self) -> None:
        job = parse_job_description(FIXTURE_JD)
        cv = parse_cv(FIXTURE_CV)
        alpha = Evidence("Experience", "Used Tool Alpha daily in production.")
        items = [assessment(i, Status.SUPPORTED, EvidenceGrade.A, (alpha,)) for i in ("M1", "M3", "M4", "P1", "P2")]
        items.append(assessment("M2", Status.UNSUPPORTED, EvidenceGrade.C))
        self.report = render_report(evaluate(job, cv, submission(*items)))

    def test_banner_names_the_gap(self) -> None:
        self.assertIn("> **⚠ MANDATORY GAP:** unsupported mandatory requirement(s): M2.", self.report)

    def test_row_is_marked(self) -> None:
        row = next(line for line in self.report.splitlines() if line.startswith("| M2 |"))
        self.assertIn("**UNSUPPORTED** ⚠ MANDATORY GAP", row)

    def test_gap_listed_in_genuine_gaps(self) -> None:
        gaps = self.report.split("## 4. Genuine gaps", 1)[1].split("## 5.", 1)[0]
        self.assertIn("- **M2** — Experience with Tool Beta.", gaps)

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
