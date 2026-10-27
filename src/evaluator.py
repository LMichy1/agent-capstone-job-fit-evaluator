"""Validation and scoring of externally supplied requirement assessments.

Implements section 6 of context/evaluation_standard.md (v0.1). Statuses and
evidence grades are inputs; this module never assigns them. Arithmetic uses
exact fractions, and only the final total is rounded (half-up, one decimal).
"""

from __future__ import annotations

from collections.abc import Iterable
from decimal import ROUND_HALF_UP, Decimal
from fractions import Fraction
from pathlib import Path

from .models import (
    AssessmentResult,
    AssessmentSubmission,
    AssessmentValidationError,
    CVDocument,
    CVSection,
    EvidenceGrade,
    FitBand,
    JobDescription,
    Requirement,
    RequirementAssessment,
    RequirementType,
    ScoreBreakdown,
    ScoringError,
    Status,
)
from .parser import normalise_heading, parse_standard_constants

MANDATORY_WEIGHT = 70
PREFERRED_WEIGHT = 20
CONFIDENCE_WEIGHT = 10
MANDATORY_WEIGHT_WITHOUT_PREFERRED = 90

STATUS_CREDIT: dict[Status, Fraction] = {
    Status.SUPPORTED: Fraction(1),
    Status.PARTIALLY_SUPPORTED: Fraction(1, 2),
    Status.UNCLEAR: Fraction(0),
    Status.UNSUPPORTED: Fraction(0),
}
GRADE_VALUE: dict[EvidenceGrade, Fraction] = {
    EvidenceGrade.A: Fraction(1),
    EvidenceGrade.B: Fraction(1, 2),
    EvidenceGrade.C: Fraction(0),
}
STRONG_FIT_THRESHOLD = Decimal("75")
MODERATE_FIT_THRESHOLD = Decimal("55")

LOCATION_SEPARATOR = "→"


# --- Public API ---------------------------------------------------------------


def evaluate(job: JobDescription, cv: CVDocument, submission: AssessmentSubmission) -> AssessmentResult:
    """Validate a submission against the parsed inputs and score it."""
    requirements = validate_submission(job, cv, submission)
    by_id = {assessment.requirement_id: assessment for assessment in submission.assessments}
    ordered = tuple(by_id[req.id] for req in requirements)
    breakdown = calculate_score(requirements, ordered)

    def ids_with(req_type: RequirementType | None, status: Status) -> tuple[str, ...]:
        return tuple(
            req.id
            for req, assessment in zip(requirements, ordered)
            if assessment.status is status and (req_type is None or req.type is req_type)
        )

    return AssessmentResult(
        candidate_id=submission.candidate_id,
        job_title=job.title,
        requirements=requirements,
        assessments=ordered,
        score=breakdown,
        mandatory_gaps=ids_with(RequirementType.MANDATORY, Status.UNSUPPORTED),
        preferred_gaps=ids_with(RequirementType.PREFERRED, Status.UNSUPPORTED),
        items_to_verify=ids_with(None, Status.UNCLEAR),
        submission=submission,
    )


def validate_submission(
    job: JobDescription, cv: CVDocument, submission: AssessmentSubmission
) -> tuple[Requirement, ...]:
    """Return the full requirement list, or raise with every problem found."""
    errors: list[str] = []
    requirements = _merge_requirements(job, submission.additional_requirements, errors)
    known_ids = {req.id for req in requirements}

    assessed_ids = [assessment.requirement_id for assessment in submission.assessments]
    for req_id in sorted({i for i in assessed_ids if assessed_ids.count(i) > 1}):
        errors.append(f"{req_id}: assessed {assessed_ids.count(req_id)} times (exactly one assessment required)")
    for req_id in sorted(set(assessed_ids) - known_ids):
        errors.append(f"{req_id}: unknown requirement ID (not in the job description or additional_requirements)")
    for req in requirements:
        if req.id not in assessed_ids:
            errors.append(f"{req.id}: missing assessment")

    for assessment in submission.assessments:
        errors.extend(_check_assessment(assessment, cv))

    if errors:
        raise AssessmentValidationError(errors)
    return requirements


def calculate_score(
    requirements: tuple[Requirement, ...], assessments: tuple[RequirementAssessment, ...]
) -> ScoreBreakdown:
    """Apply the section 6 formulas. `assessments` must align with `requirements`."""
    if len(requirements) != len(assessments) or any(
        req.id != assessment.requirement_id for req, assessment in zip(requirements, assessments)
    ):
        raise ScoringError("assessments must align one-to-one with requirements")

    mandatory = [a for r, a in zip(requirements, assessments) if r.type is RequirementType.MANDATORY]
    preferred = [a for r, a in zip(requirements, assessments) if r.type is RequirementType.PREFERRED]
    if not mandatory:
        raise ScoringError(
            "no mandatory requirements: the evaluation standard (v0.1) defines no scoring rule for this case"
        )

    mandatory_weight = MANDATORY_WEIGHT if preferred else MANDATORY_WEIGHT_WITHOUT_PREFERRED
    preferred_weight = PREFERRED_WEIGHT if preferred else 0

    mandatory_score = mandatory_weight * _mean(STATUS_CREDIT[a.status] for a in mandatory)
    preferred_score = preferred_weight * _mean(STATUS_CREDIT[a.status] for a in preferred) if preferred else Fraction(0)
    confidence_score = CONFIDENCE_WEIGHT * _mean(GRADE_VALUE[a.evidence_grade] for a in assessments)
    total_exact = mandatory_score + preferred_score + confidence_score
    total = round_total(total_exact)

    breakdown = ScoreBreakdown(
        mandatory_weight=mandatory_weight,
        preferred_weight=preferred_weight,
        confidence_weight=CONFIDENCE_WEIGHT,
        mandatory_score=float(mandatory_score),
        preferred_score=float(preferred_score),
        confidence_score=float(confidence_score),
        total_unrounded=float(total_exact),
        total=float(total),
        band=fit_band(total),
    )
    check_score_bounds(breakdown)
    return breakdown


def round_total(value: Fraction) -> Decimal:
    """Round an exact total to one decimal place, ROUND-HALF-UP (standard section 6).

    Deliberately avoids built-in round(), which rounds half to even on floats.
    """
    exact = Decimal(value.numerator) / Decimal(value.denominator)
    return exact.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)


def fit_band(total: Decimal | float) -> FitBand:
    """Band from the rounded total: >= 75 strong, >= 55 moderate, else weak."""
    total = Decimal(str(total))
    if total >= STRONG_FIT_THRESHOLD:
        return FitBand.STRONG
    if total >= MODERATE_FIT_THRESHOLD:
        return FitBand.MODERATE
    return FitBand.WEAK


def check_score_bounds(breakdown: ScoreBreakdown) -> None:
    """Raise if any component falls outside [0, its weight] or the total outside [0, 100]."""
    components = [
        ("mandatory", breakdown.mandatory_score, breakdown.mandatory_weight),
        ("preferred", breakdown.preferred_score, breakdown.preferred_weight),
        ("confidence", breakdown.confidence_score, breakdown.confidence_weight),
        ("total", breakdown.total, 100),
    ]
    for name, value, upper in components:
        if not 0 <= value <= upper:
            raise ScoringError(f"{name} score {value} is outside the range [0, {upper}]")


def check_standard_consistency(standard_path: Path | str) -> None:
    """Raise if the standard's weight/credit/grade tables differ from this module."""
    tables = parse_standard_constants(standard_path)
    expected = {
        "weights": {
            "Mandatory requirements": MANDATORY_WEIGHT,
            "Preferred requirements": PREFERRED_WEIGHT,
            "Evidence quality / confidence": CONFIDENCE_WEIGHT,
        },
        "status_credit": {status.value: credit for status, credit in STATUS_CREDIT.items()},
        "grade_value": {grade.value: value for grade, value in GRADE_VALUE.items()},
    }
    problems = []
    for table, entries in expected.items():
        for key, value in entries.items():
            found = tables[table].get(key)
            if found is None:
                problems.append(f"{table}: '{key}' not found in {standard_path}")
            elif Fraction(found) != Fraction(value):
                problems.append(f"{table}: '{key}' is {found} in the standard but {float(value)} in the evaluator")
    if problems:
        raise ScoringError("evaluation standard and evaluator disagree:\n  - " + "\n  - ".join(problems))


# --- Validation helpers -------------------------------------------------------


def _merge_requirements(
    job: JobDescription, additional: tuple[Requirement, ...], errors: list[str]
) -> tuple[Requirement, ...]:
    listed_ids = {req.id for req in job.requirements}
    seen: set[str] = set()
    for req in additional:
        if req.id in listed_ids or req.id in seen:
            errors.append(f"{req.id}: additional requirement ID duplicates an existing requirement")
        seen.add(req.id)
        if req.source_quote and not _contains_verbatim(job.text, req.source_quote):
            errors.append(f"{req.id}: source_quote does not appear verbatim in the job description")
    return job.requirements + additional


def _check_assessment(assessment: RequirementAssessment, cv: CVDocument) -> list[str]:
    req_id = assessment.requirement_id
    errors = []
    status, grade = assessment.status, assessment.evidence_grade

    if status is not Status.UNSUPPORTED and not assessment.evidence:
        errors.append(f"{req_id}: status {status.value} requires at least one evidence citation")
    if status is Status.UNSUPPORTED and grade is not EvidenceGrade.C:
        errors.append(f"{req_id}: UNSUPPORTED means no evidence, so evidence_grade must be C (got {grade.value})")
    if status is Status.SUPPORTED and grade is EvidenceGrade.C:
        errors.append(f"{req_id}: SUPPORTED cannot rest on grade C (keyword-only or no evidence)")
    if status is Status.UNCLEAR and not assessment.verification_question:
        errors.append(f"{req_id}: UNCLEAR requires a verification_question for the candidate")

    for index, evidence in enumerate(assessment.evidence):
        section = _resolve_location(evidence.location, cv)
        if section is None:
            errors.append(
                f"{req_id} evidence[{index}]: location {evidence.location!r} does not exactly match a CV heading"
                + _closest_heading_hint(evidence.location, cv)
            )
        elif not _contains_verbatim(section.body, evidence.quote):
            errors.append(
                f"{req_id} evidence[{index}]: quote not found verbatim in CV section {section.heading!r}: "
                f"{evidence.quote!r}"
            )
    return errors


def _contains_verbatim(source: str, quote: str) -> bool:
    """True if `quote` occurs character for character in `source` (standard section 4).

    Only line endings (CRLF/CR -> LF) and whitespace surrounding the quote are
    normalised. Case, punctuation, dashes, Markdown markers, backticks and
    internal spacing, including line breaks and indentation, must match.
    """
    quote = _unify_line_endings(quote).strip()
    return bool(quote) and quote in _unify_line_endings(source)


def _unify_line_endings(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _location_parts(location: str) -> list[str]:
    """Split 'Parent → Heading' on the separator; only whitespace around it is dropped."""
    return [part.strip() for part in location.split(LOCATION_SEPARATOR)]


def _resolve_location(location: str, cv: CVDocument) -> CVSection | None:
    """Match 'Heading' or 'Parent → Heading' exactly against the CV's heading tree.

    Heading text is compared character for character as parsed from the CV
    (without its leading '#' markers): no case, dash, spacing or emphasis
    normalisation.
    """
    parts = _location_parts(location)
    if not all(parts):
        return None

    *ancestors, target = parts
    for section in cv.sections:
        if section.heading == target and all(_has_ancestor(cv, section.parent_heading, name) for name in ancestors):
            return section
    return None


def _has_ancestor(cv: CVDocument, heading: str | None, wanted: str) -> bool:
    while heading is not None:
        if heading == wanted:
            return True
        heading = next((s.parent_heading for s in cv.sections if s.heading == heading), None)
    return False


def _closest_heading_hint(location: str, cv: CVDocument) -> str:
    """Name a heading that differs only in case/dash/formatting. Diagnostic only: never accepted."""
    target = normalise_heading(_location_parts(location)[-1])
    for section in cv.sections:
        if normalise_heading(section.heading) == target:
            return f" (closest heading is {section.heading!r}; case, dash characters and formatting must match exactly)"
    return ""


def _mean(values: Iterable[Fraction]) -> Fraction:
    items = list(values)
    return sum(items, Fraction(0)) / len(items)
