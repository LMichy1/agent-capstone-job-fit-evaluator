"""Tests for src/parser.py: structural parsing only, no semantic matching."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest import mock

from src.models import AssessmentValidationError, ParseError, RequirementType
from src.parser import load_assessment, parse_cv, parse_job_description, parse_standard_constants
from support import CONTEXT, FIXTURE_ASSESSMENT, FIXTURE_CV, MALFORMED_ASSESSMENT, fixture_data, write_json

JD_TEMPLATE = """# Job Description — Test

## Mandatory requirements

{mandatory}

## Preferred requirements

{preferred}
"""


class TempFileMixin(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def write(self, name: str, text: str) -> Path:
        path = self.tmp / name
        path.write_text(text, encoding="utf-8")
        return path

    def jd(self, mandatory: str = "1. **M1** — Must.", preferred: str = "1. **P1** — Nice.") -> Path:
        return self.write("jd.md", JD_TEMPLATE.format(mandatory=mandatory, preferred=preferred))


class TestCapstoneJobDescription(unittest.TestCase):
    """Structural checks against the real capstone job description."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.job = parse_job_description(CONTEXT / "job_description.md")
        cls.by_id = {req.id: req for req in cls.job.requirements}

    def test_discovers_m1_to_m6(self) -> None:
        mandatory = [r.id for r in self.job.requirements if r.type is RequirementType.MANDATORY]
        self.assertEqual(mandatory, [f"M{i}" for i in range(1, 7)])

    def test_discovers_p1_to_p6(self) -> None:
        preferred = [r.id for r in self.job.requirements if r.type is RequirementType.PREFERRED]
        self.assertEqual(preferred, [f"P{i}" for i in range(1, 7)])

    def test_preserves_requirement_text_including_wrapped_lines(self) -> None:
        self.assertEqual(
            self.by_id["M1"].text,
            "At least 3 years of professional software engineering experience using Python for backend development.",
        )
        self.assertEqual(self.by_id["P2"].text, "Experience with Kubernetes.")

    def test_classification(self) -> None:
        self.assertIs(self.by_id["M6"].type, RequirementType.MANDATORY)
        self.assertIs(self.by_id["P6"].type, RequirementType.PREFERRED)

    def test_only_labelled_sections_are_parsed(self) -> None:
        # Responsibilities and other prose are not converted into requirements.
        self.assertEqual(len(self.job.requirements), 12)

    def test_title(self) -> None:
        self.assertEqual(self.job.title, "Job Description — Backend Software Engineer (Python)")


class TestJobDescriptionErrors(TempFileMixin):
    def test_duplicate_ids_fail(self) -> None:
        path = self.jd(mandatory="1. **M1** — One.\n2. **M1** — Two.")
        with self.assertRaisesRegex(ParseError, "duplicate requirement ID"):
            parse_job_description(path)

    def test_duplicate_across_sections_fail(self) -> None:
        # Preferred IDs must start with P, so a cross-section duplicate is caught as malformed.
        path = self.jd(preferred="1. **M1** — Duplicate in wrong section.")
        with self.assertRaisesRegex(ParseError, "malformed requirement ID 'M1'"):
            parse_job_description(path)

    def test_malformed_ids_fail(self) -> None:
        for bad_id in ("M-1", "X1", "M0", "m1", "P1"):
            with self.subTest(bad_id=bad_id):
                path = self.jd(mandatory=f"1. **{bad_id}** — Text.")
                with self.assertRaisesRegex(ParseError, "malformed requirement ID"):
                    parse_job_description(path)

    def test_missing_mandatory_section_fails(self) -> None:
        path = self.write("jd.md", "# Title\n\n## Preferred requirements\n\n1. **P1** — Nice.\n")
        with self.assertRaisesRegex(ParseError, "Mandatory requirements' is missing"):
            parse_job_description(path)

    def test_missing_preferred_section_fails(self) -> None:
        path = self.write("jd.md", "# Title\n\n## Mandatory requirements\n\n1. **M1** — Must.\n")
        with self.assertRaisesRegex(ParseError, "Preferred requirements' is missing"):
            parse_job_description(path)

    def test_missing_title_fails(self) -> None:
        path = self.write("jd.md", JD_TEMPLATE.format(mandatory="1. **M1** — A.", preferred="1. **P1** — B.").split("\n", 1)[1])
        with self.assertRaisesRegex(ParseError, "title"):
            parse_job_description(path)

    def test_unexpected_structure_fails(self) -> None:
        for body in ("- M1: bullet instead of numbered item", "1. M1 — no bold ID", "Some free prose."):
            with self.subTest(body=body):
                with self.assertRaisesRegex(ParseError, "unexpected line"):
                    parse_job_description(self.jd(mandatory=body))

    def test_empty_section_fails(self) -> None:
        with self.assertRaisesRegex(ParseError, "contains no requirements"):
            parse_job_description(self.jd(preferred=""))

    def test_repeated_section_fails(self) -> None:
        text = JD_TEMPLATE.format(mandatory="1. **M1** — A.", preferred="1. **P1** — B.")
        path = self.write("jd.md", text + "\n## Mandatory requirements\n\n1. **M2** — C.\n")
        with self.assertRaisesRegex(ParseError, "appears 2 times"):
            parse_job_description(path)

    def test_missing_file_fails(self) -> None:
        with self.assertRaisesRegex(ParseError, "File not found"):
            parse_job_description(self.tmp / "absent.md")


class TestCVParsing(TempFileMixin):
    def test_capstone_cv_sections(self) -> None:
        cv = parse_cv(CONTEXT / "candidate_cv.md")
        headings = {s.heading for s in cv.sections if s.level == 2}
        self.assertTrue({"Professional experience", "Personal projects", "Skills", "Education"} <= headings)

    def test_subsection_parent_and_body(self) -> None:
        cv = parse_cv(FIXTURE_CV)
        role = next(s for s in cv.sections if s.heading.startswith("Engineer"))
        self.assertEqual(role.level, 3)
        self.assertEqual(role.parent_heading, "Experience")
        self.assertIn("Maintained Tool Beta pipelines.", role.body)
        self.assertNotIn("Tool Epsilon", role.body)

    def test_level_two_body_includes_subsections(self) -> None:
        cv = parse_cv(FIXTURE_CV)
        experience = next(s for s in cv.sections if s.heading == "Experience")
        self.assertIn("Used Tool Alpha daily in production.", experience.body)

    def test_cv_without_sections_fails(self) -> None:
        with self.assertRaisesRegex(ParseError, "no level-2 sections"):
            parse_cv(self.write("cv.md", "# CV\n\nJust prose.\n"))


class TestNoImplicitFileAccess(TempFileMixin):
    def test_irrelevant_reference_is_not_loaded(self) -> None:
        for name in ("job_description.md", "candidate_cv.md"):
            self.write(name, (CONTEXT / name).read_text(encoding="utf-8"))
        self.write("irrelevant_reference.md", "SENTINEL — must never be read")

        read_paths: list[str] = []
        original = Path.read_text

        def recording_read_text(path: Path, *args, **kwargs):  # type: ignore[no-untyped-def]
            read_paths.append(path.name)
            return original(path, *args, **kwargs)

        with mock.patch.object(Path, "read_text", recording_read_text):
            job = parse_job_description(self.tmp / "job_description.md")
            cv = parse_cv(self.tmp / "candidate_cv.md")

        self.assertEqual(read_paths, ["job_description.md", "candidate_cv.md"])
        self.assertNotIn("SENTINEL", job.text + cv.text)


class TestLoadAssessment(TempFileMixin):
    def test_fixture_loads(self) -> None:
        submission = load_assessment(FIXTURE_ASSESSMENT)
        self.assertEqual([a.requirement_id for a in submission.assessments], ["M1", "M2", "M3", "M4", "P1", "P2"])

    def test_malformed_fixture_reports_every_structural_problem(self) -> None:
        with self.assertRaises(AssessmentValidationError) as caught:
            load_assessment(MALFORMED_ASSESSMENT)
        joined = "\n".join(caught.exception.errors)
        self.assertIn("invalid status 'MOSTLY_SUPPORTED'", joined)
        self.assertIn("invalid evidence_grade 'E'", joined)
        self.assertIn("unknown field 'evidense'", joined)
        self.assertIn("missing required field 'evidence'", joined)

    def test_invalid_json_fails(self) -> None:
        with self.assertRaisesRegex(AssessmentValidationError, "invalid JSON"):
            load_assessment(self.write("bad.json", "{not json"))

    def test_wrong_schema_version_fails(self) -> None:
        data = fixture_data()
        data["schema_version"] = 2
        with self.assertRaisesRegex(AssessmentValidationError, "schema_version"):
            load_assessment(write_json(self.tmp, data))

    def test_unknown_top_level_field_fails(self) -> None:
        data = fixture_data()
        data["overall_score"] = 99
        with self.assertRaisesRegex(AssessmentValidationError, "unknown field 'overall_score'"):
            load_assessment(write_json(self.tmp, data))

    def test_wrong_types_fail(self) -> None:
        data = fixture_data()
        data["assessments"][0]["rationale"] = 5
        data["assessments"][1]["evidence"] = "a string"
        with self.assertRaises(AssessmentValidationError) as caught:
            load_assessment(write_json(self.tmp, data))
        self.assertEqual(len(caught.exception.errors), 2)

    def test_empty_rationale_fails(self) -> None:
        data = fixture_data()
        data["assessments"][5]["rationale"] = "   "
        with self.assertRaisesRegex(AssessmentValidationError, "'rationale' must be a non-empty string"):
            load_assessment(write_json(self.tmp, data))

    def test_additional_requirement_id_pattern_enforced(self) -> None:
        data = fixture_data()
        data["additional_requirements"] = [
            {"id": "M7", "type": "mandatory", "text": "x", "source_quote": "Operate the Tool Alpha platform."}
        ]
        with self.assertRaisesRegex(AssessmentValidationError, "must match"):
            load_assessment(write_json(self.tmp, data))


class TestStandardConstants(unittest.TestCase):
    def test_reads_scoring_tables(self) -> None:
        tables = parse_standard_constants(CONTEXT / "evaluation_standard.md")
        self.assertEqual(
            tables["weights"],
            {"Mandatory requirements": "70", "Preferred requirements": "20", "Evidence quality / confidence": "10"},
        )
        self.assertEqual(tables["status_credit"]["PARTIALLY_SUPPORTED"], "0.5")
        self.assertEqual(tables["grade_value"], {"A": "1.0", "B": "0.5", "C": "0.0"})


if __name__ == "__main__":
    unittest.main()
