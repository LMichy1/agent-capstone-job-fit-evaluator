"""Deterministic Markdown rendering of a validated AssessmentResult.

The renderer only lays out what it is given. Narrative sections (positioning,
application brief, uncertainties) are reproduced verbatim from the submission.
"""

from __future__ import annotations

from .models import AssessmentResult, Requirement, RequirementAssessment, RequirementOrigin, RequirementType, Status

NONE_LINE = "_None._"
NO_EVIDENCE = "No evidence cited"

SECTION_TITLES = (
    "1. Sources inspected",
    "2. Requirements assessment",
    "3. Score breakdown",
    "4. Genuine gaps",
    "5. Items to verify",
    "6. Recommended positioning",
    "7. Application brief",
    "8. Uncertainties and assumptions",
)


def render_report(result: AssessmentResult) -> str:
    sections = [
        _header(result),
        _sources(result),
        _requirements_table(result),
        _score(result),
        _gaps(result),
        _items_to_verify(result),
        _verbatim(SECTION_TITLES[5], result.submission.positioning),
        _verbatim(SECTION_TITLES[6], result.submission.application_brief),
        _uncertainties(result),
        _footer(),
    ]
    return "\n\n".join(sections).rstrip() + "\n"


def _header(result: AssessmentResult) -> str:
    score = result.score
    lines = [
        f"# Job Fit Assessment — {result.candidate_id}",
        "",
        f"- **Job:** {result.job_title}",
        f"- **Total score:** {score.total:.1f} / 100",
        f"- **Fit band:** {score.band.value}",
    ]
    if result.mandatory_gaps:
        lines += ["", f"> **⚠ MANDATORY GAP:** unsupported mandatory requirement(s): {', '.join(result.mandatory_gaps)}."]
    return "\n".join(lines)


def _sources(result: AssessmentResult) -> str:
    submission = result.submission
    lines = [f"## {SECTION_TITLES[0]}", "", "**Inspected:**", ""]
    lines += [f"- `{path}`" for path in submission.sources_inspected]
    lines += ["", "**Excluded:**", ""]
    lines += [f"- `{source.path}` — {source.reason}" for source in submission.sources_excluded] or [NONE_LINE]
    return "\n".join(lines)


def _requirements_table(result: AssessmentResult) -> str:
    lines = [
        f"## {SECTION_TITLES[1]}",
        "",
        "| ID | Type | Requirement | Status | Grade | Evidence location | Quote | Reasoning |",
        "|----|------|-------------|--------|-------|-------------------|-------|-----------|",
    ]
    for req, assessment in zip(result.requirements, result.assessments):
        lines.append(_requirement_row(req, assessment))
    if any(req.origin is RequirementOrigin.AGENT_IDENTIFIED for req in result.requirements):
        lines += ["", "_† Requirement identified by the assessor outside the labelled requirement lists._"]
    return "\n".join(lines)


def _requirement_row(req: Requirement, assessment: RequirementAssessment) -> str:
    req_id = req.id + (" †" if req.origin is RequirementOrigin.AGENT_IDENTIFIED else "")
    status = f"**{assessment.status.value}**"
    if assessment.status is Status.UNSUPPORTED and req.type is RequirementType.MANDATORY:
        status += " ⚠ MANDATORY GAP"
    if assessment.evidence:
        locations = "<br>".join(_cell(e.location) for e in assessment.evidence)
        quotes = "<br>".join(f"“{_cell(e.quote)}”" for e in assessment.evidence)
    else:
        locations, quotes = NO_EVIDENCE, "—"
    cells = [req_id, req.type.value, _cell(req.text), status, assessment.evidence_grade.value, locations, quotes, _cell(assessment.rationale)]
    return "| " + " | ".join(cells) + " |"


def _score(result: AssessmentResult) -> str:
    score = result.score
    return "\n".join(
        [
            f"## {SECTION_TITLES[2]}",
            "",
            "| Component | Weight | Score |",
            "|-----------|-------:|------:|",
            f"| Mandatory requirements | {score.mandatory_weight} | {score.mandatory_score:.2f} |",
            f"| Preferred requirements | {score.preferred_weight} | {score.preferred_score:.2f} |",
            f"| Evidence quality / confidence | {score.confidence_weight} | {score.confidence_score:.2f} |",
            f"| **Total** (rounded to one decimal) | 100 | **{score.total:.1f}** |",
            "",
            f"**Fit band:** {score.band.value}",
            "",
            "_Component scores are shown to two decimals for display; only the total is rounded under the standard._",
        ]
    )


def _gaps(result: AssessmentResult) -> str:
    lines = [f"## {SECTION_TITLES[3]}", "", "**Mandatory (⚠ MANDATORY GAP):**", ""]
    lines += _requirement_lines(result, result.mandatory_gaps) or [NONE_LINE]
    lines += ["", "**Preferred:**", ""]
    lines += _requirement_lines(result, result.preferred_gaps) or [NONE_LINE]
    return "\n".join(lines)


def _items_to_verify(result: AssessmentResult) -> str:
    lines = [f"## {SECTION_TITLES[4]}", ""]
    by_id = {a.requirement_id: a for a in result.assessments}
    for line, req_id in zip(_requirement_lines(result, result.items_to_verify), result.items_to_verify):
        lines += [line, f"  - Question for the candidate: {by_id[req_id].verification_question}"]
    if not result.items_to_verify:
        lines.append(NONE_LINE)
    return "\n".join(lines)


def _verbatim(title: str, body: str) -> str:
    return f"## {title}\n\n{body.strip()}"


def _uncertainties(result: AssessmentResult) -> str:
    lines = [f"## {SECTION_TITLES[7]}", ""]
    lines += [f"- {item}" for item in result.submission.uncertainties] or [NONE_LINE]
    notes = [(a.requirement_id, a.uncertainty) for a in result.assessments if a.uncertainty]
    if notes:
        lines += ["", "**Per-requirement notes:**", ""]
        lines += [f"- **{req_id}:** {note}" for req_id, note in notes]
    return "\n".join(lines)


def _requirement_lines(result: AssessmentResult, ids: tuple[str, ...]) -> list[str]:
    text = {req.id: req.text for req in result.requirements}
    return [f"- **{req_id}** — {text[req_id]}" for req_id in ids]


def _footer() -> str:
    return (
        "---\n\n"
        "_Rendered deterministically by the Job Fit Evaluator framework. Statuses, evidence grades, "
        "rationale and narrative sections were supplied by the assessor; the framework validated "
        "citations and calculated scores but made no semantic judgements._"
    )


def _cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\r", "").replace("\n", "<br>").strip()
