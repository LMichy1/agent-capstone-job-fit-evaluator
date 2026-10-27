"""Shared paths and builders for the test suite (unittest- and pytest-compatible)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.models import (
    AssessmentSubmission,
    Evidence,
    EvidenceGrade,
    Requirement,
    RequirementAssessment,
    RequirementType,
    Status,
)

ROOT = Path(__file__).resolve().parent.parent
CONTEXT = ROOT / "context"
FIXTURES = Path(__file__).resolve().parent / "fixtures"

FIXTURE_JD = FIXTURES / "job_description_fixture.md"
FIXTURE_CV = FIXTURES / "cv_fixture.md"
FIXTURE_ASSESSMENT = FIXTURES / "assessment_fixture.json"
MALFORMED_ASSESSMENT = FIXTURES / "assessment_malformed.json"


def requirement(req_id: str) -> Requirement:
    req_type = RequirementType.MANDATORY if req_id.startswith("M") else RequirementType.PREFERRED
    return Requirement(id=req_id, text=f"Requirement {req_id}", type=req_type)


def assessment(
    req_id: str,
    status: Status = Status.SUPPORTED,
    grade: EvidenceGrade = EvidenceGrade.A,
    evidence: tuple[Evidence, ...] = (),
    question: str = "",
) -> RequirementAssessment:
    return RequirementAssessment(
        requirement_id=req_id,
        status=status,
        evidence_grade=grade,
        evidence=evidence,
        rationale=f"Rationale for {req_id}",
        verification_question=question,
    )


def submission(*assessments: RequirementAssessment, additional: tuple[Requirement, ...] = ()) -> AssessmentSubmission:
    return AssessmentSubmission(
        candidate_id="Fixture Candidate",
        sources_inspected=("cv_fixture.md",),
        sources_excluded=(),
        additional_requirements=additional,
        assessments=tuple(assessments),
        positioning="Positioning.",
        application_brief="Brief.",
        uncertainties=(),
    )


def fixture_data() -> dict[str, Any]:
    return json.loads(FIXTURE_ASSESSMENT.read_text(encoding="utf-8"))


def write_json(directory: Path, data: dict[str, Any]) -> Path:
    path = directory / "assessment.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return path
