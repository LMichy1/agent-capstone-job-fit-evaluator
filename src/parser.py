"""Deterministic parsing of the structured context files and assessment JSON.

Every function takes an explicit path from the caller. Nothing here scans
directories or discovers files, so the same code can run against an isolated
run workspace. Nothing here judges whether CV content satisfies a requirement.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .models import (
    AssessmentSubmission,
    CVDocument,
    CVSection,
    Evidence,
    EvidenceGrade,
    ExcludedSource,
    JobDescription,
    ParseError,
    AssessmentValidationError,
    Requirement,
    RequirementAssessment,
    RequirementOrigin,
    RequirementType,
    Status,
)

SCHEMA_VERSION = 1

REQUIREMENT_SECTIONS = {
    "mandatory requirements": (RequirementType.MANDATORY, re.compile(r"^M[1-9]\d*$")),
    "preferred requirements": (RequirementType.PREFERRED, re.compile(r"^P[1-9]\d*$")),
}
AGENT_REQUIREMENT_ID = re.compile(r"^A[1-9]\d*$")

_HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
# "1. **M1** — text"; the dash may be an em dash, en dash or hyphen.
_REQUIREMENT_ITEM = re.compile(r"^\d+\.\s+\*\*(?P<id>[^*]+)\*\*\s+[—–-]\s+(?P<text>\S.*)$")
_DASHES = re.compile(r"[—–]")
_WHITESPACE = re.compile(r"\s+")


# --- Normalisation (section-name lookup and diagnostic hints only) ----------
# Never used for quote or location validation, which are exact.


def normalise_text(text: str) -> str:
    """Remove Markdown emphasis/code markers, unify dashes, collapse whitespace."""
    text = text.replace("*", "").replace("`", "")
    text = _DASHES.sub("-", text)
    return _WHITESPACE.sub(" ", text).strip()


def normalise_heading(heading: str) -> str:
    return normalise_text(heading).casefold()


def _read(path: Path | str) -> str:
    path = Path(path)
    if not path.is_file():
        raise ParseError(f"File not found: {path}")
    return path.read_text(encoding="utf-8")


def _headings(lines: list[str]) -> list[tuple[int, int, str]]:
    """Return (line_index, level, heading_text) for every Markdown heading."""
    found = []
    for index, line in enumerate(lines):
        match = _HEADING.match(line)
        if match:
            found.append((index, len(match.group(1)), match.group(2).strip()))
    return found


# --- Job description ----------------------------------------------------------


def parse_job_description(path: Path | str) -> JobDescription:
    """Extract labelled mandatory and preferred requirements from a job description."""
    text = _read(path)
    lines = text.splitlines()
    headings = _headings(lines)

    title = next((heading for _, level, heading in headings if level == 1), "")
    if not title:
        raise ParseError(f"{path}: no level-1 title heading found")

    requirements: list[Requirement] = []
    for section_name, (req_type, id_pattern) in REQUIREMENT_SECTIONS.items():
        body = _section_lines(lines, headings, section_name, path)
        requirements.extend(_parse_requirement_items(body, req_type, id_pattern, section_name, path))

    _reject_duplicate_ids([req.id for req in requirements], path)
    return JobDescription(title=title, requirements=tuple(requirements), text=text)


def _section_lines(
    lines: list[str], headings: list[tuple[int, int, str]], name: str, path: Path | str
) -> list[str]:
    matches = [(i, level) for i, level, heading in headings if normalise_heading(heading) == name]
    if not matches:
        raise ParseError(f"{path}: required section '## {name.capitalize()}' is missing")
    if len(matches) > 1:
        raise ParseError(f"{path}: section '{name}' appears {len(matches)} times")
    start, level = matches[0]
    end = next((i for i, lvl, _ in headings if i > start and lvl <= level), len(lines))
    return lines[start + 1 : end]


def _parse_requirement_items(
    body: list[str],
    req_type: RequirementType,
    id_pattern: re.Pattern[str],
    section_name: str,
    path: Path | str,
) -> list[Requirement]:
    items: list[tuple[str, list[str]]] = []
    for line in body:
        if not line.strip():
            continue
        match = _REQUIREMENT_ITEM.match(line)
        if match:
            items.append((match.group("id").strip(), [match.group("text").strip()]))
        elif line[:1].isspace() and items:
            items[-1][1].append(line.strip())  # wrapped continuation line
        else:
            raise ParseError(
                f"{path}: unexpected line in '{section_name}' (expected "
                f"'N. **ID** — text' or an indented continuation): {line.strip()!r}"
            )
    if not items:
        raise ParseError(f"{path}: section '{section_name}' contains no requirements")

    requirements = []
    for req_id, text_parts in items:
        if not id_pattern.match(req_id):
            raise ParseError(
                f"{path}: malformed requirement ID {req_id!r} in '{section_name}' "
                f"(expected pattern {id_pattern.pattern})"
            )
        requirements.append(Requirement(id=req_id, text=" ".join(text_parts), type=req_type))
    return requirements


def _reject_duplicate_ids(ids: list[str], source: Path | str) -> None:
    duplicates = sorted({req_id for req_id in ids if ids.count(req_id) > 1})
    if duplicates:
        raise ParseError(f"{source}: duplicate requirement ID(s): {', '.join(duplicates)}")


# --- Candidate CV -------------------------------------------------------------


def parse_cv(path: Path | str) -> CVDocument:
    """Split a CV into heading-delimited sections for evidence-reference checks.

    Each section's body runs to the next heading of the same or higher level,
    so a level-2 section includes its level-3 subsections. Bodies are exact
    slices of the source text, line terminators included.
    """
    text = _read(path)
    lines = text.splitlines()
    raw_lines = text.splitlines(keepends=True)
    headings = _headings(lines)
    if not any(level == 2 for _, level, _ in headings):
        raise ParseError(f"{path}: CV has no level-2 sections to cite as evidence locations")

    sections = []
    parents: dict[int, str] = {}
    for position, (start, level, heading) in enumerate(headings):
        end = next((i for i, lvl, _ in headings[position + 1 :] if lvl <= level), len(lines))
        parent = next((parents[lvl] for lvl in range(level - 1, 0, -1) if lvl in parents), None)
        parents = {lvl: name for lvl, name in parents.items() if lvl < level}
        parents[level] = heading
        sections.append(
            CVSection(heading=heading, level=level, body="".join(raw_lines[start + 1 : end]), parent_heading=parent)
        )
    return CVDocument(sections=tuple(sections), text=text)


# --- Structured assessment (JSON) ---------------------------------------------

_TOP_LEVEL_KEYS = {
    "schema_version",
    "candidate_id",
    "sources_inspected",
    "sources_excluded",
    "additional_requirements",
    "assessments",
    "positioning",
    "application_brief",
    "uncertainties",
}
_ASSESSMENT_KEYS = {
    "requirement_id",
    "status",
    "evidence_grade",
    "evidence",
    "rationale",
    "uncertainty",
    "verification_question",
}
_ADDITIONAL_REQUIREMENT_KEYS = {"id", "type", "text", "source_quote"}
_EVIDENCE_KEYS = {"location", "quote"}
_EXCLUDED_KEYS = {"path", "reason"}


def load_assessment(path: Path | str) -> AssessmentSubmission:
    """Load an agent-supplied assessment JSON file, checking structure only.

    Every structural problem is collected and raised together. Unknown keys are
    rejected rather than ignored so that typos cannot silently drop data.
    """
    try:
        data = json.loads(_read(path))
    except json.JSONDecodeError as exc:
        raise AssessmentValidationError([f"{path}: invalid JSON: {exc}"]) from exc

    errors: list[str] = []
    if not isinstance(data, dict):
        raise AssessmentValidationError([f"{path}: top level must be a JSON object"])

    _check_keys(data, _TOP_LEVEL_KEYS, _TOP_LEVEL_KEYS - {"uncertainties", "additional_requirements"}, "top level", errors)
    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}, got {data.get('schema_version')!r}")

    submission = AssessmentSubmission(
        candidate_id=_string(data, "candidate_id", "top level", errors),
        sources_inspected=tuple(_string_list(data, "sources_inspected", errors)),
        sources_excluded=tuple(_excluded_sources(data.get("sources_excluded"), errors)),
        additional_requirements=tuple(_additional_requirements(data.get("additional_requirements", []), errors)),
        assessments=tuple(_assessments(data.get("assessments"), errors)),
        positioning=_string(data, "positioning", "top level", errors),
        application_brief=_string(data, "application_brief", "top level", errors),
        uncertainties=tuple(_string_list(data, "uncertainties", errors, required=False)),
    )
    if errors:
        raise AssessmentValidationError(errors)
    return submission


def _check_keys(obj: dict[str, Any], allowed: set[str], required: set[str], where: str, errors: list[str]) -> None:
    for key in sorted(set(obj) - allowed):
        errors.append(f"{where}: unknown field {key!r}")
    for key in sorted(required - set(obj)):
        errors.append(f"{where}: missing required field {key!r}")


def _string(obj: dict[str, Any], key: str, where: str, errors: list[str], required: bool = True) -> str:
    if key not in obj:  # absence of a required key is reported by _check_keys
        return ""
    value = obj[key]
    if value is None and not required:
        return ""
    if not isinstance(value, str) or (required and not value.strip()):
        errors.append(f"{where}: field {key!r} must be a non-empty string")
        return ""
    return value.strip()


def _string_list(obj: dict[str, Any], key: str, errors: list[str], required: bool = True) -> list[str]:
    if key not in obj:  # absence of a required key is reported by _check_keys
        return []
    value = obj[key]
    if not isinstance(value, list) or not all(isinstance(v, str) and v.strip() for v in value):
        errors.append(f"top level: field {key!r} must be a list of non-empty strings")
        return []
    if required and not value:
        errors.append(f"top level: field {key!r} must not be empty")
    return [v.strip() for v in value]


def _objects(value: Any, key: str, errors: list[str]) -> list[dict[str, Any]]:
    if value is None:  # absence is reported by _check_keys
        return []
    if not isinstance(value, list):
        errors.append(f"top level: field {key!r} must be a list")
        return []
    objects = []
    for index, item in enumerate(value):
        if isinstance(item, dict):
            objects.append(item)
        else:
            errors.append(f"{key}[{index}]: must be a JSON object")
    return objects


def _excluded_sources(value: Any, errors: list[str]) -> list[ExcludedSource]:
    sources = []
    for index, item in enumerate(_objects(value, "sources_excluded", errors)):
        where = f"sources_excluded[{index}]"
        _check_keys(item, _EXCLUDED_KEYS, _EXCLUDED_KEYS, where, errors)
        sources.append(ExcludedSource(path=_string(item, "path", where, errors), reason=_string(item, "reason", where, errors)))
    return sources


def _additional_requirements(value: Any, errors: list[str]) -> list[Requirement]:
    requirements = []
    for index, item in enumerate(_objects(value, "additional_requirements", errors)):
        where = f"additional_requirements[{index}]"
        _check_keys(item, _ADDITIONAL_REQUIREMENT_KEYS, _ADDITIONAL_REQUIREMENT_KEYS, where, errors)
        req_id = _string(item, "id", where, errors)
        if req_id and not AGENT_REQUIREMENT_ID.match(req_id):
            errors.append(f"{where}: id {req_id!r} must match {AGENT_REQUIREMENT_ID.pattern}")
        req_type = _enum(item, "type", RequirementType, where, errors)
        requirements.append(
            Requirement(
                id=req_id,
                text=_string(item, "text", where, errors),
                type=req_type or RequirementType.MANDATORY,
                origin=RequirementOrigin.AGENT_IDENTIFIED,
                source_quote=_string(item, "source_quote", where, errors),
            )
        )
    return requirements


def _assessments(value: Any, errors: list[str]) -> list[RequirementAssessment]:
    assessments = []
    for index, item in enumerate(_objects(value, "assessments", errors)):
        req_id = item.get("requirement_id")
        where = f"assessments[{index}]" + (f" ({req_id})" if isinstance(req_id, str) else "")
        _check_keys(item, _ASSESSMENT_KEYS, {"requirement_id", "status", "evidence_grade", "evidence", "rationale"}, where, errors)
        status = _enum(item, "status", Status, where, errors)
        grade = _enum(item, "evidence_grade", EvidenceGrade, where, errors)
        assessments.append(
            RequirementAssessment(
                requirement_id=_string(item, "requirement_id", where, errors),
                status=status or Status.UNCLEAR,
                evidence_grade=grade or EvidenceGrade.C,
                evidence=tuple(_evidence(item.get("evidence"), where, errors)),
                rationale=_string(item, "rationale", where, errors),
                uncertainty=_string(item, "uncertainty", where, errors, required=False),
                verification_question=_string(item, "verification_question", where, errors, required=False),
            )
        )
    return assessments


def _evidence(value: Any, where: str, errors: list[str]) -> list[Evidence]:
    if value is None:  # absence is reported by _check_keys
        return []
    if not isinstance(value, list):
        errors.append(f"{where}: field 'evidence' must be a list (use [] when there is none)")
        return []
    evidence = []
    for index, item in enumerate(value):
        item_where = f"{where} evidence[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{item_where}: must be a JSON object")
            continue
        _check_keys(item, _EVIDENCE_KEYS, _EVIDENCE_KEYS, item_where, errors)
        evidence.append(
            Evidence(location=_string(item, "location", item_where, errors), quote=_string(item, "quote", item_where, errors))
        )
    return evidence


def _enum(obj: dict[str, Any], key: str, enum_type: type, where: str, errors: list[str]) -> Any:
    if key not in obj:  # absence is reported by _check_keys
        return None
    raw = obj[key]
    try:
        return enum_type(raw)
    except ValueError:
        allowed = ", ".join(member.value for member in enum_type)
        errors.append(f"{where}: invalid {key} {raw!r} (allowed: {allowed})")
        return None


# --- Evaluation standard (consistency check only) -----------------------------


def parse_standard_constants(path: Path | str) -> dict[str, dict[str, str]]:
    """Read the weight, status-credit and grade-value tables from the standard.

    Used only to detect drift between the document and the evaluator's
    constants; the evaluator never takes its rules from this at run time.
    """
    rows = [_table_cells(line) for line in _read(path).splitlines() if line.lstrip().startswith("|")]
    tables: dict[str, dict[str, str]] = {"weights": {}, "status_credit": {}, "grade_value": {}}
    for cells in rows:
        if len(cells) < 2 or set(cells[0]) <= {"-", ":", " "}:
            continue
        key, last = cells[0], cells[-1]
        if key in {"Mandatory requirements", "Preferred requirements", "Evidence quality / confidence"}:
            tables["weights"][key] = last
        elif key in Status.__members__ and len(cells) == 2:
            tables["status_credit"][key] = last
        elif key in EvidenceGrade.__members__ and len(cells) == 3:
            tables["grade_value"][key] = last
    return tables


def _table_cells(line: str) -> list[str]:
    return [cell.strip().replace("*", "").replace("`", "") for cell in line.strip().strip("|").split("|")]
