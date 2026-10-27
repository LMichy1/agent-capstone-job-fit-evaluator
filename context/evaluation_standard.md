# Evaluation Standard — Job Fit Assessment

**Version:** 0.1 (Milestone 1 draft, initial model, subject to revision after Run 1)

This standard defines how a candidate is assessed against a job description. It
applies to both human reviewers and the agent. The scoring engine that applies it
is built in Milestone 2.

## 1. Core rule: no fabrication

The assessment may only state what the candidate materials support.

- Never present a skill, technology, responsibility, duration, achievement,
  certification or metric as fact unless the candidate materials support it.
- Never infer professional experience from a related technology. For example,
  Flask experience is not Django experience, and Docker Compose on a personal
  project is not production containerisation.
- When evidence is missing, weak or ambiguous, use `UNSUPPORTED` or `UNCLEAR`.
  Do not round up.
- Evidence about the candidate must come from the candidate's own materials.

## 2. Requirement types

| Type          | Source in the job description                                    |
|---------------|------------------------------------------------------------------|
| **Mandatory** | Requirements listed as mandatory or required. |
| **Preferred** | Requirements listed as preferred, nice to have, or a plus.       |

When a requirement's type is ambiguous, record the ambiguity and treat it as
mandatory. Being conservative here protects against overstating fit.

## 3. Evidence statuses

Each requirement receives exactly one status.

| Status                | Definition | Typical signals |
|-----------------------|------------|-----------------|
| `SUPPORTED`           | The CV contains direct, specific evidence that meets the **whole** requirement in the context it asks for (e.g. professional when it says professional). | A concrete activity in a professional role that matches the requirement's scope and duration. |
| `PARTIALLY_SUPPORTED` | The CV contains direct evidence for **part** of the requirement, or meets it in a weaker context than required. | Part of a compound requirement is met; the experience is from a personal project or education; the duration falls short. |
| `UNSUPPORTED`         | The CV contains **no** evidence for the requirement. | Not mentioned at all, or mentioned only as a goal or as work in progress. |
| `UNCLEAR`             | Evidence exists but is too ambiguous to judge either way. | A keyword appears only in a skills list; wording is vague (e.g. "significantly improved"); dates or employment type make the duration impossible to confirm. |

### Decision rules

1. Use the most conservative status that is defensible. If the choice is between
   `SUPPORTED` and `PARTIALLY_SUPPORTED`, choose `PARTIALLY_SUPPORTED`.
2. A keyword in a skills list with no supporting experience is `UNCLEAR`, never
   `SUPPORTED`.
3. A certification or degree that is "in progress" does not satisfy a
   requirement for that certification or degree.
4. Compound requirements ("A and B", "A including B") are `SUPPORTED` only when
   every part is evidenced.
5. Durations must be calculable from the CV. Part-time roles, overlapping roles
   and internships must be flagged, not counted silently as full-time years.
6. "Present" is interpreted relative to the CV's stated last-updated date, not
   today's date. If the CV has no date, duration is `UNCLEAR`.

## 4. Evidence citation

Every status other than `UNSUPPORTED` must cite its evidence:

- **Location:** the section and role or entry in the CV (e.g. *Professional
  experience → Software Engineer, Example Logistics Ltd*).
- **Quote:** a short verbatim excerpt.
- **Reasoning:** one or two sentences on why the evidence earns this status.

An `UNSUPPORTED` status must name what was searched for and confirm that it was
not found.

## 5. Evidence quality grades

Each requirement also receives an evidence-quality grade, used in the
confidence component of the score.

| Grade | Meaning | Value |
|-------|---------|-------|
| **A** | Direct, specific evidence from a professional role. | 1.0 |
| **B** | Indirect or weaker evidence: a personal project, education, part-time or internship context, or vague wording. | 0.5 |
| **C** | Skills-list keyword only, or no evidence. | 0.0 |

## 6. Scoring model (initial)

The total score is out of 100 and has three components.

| Component                     | Weight |
|-------------------------------|--------|
| Mandatory requirements        | 70     |
| Preferred requirements        | 20     |
| Evidence quality / confidence | 10     |

### Status credit

| Status                | Credit |
|-----------------------|--------|
| `SUPPORTED`           | 1.0    |
| `PARTIALLY_SUPPORTED` | 0.5    |
| `UNCLEAR`             | 0.0    |
| `UNSUPPORTED`         | 0.0    |

`UNCLEAR` earns no credit because the score must not reward unverified claims.
`UNCLEAR` and `UNSUPPORTED` differ in the narrative: an unclear item is something
to verify with the candidate, while an unsupported item is a genuine gap.

### Formulas

All requirements within a category carry equal weight.

```
mandatory_score  = 70 × (sum of mandatory credits ÷ number of mandatory requirements)
preferred_score  = 20 × (sum of preferred credits ÷ number of preferred requirements)
confidence_score = 10 × (sum of evidence-quality values ÷ number of all requirements)
total            = mandatory_score + preferred_score + confidence_score
```

If the job has no preferred requirements, the mandatory weight becomes 90.
Round only the final total, to one decimal place.

### Fit bands

| Total   | Band          |
|---------|---------------|
| ≥ 75    | Strong fit    |
| 55–74.9 | Moderate fit  |
| < 55    | Weak fit      |

### Mandatory gap override

If any mandatory requirement is `UNSUPPORTED`, the assessment must state a
**mandatory gap** prominently, whatever the band. The band is not changed
automatically, but the recommendation must address the gap.

### Worked example (illustrative numbers only)

A job has 4 mandatory and 2 preferred requirements.

- Mandatory: SUPPORTED, SUPPORTED, PARTIALLY_SUPPORTED, UNCLEAR → credits 2.5 / 4
  → 70 × 0.625 = **43.75**
- Preferred: PARTIALLY_SUPPORTED, UNSUPPORTED → credits 0.5 / 2
  → 20 × 0.25 = **5.0**
- Evidence quality for the 6 requirements: A, A, B, C, B, C → 2.0 / 6
  → 10 × 0.333… = **3.33**
- Total = 52.08 → **52.1, Weak fit**

## 7. Required output sections

A complete assessment contains:

1. Sources inspected, listing which files were used and which were excluded.
2. A requirements table: ID, requirement, type, status, evidence-quality grade,
   evidence location, quote and reasoning.
3. The score breakdown by component, total and band.
4. Genuine gaps: `UNSUPPORTED` mandatory and preferred requirements.
5. Items to verify: `UNCLEAR` requirements, with a suggested question for the
   candidate.
6. Recommended positioning: how the candidate can honestly present their
   strengths, using only supported evidence.
7. Application brief: a short evidence-backed summary with no unsupported
   claims.
8. Uncertainties and assumptions made during the assessment.
