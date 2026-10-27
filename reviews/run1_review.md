# Run 1 Review — Manager review of the first agent draft

**Date:** 2026-10-27
**Reviewed:** `runs/run1/assessment.json` and `runs/run1/trajectory.md`
(byte-identical to the isolated workspace outputs; not edited)
**Supporting evidence:** the deterministic report `runs/run1/report.md`, the
Run 1 session transcript, and the two helper scripts the agent left in its
session scratchpad (all read-only; hashes in `capstone/evidence_log.md`).
**Lever diagnosis:** see `reviews/diagnosis.md`.

| Output | SHA-256 |
|--------|---------|
| `assessment.json` | `e44309982cb70671001960d8da6aa02c55eec1e0128d2f0b7aaf8d3aa695a73c` |
| `trajectory.md` | `244bd30707ceeff88128f1b48a8b8e1373f3078e9c6671f83fc1cce831195a92` |

---

## 1. Executive assessment

Run 1 is a disciplined, conservative first draft. The assessment passed strict
deterministic validation first time: every one of its 22 evidence quotes is
verbatim and in the right CV section, and coverage of the 12 numbered
requirements is complete. It fabricated nothing that this review found. It
handled the skills-list keywords, the in-progress certification, the personal
project, the part-time role and the vague "significantly improved" wording the
way the standard requires. It also recorded its own interpretation problems
openly.

The framework scored it **52.1 / 100, Weak fit, with no mandatory gap**.

Four agent-side issues limit how far the result can be trusted. One is a
deterministic presentation defect in our own framework.

1. **Scope (INS-1).** The agent saw explicit role duties in the job
   description, including an on-call rotation. It chose not to assess them
   because they were not numbered. The instructions gave it a mechanism
   (`additional_requirements`) but no rule for when to use it.
2. **Experience duration (CTX-1).** M1 was marked UNCLEAR because the standard
   does not say whether "3 years" means calendar time or full-time equivalent.
   This single ambiguity is enough to change the fit band.
3. **Parenthetical lists (CTX-2).** P5 was read as requiring all of "structured
   logging, metrics, tracing". The standard does not say how such lists are
   read. The effect on the score is small.
4. **Workspace boundary (WS-1).** The agent wrote and ran two helper scripts in
   a scratchpad outside the workspace. It had been told twice not to. The
   scripts touched only workspace files, so the artifact is unaffected, but the
   process broke the isolation contract.

Separately, **CODE-1:** the report renderer printed "⚠ MANDATORY GAP" on the
gaps sub-heading even though there was no mandatory gap.

## 2. What Run 1 did well

Each item below was checked against the files, not taken from the trajectory.

| Behaviour | Evidence |
|-----------|----------|
| Did not use `irrelevant_reference.md` | Listed in `sources_excluded`. The transcript's six tool calls never read it; it was seen only as a name in `ls -la`. |
| Did not use `manifest.json` as evidence | Listed in `sources_excluded` as "audit metadata, not a source". It was never read. |
| Did not fabricate metrics | "significantly improved test coverage" is not converted into a number. M4 says it "is not credited as a metric". |
| Did not treat the in-progress certification as held | M6 rationale: "The AWS Cloud Practitioner certification is in progress and is not credited." Also recorded in `uncertainties`. |
| Did not credit Skills-list keywords as experience | Kubernetes (P2) → UNCLEAR/C. Kafka (P3) and Docker (P1) are mentioned but not credited. Terraform is not credited anywhere. |
| Did not infer professional experience from related technologies | Docker Compose and Celery on a personal project → PARTIALLY_SUPPORTED/B, explicitly "not production". Flask is not treated as Django. |
| Applied the CV-date rule | "Present" was read as June 2024 (the last-updated date), not today. |
| Flagged the part-time role rather than counting it silently | M1 rationale and `uncertainties`. |
| Applied the compound-requirement rule | M2 (design + build), M3 (schema design + tuning), M4 (unit + integration; tests + CI) and M6 (deploy + operate) each lose credit for the unevidenced part. |
| Preserved uncertainty | 10 per-requirement `uncertainty` notes and 8 top-level `uncertainties`. UNCLEAR items carry specific verification questions. |
| Citations passed strict validation | Exact heading locations, including the em dash and `*(fictional)*` formatting. A multi-line quote keeps its `\n` plus two-space continuation. |
| Produced valid JSON | Schema version 1. No unknown keys. Validator exit 0. |
| Covered all numbered requirements | M1–M6 and P1–P6, each assessed exactly once. |
| Narrative sections stay within cited evidence | Every factual claim in `positioning` and `application_brief` traces to a CV line. Both list the unverified items the candidate should not yet claim. |
| Recorded its own interpretation problems | Trajectory §9 names M1, P5, P6, P4, the unnumbered responsibilities, and the score-section/prompt tension. |
| Accurate trajectory | The six steps in trajectory §2 match the six tool calls in the session transcript one-for-one, including the scratchpad use. |
| Created only the two deliverables inside the workspace | The workspace holds exactly the six inputs plus `assessment.json` and `trajectory.md`. |

## 3. Output problems

### 3.1 Role obligations outside the numbered lists were not assessed (INS-1)

`additional_requirements` is `[]`. Trajectory §9 shows the agent read the
Responsibilities section and decided to exclude it:

> "Responsibilities in the job description (e.g. on-call rotation, working with
> product managers) are not numbered requirements; they were not added as
> additional requirements."

This is not a reading failure. The M6 rationale even uses "on-call" as an
example of operating work. The output is incomplete as a fit assessment,
because explicit obligations of the role are absent from the requirements
table, the gaps and the items to verify. → **INSTRUCTIONS**

### 3.2 M1 status rests on an undefined duration rule (CTX-1)

The agent's arithmetic is correct. The current role (March 2022 – June 2024)
alone is about 2 years 3 months. Adding the part-time role, the calendar span is
about 3 years 5 months. The standard does not define what counts toward the
duration, so the same facts support three different statuses:

| Reading of "at least 3 years" | Plausible status | Total (M1 grade held at B) |
|------------------------------|------------------|----------------------------|
| Full-time-equivalent; part-time hours unknown | UNCLEAR (Run 1) | **52.1 Weak** |
| Only full-time roles count; duration falls short | PARTIALLY_SUPPORTED | 57.9 Moderate |
| Calendar span of qualifying roles, part-time flagged | SUPPORTED | 63.8 Moderate |

Run 1's choice is defensible under decision rule 1, which says to prefer the
conservative status. But the result is not reproducible: a different, equally
compliant agent could cross the Weak/Moderate boundary. → **CONTEXT**

### 3.3 P5 parenthetical read as cumulative scope (CTX-2)

P5 reads: "Experience with observability tooling (structured logging, metrics,
tracing)." Run 1 required all three, so it gave PARTIALLY_SUPPORTED with grade
A, on the strength of structured logging only. The job description itself uses
three conventions for parentheses:

- "e.g." for examples (M3, P3);
- "or" for alternatives (M6);
- a bare list (P5).

The standard's compound-requirement rule covers "A and B" and "A including B",
but not parenthetical lists. → **CONTEXT**. The effect is small: under the
"examples" reading, P5 would be SUPPORTED and the total 53.8, still Weak.

### 3.4 Deterministic report-rendering defect (CODE-1; framework, not agent)

`runs/run1/report.md`, section 4, renders `**Mandatory (⚠ MANDATORY GAP):**`
followed by `_None._`, which contradicts the header. The header correctly shows
no gap banner, and no mandatory requirement is UNSUPPORTED. The cause is a
hard-coded label in `src/report.py` (`_gaps`, line 114). The existing test
missed it: it asserted the absence of `"⚠ MANDATORY GAP:"`, but the label
reads `"(⚠ MANDATORY GAP):"`. This is a framework defect. It is not a lever
diagnosis of the agent. It is fixed in Milestone 4 after being recorded here
(see the evidence log).

## 4. Trajectory and process problems

### 4.1 Helper scripts outside the workspace (WS-1)

Trajectory steps 4–5, confirmed by tool calls 3–4 in the transcript:

- `build.py`, written to the session scratchpad
  `/tmp/claude-1000/-home-ngetich-flow-HamanLabs-agent-capstone-run1/e110aae1-…/scratchpad/`,
  generated `assessment.json`;
- `check.py`, in the same place, validated it.

Both the kickoff message ("Do not access any files, directories … outside this
workspace") and `run1_prompt.md` §2/§3 ("Work only with files in the current
workspace"; "do not create any other files") prohibit this.

- **Impact on the artifact:** none found. The scripts read only
  `candidate_cv.md` and `assessment.json` inside the workspace, and they write
  only `assessment.json`.
- **Impact on the process:** real. Work happened where the audit cannot see
  it, in ephemeral `/tmp` storage. Isolation, which is procedural (Decision
  M2-1), was not respected. The agent disclosed the breach itself, which is to
  its credit. → **WORKSPACE** (see diagnosis).

### 4.2 No other process issues found

The agent read the CV with `cat -A` to confirm the dash characters, read the job
description and standard once, wrote both deliverables and confirmed the file
set. It made no web access, opened no repository paths, and ran no wider file
searches.

## 5. Important judgment calls

These are not defects. They are calls a reviewer should be aware of when
comparing runs.

| Item | Call made | Comment |
|------|-----------|---------|
| M1 | UNCLEAR, grade B; also flagged that the current role is "not stated to be full-time" | Very conservative. The standard does not say whether an unstated employment type means full-time. Folded into CTX-1. |
| M2 | PARTIALLY_SUPPORTED: "designing" is not evidenced | Defensible under the compound rule. A different agent could read "built and maintained REST APIs" as implying design. |
| M6 | PARTIALLY_SUPPORTED: operating in production is not described | Defensible. Overlaps with the unassessed on-call duty (INS-1). |
| P4 | PARTIALLY_SUPPORTED/B: "Helped onboard two interns" | The agent noted it "could support the requirement fully" and applied rule 1. Defensible. |
| P6 | SUPPORTED/B for a completed BSc | The grade table puts education in B, so a degree requirement can never earn A. The agent applied the table as written and flagged it. Confidence impact is about 0.4 points. Recorded as an observation for the manager, not a finding. |
| Scores | Left out of `assessment.json` | Standard §7 lists a score breakdown, but the prompt forbids scores. The agent resolved this correctly and flagged it. |
| `sources_inspected` | Includes `run1_prompt.md` | Harmless. The prompt is instructions, not evidence. |

## 6. Deterministic validation result

```
.venv/bin/python scripts/run_evaluation.py --job context/job_description.md --cv context/candidate_cv.md --assessment runs/run1/assessment.json --standard context/evaluation_standard.md --output runs/run1/report.md
```

- Exit code **0**; stderr empty.
- stdout: `Wrote runs/run1/report.md (total 52.1, Weak fit)`

| Component | Score |
|-----------|-------|
| Mandatory | 35.00 (3.0 / 6) |
| Preferred | 10.00 (3.0 / 6) |
| Confidence | 7.08 (8.5 / 12) |
| **Total** | **52.1 — Weak fit** |

- **Mandatory gap:** none.
- **`additional_requirements`:** `[]`.

## 7. Manager acceptance decision

**Run 1 is accepted as the baseline for the Run 1 / Run 2 comparison.**

Acceptance means the run is valid, complete and honestly recorded, and is
preserved unedited as the reference point. It does **not** endorse its
conclusions. In particular:

- the M1 status and the overall band depend on an ambiguity in the standard
  (CTX-1);
- the requirement scope is incomplete (INS-1);
- the process breached the workspace boundary (WS-1).

These are to be addressed through the levers in `reviews/diagnosis.md`, not by
correcting Run 1.
