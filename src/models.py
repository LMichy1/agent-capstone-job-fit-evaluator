"""Typed data models for the Job Fit Evaluator.

These are plain containers. Semantic judgements (statuses, grades, rationale)
are supplied by an external agent; nothing here derives them.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class FrameworkError(Exception):
    """Base class for all errors raised by the framework."""


class ParseError(FrameworkError):
    """A context file is missing a required section or is malformed."""


class AssessmentValidationError(FrameworkError):
    """A structured assessment failed validation. Holds every problem found."""

    def __init__(self, errors: list[str]) -> None:
        self.errors = list(errors)
        bullet_list = "\n".join(f"  - {error}" for error in self.errors)
        super().__init__(f"{len(self.errors)} validation error(s):\n{bullet_list}")


class ScoringError(FrameworkError):
    """Scores cannot be calculated under the evaluation standard."""


class Status(str, Enum):
    SUPPORTED = "SUPPORTED"
    PARTIALLY_SUPPORTED = "PARTIALLY_SUPPORTED"
    UNSUPPORTED = "UNSUPPORTED"
    UNCLEAR = "UNCLEAR"


class EvidenceGrade(str, Enum):
    A = "A"
    B = "B"
    C = "C"


class RequirementType(str, Enum):
    MANDATORY = "mandatory"
    PREFERRED = "preferred"


class RequirementOrigin(str, Enum):
    LISTED = "listed"  # parsed from a labelled requirements section
    AGENT_IDENTIFIED = "agent_identified"  # declared by the agent, quoted from the JD


class FitBand(str, Enum):
    STRONG = "Strong fit"
    MODERATE = "Moderate fit"
    WEAK = "Weak fit"


@dataclass(frozen=True)
class Requirement:
    id: str
    text: str
    type: RequirementType
    origin: RequirementOrigin = RequirementOrigin.LISTED
    source_quote: str | None = None  # set only for agent-identified requirements


@dataclass(frozen=True)
class JobDescription:
    title: str
    requirements: tuple[Requirement, ...]
    text: str


@dataclass(frozen=True)
class CVSection:
    heading: str
    level: int
    body: str
    parent_heading: str | None


@dataclass(frozen=True)
class CVDocument:
    sections: tuple[CVSection, ...]
    text: str


@dataclass(frozen=True)
class Evidence:
    location: str
    quote: str


@dataclass(frozen=True)
class RequirementAssessment:
    requirement_id: str
    status: Status
    evidence_grade: EvidenceGrade
    evidence: tuple[Evidence, ...]
    rationale: str
    uncertainty: str = ""
    verification_question: str = ""


@dataclass(frozen=True)
class ExcludedSource:
    path: str
    reason: str


@dataclass(frozen=True)
class AssessmentSubmission:
    """Everything the external agent supplies, after structural loading."""

    candidate_id: str
    sources_inspected: tuple[str, ...]
    sources_excluded: tuple[ExcludedSource, ...]
    additional_requirements: tuple[Requirement, ...]
    assessments: tuple[RequirementAssessment, ...]
    positioning: str
    application_brief: str
    uncertainties: tuple[str, ...]


@dataclass(frozen=True)
class ScoreBreakdown:
    mandatory_weight: int
    preferred_weight: int
    confidence_weight: int
    mandatory_score: float
    preferred_score: float
    confidence_score: float
    total_unrounded: float
    total: float  # rounded to one decimal place, half-up
    band: FitBand


@dataclass(frozen=True)
class AssessmentResult:
    candidate_id: str
    job_title: str
    requirements: tuple[Requirement, ...]
    assessments: tuple[RequirementAssessment, ...]  # same order as requirements
    score: ScoreBreakdown
    mandatory_gaps: tuple[str, ...]
    preferred_gaps: tuple[str, ...]
    items_to_verify: tuple[str, ...]
    submission: AssessmentSubmission
