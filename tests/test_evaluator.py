"""Tests for src/evaluator.py: validation of supplied judgements and scoring."""

from __future__ import annotations

import re
import tempfile
import unittest
from decimal import ROUND_HALF_EVEN, Decimal
from fractions import Fraction
from pathlib import Path

from src.evaluator import (
    GRADE_VALUE,
    _resolve_location,
    STATUS_CREDIT,
    calculate_score,
    check_score_bounds,
    check_standard_consistency,
    evaluate,
    fit_band,
    round_total,
)
from src.models import (
    AssessmentValidationError,
    Evidence,
    EvidenceGrade,
    FitBand,
    Requirement,
    RequirementOrigin,
    RequirementType,
    ScoreBreakdown,
    ScoringError,
    Status,
)
from src.parser import load_assessment, parse_cv, parse_job_description
from support import CONTEXT, FIXTURE_ASSESSMENT, FIXTURE_CV, FIXTURE_JD, assessment, requirement, submission

S, P, U, X = Status.SUPPORTED, Status.PARTIALLY_SUPPORTED, Status.UNSUPPORTED, Status.UNCLEAR
A, B, C = EvidenceGrade.A, EvidenceGrade.B, EvidenceGrade.C


def score(spec: list[tuple[str, Status, EvidenceGrade]]) -> ScoreBreakdown:
    reqs = tuple(requirement(req_id) for req_id, _, _ in spec)
    return calculate_score(reqs, tuple(assessment(req_id, st, gr) for req_id, st, gr in spec))


class TestCreditTables(unittest.TestCase):
    def test_status_credit(self) -> None:
        self.assertEqual(STATUS_CREDIT, {S: 1, P: Fraction(1, 2), X: 0, U: 0})

    def test_unclear_earns_no_credit(self) -> None:
        self.assertEqual(STATUS_CREDIT[X], STATUS_CREDIT[U])

    def test_grade_values(self) -> None:
        self.assertEqual(GRADE_VALUE, {A: 1, B: Fraction(1, 2), C: 0})

    def test_constants_match_current_standard(self) -> None:
        check_standard_consistency(CONTEXT / "evaluation_standard.md")  # must not raise

    def test_worked_example_total_in_standard_matches_evaluator(self) -> None:
        text = (CONTEXT / "evaluation_standard.md").read_text(encoding="utf-8")
        example = text.split("### Worked example", 1)[1].split("\n## ", 1)[0]
        stated = re.search(r"→ \*\*(\d+\.\d), (\w+ fit)\*\*", example)
        self.assertIsNotNone(stated)
        result = score([("M1", S, A), ("M2", S, A), ("M3", P, B), ("M4", X, C), ("P1", P, B), ("P2", U, C)])
        self.assertEqual((float(stated.group(1)), stated.group(2)), (result.total, result.band.value))

    def test_standard_citation_example_locations_exist_in_candidate_cv(self) -> None:
        text = (CONTEXT / "evaluation_standard.md").read_text(encoding="utf-8")
        citation_rules = text.split("## 4. Evidence citation", 1)[1].split("\n## ", 1)[0]
        example_text = re.split(r"Matching\s+is\s+exact", citation_rules.split("For example:", 1)[1], maxsplit=1)[0]
        examples = re.findall(r"`([^`]+)`", example_text)
        self.assertEqual(len(examples), 2)
        cv = parse_cv(CONTEXT / "candidate_cv.md")
        for location in examples:
            with self.subTest(location=location):
                self.assertIsNotNone(_resolve_location(location, cv))

    def test_standard_drift_is_detected(self) -> None:
        text = (CONTEXT / "evaluation_standard.md").read_text(encoding="utf-8")
        drifted = text.replace("| Mandatory requirements        | 70     |", "| Mandatory requirements        | 60     |")
        self.assertNotEqual(text, drifted)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "standard.md"
            path.write_text(drifted, encoding="utf-8")
            with self.assertRaisesRegex(ScoringError, "60 in the standard but 70.0"):
                check_standard_consistency(path)


class TestScoring(unittest.TestCase):
    def test_components_and_total(self) -> None:
        result = score([("M1", S, A), ("M2", P, B), ("P1", S, A), ("P2", U, C)])
        self.assertAlmostEqual(result.mandatory_score, 70 * 0.75)
        self.assertAlmostEqual(result.preferred_score, 20 * 0.5)
        self.assertAlmostEqual(result.confidence_score, 10 * (2.5 / 4))
        self.assertEqual(result.total, 68.8)  # 52.5 + 10 + 6.25 = 68.75 -> half-up
        self.assertEqual(result.band, FitBand.MODERATE)

    def test_worked_example_inputs_from_standard(self) -> None:
        """Statuses and grades from the worked example in section 6 of evaluation_standard.md.

        Grades A, A, B, C, B, C sum to 3.0, so the total is 43.75 + 5.0 + 5.0 = 53.75 -> 53.8.
        (Before the Milestone 2 context correction the standard stated 2.0 and 52.1.)
        """
        result = score([("M1", S, A), ("M2", S, A), ("M3", P, B), ("M4", X, C), ("P1", P, B), ("P2", U, C)])
        self.assertEqual(result.mandatory_score, 43.75)
        self.assertEqual(result.preferred_score, 5.0)
        self.assertEqual(result.confidence_score, 5.0)
        self.assertEqual(result.total, 53.8)
        self.assertEqual(result.band, FitBand.WEAK)

    def test_all_supported_grade_a_is_exactly_100(self) -> None:
        result = score([("M1", S, A), ("M2", S, A), ("P1", S, A)])
        self.assertEqual(result.total, 100.0)
        self.assertEqual(result.band, FitBand.STRONG)

    def test_all_unsupported_is_exactly_zero(self) -> None:
        result = score([("M1", U, C), ("P1", U, C)])
        self.assertEqual(result.total, 0.0)
        self.assertEqual(result.band, FitBand.WEAK)

    def test_zero_preferred_requirements_uses_mandatory_weight_90(self) -> None:
        result = score([("M1", S, A), ("M2", P, B)])
        self.assertEqual((result.mandatory_weight, result.preferred_weight), (90, 0))
        self.assertAlmostEqual(result.mandatory_score, 90 * 0.75)
        self.assertEqual(result.preferred_score, 0.0)
        self.assertEqual(result.total, 75.0)  # 67.5 + 7.5

    def test_zero_mandatory_requirements_fails(self) -> None:
        with self.assertRaisesRegex(ScoringError, "no mandatory requirements"):
            score([("P1", S, A)])

    def test_misaligned_assessments_fail(self) -> None:
        with self.assertRaisesRegex(ScoringError, "align"):
            calculate_score((requirement("M1"),), (assessment("M2"),))

    def test_only_total_is_rounded(self) -> None:
        # Components keep full precision; 70 * 2/3 = 46.666...
        result = score([("M1", S, A), ("M2", S, A), ("M3", U, C), ("P1", U, C)])
        self.assertAlmostEqual(result.mandatory_score, 140 / 3)
        self.assertEqual(result.total, 51.7)  # 46.667 + 0 + 5.0 = 51.667

    def test_round_half_up(self) -> None:
        self.assertEqual(round_total(Fraction(5375, 100)), Decimal("53.8"))
        self.assertEqual(round_total(Fraction(5365, 100)), Decimal("53.7"))  # not banker's rounding
        self.assertEqual(round_total(Fraction(6125, 100)), Decimal("61.3"))

    def test_half_up_differs_from_half_even_on_ties_after_an_even_digit(self) -> None:
        for exact, expected in [("53.65", "53.7"), ("56.25", "56.3"), ("61.25", "61.3"), ("0.05", "0.1")]:
            with self.subTest(exact=exact):
                value = Fraction(exact)
                half_even = Decimal(exact).quantize(Decimal("0.1"), rounding=ROUND_HALF_EVEN)
                self.assertNotEqual(half_even, Decimal(expected))  # the case discriminates
                self.assertEqual(round_total(value), Decimal(expected))

    def test_non_tie_values_round_to_nearest(self) -> None:
        self.assertEqual(round_total(Fraction(5374, 100)), Decimal("53.7"))
        self.assertEqual(round_total(Fraction(2, 3) * 100), Decimal("66.7"))

    def test_scored_tie_uses_half_up_not_builtin_round(self) -> None:
        # 70 * 0.75 + 20 * 0 + 10 * (1.5 / 4) = 52.5 + 0 + 3.75 = 56.25 exactly.
        result = score([("M1", S, A), ("M2", P, B), ("P1", U, C), ("P2", U, C)])
        self.assertEqual(result.total_unrounded, 56.25)
        self.assertEqual(round(56.25, 1), 56.2)  # Python's built-in would round half to even
        self.assertEqual(result.total, 56.3)
        self.assertEqual(result.band, FitBand.MODERATE)

    def test_rounding_happens_before_banding(self) -> None:
        self.assertEqual(fit_band(round_total(Fraction(7495, 100))), FitBand.STRONG)  # 74.95 -> 75.0
        self.assertEqual(fit_band(round_total(Fraction(5494, 100))), FitBand.WEAK)  # 54.94 -> 54.9

    def test_standard_states_round_half_up(self) -> None:
        text = (CONTEXT / "evaluation_standard.md").read_text(encoding="utf-8")
        self.assertIn("**ROUND-HALF-UP**", text)
        self.assertIn("**not** rounded before", text)


class TestFitBands(unittest.TestCase):
    def test_boundaries(self) -> None:
        cases = [(100, FitBand.STRONG), (75, FitBand.STRONG), (74.9, FitBand.MODERATE),
                 (55, FitBand.MODERATE), (54.9, FitBand.WEAK), (0, FitBand.WEAK)]
        for total, band in cases:
            with self.subTest(total=total):
                self.assertEqual(fit_band(total), band)


class TestScoreBounds(unittest.TestCase):
    def breakdown(self, **overrides: float) -> ScoreBreakdown:
        values = dict(mandatory_weight=70, preferred_weight=20, confidence_weight=10, mandatory_score=70.0,
                      preferred_score=20.0, confidence_score=10.0, total_unrounded=100.0, total=100.0, band=FitBand.STRONG)
        values.update(overrides)
        return ScoreBreakdown(**values)  # type: ignore[arg-type]

    def test_in_bounds_passes(self) -> None:
        check_score_bounds(self.breakdown())

    def test_out_of_bounds_fails(self) -> None:
        for field, value in [("mandatory_score", 70.01), ("preferred_score", -0.1), ("confidence_score", 11.0), ("total", 100.1)]:
            with self.subTest(field=field):
                with self.assertRaisesRegex(ScoringError, "outside the range"):
                    check_score_bounds(self.breakdown(**{field: value}))


class TestEvaluateFixture(unittest.TestCase):
    def setUp(self) -> None:
        self.job = parse_job_description(FIXTURE_JD)
        self.cv = parse_cv(FIXTURE_CV)

    def test_fixture_end_to_end(self) -> None:
        result = evaluate(self.job, self.cv, load_assessment(FIXTURE_ASSESSMENT))
        self.assertEqual(result.score.total, 53.8)
        self.assertEqual(result.mandatory_gaps, ())
        self.assertEqual(result.preferred_gaps, ("P2",))
        self.assertEqual(result.items_to_verify, ("M4",))
        self.assertEqual([a.requirement_id for a in result.assessments], [r.id for r in result.requirements])


class TestValidation(unittest.TestCase):
    """Validation of supplied judgements against the fixture JD (M1-M4, P1-P2) and CV."""

    ALPHA = Evidence("Experience", "Used Tool Alpha daily in production.")

    def setUp(self) -> None:
        self.job = parse_job_description(FIXTURE_JD)
        self.cv = parse_cv(FIXTURE_CV)

    def valid(self) -> list:
        return [assessment(i, S, A, (self.ALPHA,)) for i in ("M1", "M2", "M3", "M4", "P1", "P2")]

    def errors_for(self, assessments: list, additional: tuple[Requirement, ...] = ()) -> list[str]:
        with self.assertRaises(AssessmentValidationError) as caught:
            evaluate(self.job, self.cv, submission(*assessments, additional=additional))
        return caught.exception.errors

    def test_valid_submission_passes(self) -> None:
        self.assertEqual(evaluate(self.job, self.cv, submission(*self.valid())).score.total, 100.0)

    def test_missing_assessment_fails(self) -> None:
        self.assertIn("P2: missing assessment", self.errors_for(self.valid()[:-1]))

    def test_duplicate_assessment_fails(self) -> None:
        errors = self.errors_for(self.valid() + [assessment("M1", S, A, (self.ALPHA,))])
        self.assertTrue(any("M1: assessed 2 times" in e for e in errors))

    def test_unknown_requirement_id_fails(self) -> None:
        errors = self.errors_for(self.valid() + [assessment("M9", S, A, (self.ALPHA,))])
        self.assertTrue(any("M9: unknown requirement ID" in e for e in errors))

    def test_all_errors_are_reported_together(self) -> None:
        items = self.valid()[:-1] + [assessment("M9", S, A, (self.ALPHA,)), assessment("M1", S, A, (self.ALPHA,))]
        self.assertGreaterEqual(len(self.errors_for(items)), 3)

    def test_fabricated_quote_fails(self) -> None:
        items = self.valid()
        items[0] = assessment("M1", S, A, (Evidence("Experience", "Led a Tool Alpha migration."),))
        self.assertTrue(any("quote not found verbatim" in e for e in self.errors_for(items)))

    def test_quote_from_wrong_section_fails(self) -> None:
        items = self.valid()
        items[0] = assessment("M1", S, A, (Evidence("Skills", "Used Tool Alpha daily in production."),))
        self.assertTrue(any("quote not found verbatim in CV section 'Skills'" in e for e in self.errors_for(items)))

    def test_unknown_location_fails(self) -> None:
        items = self.valid()
        items[0] = assessment("M1", S, A, (Evidence("Volunteering", "Used Tool Alpha daily in production."),))
        self.assertTrue(any("does not exactly match a CV heading" in e for e in self.errors_for(items)))

    def test_location_path_must_match_ancestry(self) -> None:
        items = self.valid()
        items[0] = assessment("M1", S, A, (Evidence("Projects → Engineer — Fixture Org *(fictional)*", "Used Tool Alpha"),))
        self.assertTrue(any("does not exactly match a CV heading" in e for e in self.errors_for(items)))

    def test_inexact_location_fails_with_closest_heading_hint(self) -> None:
        items = self.valid()
        items[0] = assessment("M1", S, A, (Evidence("experience → ENGINEER - fixture org (fictional)", "Used Tool Alpha"),))
        errors = self.errors_for(items)
        self.assertTrue(any("closest heading is 'Engineer — Fixture Org *(fictional)*'" in e for e in errors))

    def test_quote_is_case_sensitive(self) -> None:
        items = self.valid()
        items[0] = assessment("M1", S, A, (Evidence("Experience", "used tool alpha daily"),))
        self.assertTrue(any("quote not found verbatim" in e for e in self.errors_for(items)))

    def test_cited_status_without_evidence_fails(self) -> None:
        for status in (S, P, X):
            with self.subTest(status=status):
                items = self.valid()
                items[0] = assessment("M1", status, B, (), question="Q?")
                self.assertTrue(any("requires at least one evidence citation" in e for e in self.errors_for(items)))

    def test_unsupported_requires_grade_c(self) -> None:
        items = self.valid()
        items[0] = assessment("M1", U, B)
        self.assertTrue(any("evidence_grade must be C" in e for e in self.errors_for(items)))

    def test_supported_cannot_be_grade_c(self) -> None:
        items = self.valid()
        items[0] = assessment("M1", S, C, (self.ALPHA,))
        self.assertTrue(any("SUPPORTED cannot rest on grade C" in e for e in self.errors_for(items)))

    def test_unclear_requires_verification_question(self) -> None:
        items = self.valid()
        items[0] = assessment("M1", X, C, (self.ALPHA,))
        self.assertTrue(any("requires a verification_question" in e for e in self.errors_for(items)))


class TestMandatoryGaps(unittest.TestCase):
    def setUp(self) -> None:
        self.job = parse_job_description(FIXTURE_JD)
        self.cv = parse_cv(FIXTURE_CV)
        alpha = Evidence("Experience", "Used Tool Alpha daily in production.")
        self.items = {i: assessment(i, S, A, (alpha,)) for i in ("M1", "M2", "M3", "M4", "P1", "P2")}

    def test_unsupported_mandatory_is_a_gap(self) -> None:
        self.items["M2"] = assessment("M2", U, C)
        self.items["P1"] = assessment("P1", U, C)
        result = evaluate(self.job, self.cv, submission(*self.items.values()))
        self.assertEqual(result.mandatory_gaps, ("M2",))
        self.assertEqual(result.preferred_gaps, ("P1",))

    def test_gap_does_not_change_band_automatically(self) -> None:
        self.items["M4"] = assessment("M4", U, C)
        result = evaluate(self.job, self.cv, submission(*self.items.values()))
        self.assertEqual(result.mandatory_gaps, ("M4",))
        self.assertEqual(result.score.total, 80.8)  # 52.5 + 20 + 8.33
        self.assertEqual(result.score.band, FitBand.STRONG)  # the gap is flagged, not used to demote

    def test_unclear_mandatory_is_not_a_gap(self) -> None:
        self.items["M1"] = assessment("M1", X, C, (Evidence("Skills", "Tool Delta"),), question="Where?")
        result = evaluate(self.job, self.cv, submission(*self.items.values()))
        self.assertEqual(result.mandatory_gaps, ())
        self.assertEqual(result.items_to_verify, ("M1",))


class TestAdditionalRequirements(unittest.TestCase):
    """Agent-identified requirements must quote the job description verbatim."""

    def setUp(self) -> None:
        self.job = parse_job_description(FIXTURE_JD)
        self.cv = parse_cv(FIXTURE_CV)
        alpha = Evidence("Experience", "Used Tool Alpha daily in production.")
        self.items = [assessment(i, S, A, (alpha,)) for i in ("M1", "M2", "M3", "M4", "P1", "P2")]

    def extra(self, quote: str, req_id: str = "A1") -> Requirement:
        return Requirement(req_id, "Operate Tool Alpha", RequirementType.MANDATORY,
                           RequirementOrigin.AGENT_IDENTIFIED, quote)

    def test_valid_additional_requirement_is_scored(self) -> None:
        extra = self.extra("Operate the Tool Alpha platform.")
        result = evaluate(self.job, self.cv, submission(*self.items, assessment("A1", U, C), additional=(extra,)))
        self.assertEqual(result.requirements[-1].id, "A1")
        self.assertEqual(result.mandatory_gaps, ("A1",))
        self.assertAlmostEqual(result.score.mandatory_score, 70 * 4 / 5)

    def test_quote_not_in_job_description_fails(self) -> None:
        extra = self.extra("Must hold a security clearance.")
        with self.assertRaisesRegex(AssessmentValidationError, "does not appear verbatim in the job description"):
            evaluate(self.job, self.cv, submission(*self.items, assessment("A1", U, C), additional=(extra,)))

    def test_additional_requirement_must_be_assessed(self) -> None:
        extra = self.extra("Operate the Tool Alpha platform.")
        with self.assertRaisesRegex(AssessmentValidationError, "A1: missing assessment"):
            evaluate(self.job, self.cv, submission(*self.items, additional=(extra,)))

    def test_duplicate_additional_ids_fail(self) -> None:
        extras = (self.extra("Operate the Tool Alpha platform."),) * 2
        with self.assertRaisesRegex(AssessmentValidationError, "duplicates an existing requirement"):
            evaluate(self.job, self.cv, submission(*self.items, assessment("A1", U, C), additional=extras))


CV_SOURCE_LINE = "Rewrote the `alpha-cli` wrapper — **twice** as fast as the"
CV_WRAPPED = "as fast as the\n  previous script."
JD_SOURCE_LINE = "Maintain the `beta-sync` service — **weekly**, with partner teams."

# Each variant differs from the source by exactly one kind of character change.
VERBATIM_VIOLATIONS = {
    "wrong case": lambda q: q.replace("Rewrote", "rewrote").replace("Maintain", "maintain"),
    "hyphen for em dash": lambda q: q.replace("—", "-"),
    "en dash for em dash": lambda q: q.replace("—", "–"),
    "removed emphasis markers": lambda q: q.replace("**", ""),
    "removed backticks": lambda q: q.replace("`", ""),
    "altered internal spacing": lambda q: q.replace(" — ", "  —  "),
    "changed punctuation": lambda q: q.replace("— ", ", ").replace(", with", "; with"),
}


class TestVerbatimQuotes(unittest.TestCase):
    """Quotes must match source text character for character (standard section 4).

    Allowed: surrounding whitespace and CRLF/CR line endings. Nothing else.
    """

    ROLE = "Engineer — Fixture Org *(fictional)*"

    def setUp(self) -> None:
        self.job = parse_job_description(FIXTURE_JD)
        self.cv = parse_cv(FIXTURE_CV)
        alpha = Evidence("Experience", "Used Tool Alpha daily in production.")
        self.others = [assessment(i, S, A, (alpha,)) for i in ("M2", "M3", "M4", "P1", "P2")]

    def quote_errors(self, quote: str) -> list[str]:
        items = [assessment("M1", S, A, (Evidence(self.ROLE, quote),))] + self.others
        try:
            evaluate(self.job, self.cv, submission(*items))
        except AssessmentValidationError as error:
            return error.errors
        return []

    def source_quote_errors(self, quote: str) -> list[str]:
        extra = Requirement("A1", "Maintain beta-sync", RequirementType.MANDATORY, RequirementOrigin.AGENT_IDENTIFIED, quote)
        items = [assessment("M1", S, A, (Evidence(self.ROLE, "Used Tool Alpha daily in production."),))]
        items += self.others + [assessment("A1", U, C)]
        try:
            evaluate(self.job, self.cv, submission(*items, additional=(extra,)))
        except AssessmentValidationError as error:
            return error.errors
        return []

    # --- Evidence.quote: passing cases

    def test_exact_quote_passes(self) -> None:
        self.assertEqual(self.quote_errors(CV_SOURCE_LINE), [])

    def test_exact_multiline_quote_with_original_indentation_passes(self) -> None:
        self.assertEqual(self.quote_errors(CV_WRAPPED), [])

    def test_crlf_line_endings_are_normalised(self) -> None:
        self.assertEqual(self.quote_errors(CV_WRAPPED.replace("\n", "\r\n")), [])

    def test_surrounding_whitespace_is_ignored(self) -> None:
        self.assertEqual(self.quote_errors(f"  {CV_SOURCE_LINE}\n"), [])

    # --- Evidence.quote: failing cases

    def test_character_level_changes_fail(self) -> None:
        for name, change in VERBATIM_VIOLATIONS.items():
            with self.subTest(change=name):
                altered = change(CV_SOURCE_LINE)
                self.assertNotEqual(altered, CV_SOURCE_LINE)
                self.assertTrue(any("quote not found verbatim" in e for e in self.quote_errors(altered)))

    def test_collapsed_line_wrap_fails(self) -> None:
        self.assertTrue(self.quote_errors("as fast as the previous script."))

    def test_reindented_line_wrap_fails(self) -> None:
        self.assertTrue(self.quote_errors("as fast as the\nprevious script."))

    def test_whitespace_only_quote_fails(self) -> None:
        self.assertTrue(self.quote_errors("   "))

    # --- additional_requirements source_quote

    def test_exact_source_quote_passes(self) -> None:
        self.assertEqual(self.source_quote_errors(JD_SOURCE_LINE), [])

    def test_source_quote_character_level_changes_fail(self) -> None:
        for name, change in VERBATIM_VIOLATIONS.items():
            with self.subTest(change=name):
                altered = change(JD_SOURCE_LINE)
                self.assertNotEqual(altered, JD_SOURCE_LINE)
                errors = self.source_quote_errors(altered)
                self.assertTrue(any("does not appear verbatim in the job description" in e for e in errors))


class TestLocationExactness(unittest.TestCase):
    """Citation locations must match CV heading text exactly (standard section 4).

    Uses Candidate A's real headings but only resolves locations: no statuses or quotes.
    """

    HEADING = "Software Engineer — Example Logistics Ltd *(fictional)*"

    @classmethod
    def setUpClass(cls) -> None:
        cls.cv = parse_cv(CONTEXT / "candidate_cv.md")

    def resolves(self, location: str) -> bool:
        return _resolve_location(location, self.cv) is not None

    def test_exact_heading_passes(self) -> None:
        self.assertTrue(self.resolves(self.HEADING))
        self.assertTrue(self.resolves("Skills"))

    def test_exact_parent_child_form_passes(self) -> None:
        self.assertTrue(self.resolves(f"Professional experience → {self.HEADING}"))

    def test_spacing_around_separator_is_not_significant(self) -> None:
        self.assertTrue(self.resolves(f"Professional experience→{self.HEADING}"))

    def test_wrong_case_fails(self) -> None:
        for location in (self.HEADING.lower(), self.HEADING.upper(), "skills", f"professional experience → {self.HEADING}"):
            with self.subTest(location=location):
                self.assertFalse(self.resolves(location))

    def test_wrong_dash_character_fails(self) -> None:
        for dash in ("-", "–"):  # hyphen, en dash; the CV uses an em dash
            with self.subTest(dash=dash):
                self.assertFalse(self.resolves(self.HEADING.replace("—", dash)))

    def test_missing_inline_formatting_fails(self) -> None:
        self.assertFalse(self.resolves("Software Engineer — Example Logistics Ltd (fictional)"))

    def test_meaningful_spacing_difference_fails(self) -> None:
        self.assertFalse(self.resolves(self.HEADING.replace(" — ", "  —  ")))

    def test_nonexistent_heading_fails(self) -> None:
        for location in ("Volunteering", "Software Engineer — Example Logistics Ltd", f"Personal projects → {self.HEADING}"):
            with self.subTest(location=location):
                self.assertFalse(self.resolves(location))

    def test_undocumented_separator_is_not_accepted(self) -> None:
        self.assertFalse(self.resolves(f"Professional experience > {self.HEADING}"))

    def test_empty_location_parts_fail(self) -> None:
        for location in ("", " → Skills", "Skills → "):
            with self.subTest(location=location):
                self.assertFalse(self.resolves(location))


if __name__ == "__main__":
    unittest.main()
