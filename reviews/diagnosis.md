# Run 1 Diagnosis — Context, Workspace and Instructions levers

**Date:** 2026-10-27
**Source:** `reviews/run1_review.md`. Run 1 outputs are unedited (SHA-256 in the
evidence log).
**Status:** Interventions are **planned only**. Apart from the CODE-1 framework
fix, nothing below is implemented in Milestone 4. Context and instruction
changes belong to Run 2 preparation.

## Lever definitions

- **CONTEXT:** what the agent is given to know: the CV, the job description and
  the evaluation standard. A context defect means the materials are missing,
  wrong or ambiguous.
- **WORKSPACE:** the environment the agent works in: the files, tools, writable
  locations and harness defaults available to it.
- **INSTRUCTIONS:** what the agent is told to do: the run prompt and the kickoff
  message.

## Diagnosis table

| ID | Observed problem | Evidence from Run 1 | Lever | Rationale | Planned intervention | Expected Run 2 effect | Success criterion |
|----|------------------|---------------------|-------|-----------|----------------------|-----------------------|-------------------|
| **INS-1** | Explicit role obligations outside the M1–M6 / P1–P6 lists were not assessed. | `"additional_requirements": []`. Trajectory §9: "Responsibilities … (e.g. on-call rotation, working with product managers) are not numbered requirements; they were not added". The M6 rationale cites "on-call" as unevidenced operating work. | **INSTRUCTIONS** | The agent read and understood the job description, so the information was present. The prompt defines the shape of `additional_requirements` and calls it optional ("Leave it as `[]` if you do not use it"), but never says *when* it applies. Treating the numbered lists as the full scope was a reasonable reading of incomplete instructions. | Add a scope rule to the Run 2 prompt: an assessment covers every explicit obligation or condition of the role stated anywhere in the job description. Any not already covered by a numbered requirement is recorded in `additional_requirements` with a verbatim `source_quote`, typed by the standard's existing rule (ambiguous → mandatory). Any deliberately excluded is listed in the trajectory with a reason. The rule must not name or hint at any specific duty, and the standard is not used for this (standing constraint). | The agent searches the whole job description for obligations and records a decision for each, instead of excluding unnumbered duties by default. | Every explicit role obligation outside the numbered lists is either assessed as an `A…` item with a validator-accepted `source_quote`, or excluded with a stated reason. No `A…` item lacks a job-description source. Checked by the manager against expected results held outside the repository. |
| **CTX-1** | M1's status depends on an undefined way of counting experience duration. | M1 is UNCLEAR/B. The rationale says the current role is "about 2 years 3 months"; reaching 3 years "depends on the January 2021 – February 2022 role, which is explicitly part-time", with "no hours". Trajectory §9 notes the conflict between "duration falls short" (PARTIAL) and "impossible to confirm" (UNCLEAR). | **CONTEXT** | The standard requires durations to be "calculable" and part-time roles to be "flagged, not counted silently as full-time years" (rule 5). It does not say whether a threshold means calendar time, full-time equivalent, or only full-time roles. It also does not say whether internships or roles of unstated type count. The same CV facts support UNCLEAR, PARTIALLY_SUPPORTED or SUPPORTED, giving 52.1 (Weak), 57.9 (Moderate) or 63.8 (Moderate) with the grade held at B. The ambiguity alone can change the band. | Add a duration-counting rule to the standard (§3 decision rules). It should define the unit (calendar span of qualifying roles, or full-time equivalent); how part-time roles, internships and roles of unstated employment type are counted; and which status applies when the threshold is met under one counting method but not confirmed under another. Which definition to adopt is a **manager policy decision**, deliberately not pre-empted here. | M1's status follows from a stated rule, not from the agent choosing among readings. The rationale cites the rule. | M1's status and rationale are consistent with the adopted rule and cite it. Any remaining uncertainty is limited to facts the CV really omits (such as hours), not to interpreting the standard. |
| **CTX-2** | A parenthetical list in P5 was read as cumulative sub-requirements. | P5 is PARTIALLY_SUPPORTED/A: "Metrics and tracing tooling are not mentioned … only part of the listed observability scope is evidenced." Trajectory §9: "could be read as examples or as the full scope; it was read as scope". | **CONTEXT** | P5's "(structured logging, metrics, tracing)" has no "e.g." (M3 and P3 use it) and no "or" (M6 uses it). The standard's compound rule (rule 4) covers "A and B" and "A including B" but not parenthetical lists. The requirement is genuinely ambiguous between examples, alternatives and cumulative scope. Impact: SUPPORTED instead of PARTIAL gives 53.8 instead of 52.1; the band is unchanged. | Add an interpretation rule to the standard covering parenthetical lists in requirements: the "e.g."/"such as" form, the "or" form, and the bare-list form. The policy choice for the bare list is a **manager decision**. The job description is not changed. | P5 is classified by a stated rule. Equivalent parenthetical forms are treated consistently. | P5's rationale cites the rule. Its status is the one the rule prescribes for the observed evidence (structured logging only). |
| **WS-1** | The agent created and ran helper scripts outside the workspace. | Trajectory §2 steps 4–5: "Generated `assessment.json` with a script in the session scratchpad (outside the workspace)" and "Ran a validation script (also in the scratchpad)". Confirmed by transcript tool calls 3–4: `build.py` and `check.py` under `/tmp/claude-1000/…/scratchpad/`. | **WORKSPACE** (contributing: INSTRUCTIONS) | The boundary was stated twice and clearly (kickoff message and prompt §2/§3), so this is not mainly an instruction-clarity problem. The environment offered a competing default: the agent harness provides a per-session scratchpad outside the workspace as the place for temporary scripts. This is inferred from the same harness's default guidance in the implementation session; the Run 1 system prompt is not stored in its transcript. The workspace offered no sanctioned writable place for working files and no validator, while prompt §8 asked for a character-by-character self-check. The workspace forced the choice between hand-checking and leaving it. A contributing instruction gap: "do not create any other files" did not say whether temporary working files count. | Give Run 2 a sanctioned working location **inside** the workspace (for example an empty `scratch/` directory, captured as evidence after the run). State explicitly in the prompt that harness scratchpads, `/tmp` and any other location outside the workspace are prohibited, including for temporary scripts. Preserve the session transcript after the run as standard provenance. | Any helper scripts are written inside the workspace, where they are audited and preserved. No tool call touches a path outside the workspace. | The Run 2 transcript's tool calls reference no path outside the workspace. Every non-deliverable file the agent creates is inside the sanctioned location and preserved with hashes. |
| **CODE-1** | The report's gaps section printed "⚠ MANDATORY GAP" when no mandatory gap existed. | `runs/run1/report.md` §4: `**Mandatory (⚠ MANDATORY GAP):**` followed by `_None._`. The header has no gap banner. No mandatory requirement is UNSUPPORTED. | **None (framework defect)**: deterministic code, not a semantic-agent lever | The label was hard-coded in `src/report.py` `_gaps()`. The regression test asserted the absence of `"⚠ MANDATORY GAP:"`, which never matches the label text `"(⚠ MANDATORY GAP):"`, so it passed vacuously. Scoring and statuses are unaffected. | **Implemented in Milestone 4** after this record: the warning label appears only when mandatory gaps exist, with regression tests for no gap, one gap and multiple gaps. | Run 2 reports, and the re-rendered Run 1 report, show the warning only when a mandatory requirement is UNSUPPORTED. | The full unittest suite passes. The re-rendered Run 1 report scores 52.1 / Weak fit and contains no "MANDATORY GAP" text. |

## Findings considered and not raised as defects

These are listed so that the finding count is not inflated, and so that a
reviewer can see they were considered.

- **P6 grade B for a completed degree.** The standard's grade table puts
  education in B, so a degree requirement can never earn grade A. Run 1 applied
  the table as written and flagged it. The impact is about 0.4 confidence
  points. Left for the manager to decide whether the grade table should be
  revised; not diagnosed as a Run 1 problem.
- **Conservative calls on M2, M6 and P4.** These are defensible applications
  of decision rule 1 and the compound rule. They are judgment variance, not
  defects.
- **Score section vs. prompt.** Standard §7 lists a score breakdown, but the
  prompt forbids scores in `assessment.json`. The agent resolved this correctly.
  The output requirements could be worded more precisely in Run 2 preparation,
  but there was no observed harm.
- **`run1_prompt.md` listed in `sources_inspected`.** Harmless.

## Lever summary

| Lever | Findings |
|-------|----------|
| CONTEXT | CTX-1 (band-changing), CTX-2 (minor score effect) |
| WORKSPACE | WS-1 (process integrity; no artifact effect found) |
| INSTRUCTIONS | INS-1 (scope completeness); also contributing to WS-1 |
| Framework (not a lever) | CODE-1 (presentation only; fixed in Milestone 4) |

## Manager decisions for Run 2 (recorded 2026-10-27; planned, not implemented)

These decisions settle the policy choices left open above. They are **not**
yet applied to the standard, the prompt or any workspace. Implementation
belongs to Run 2 preparation.

### CTX-1 — Experience duration

Experience-duration thresholds use the **calendar duration of qualifying
professional experience**, unless the job description explicitly specifies
full-time-equivalent experience.

- Qualifying part-time professional work counts.
- Do not convert part-time work into FTE unless it is explicitly required.
- The absence of an explicit "full-time" label does not, by itself, make a role
  uncertain.
- Do not double-count overlapping periods.
- Use the CV's stated last-updated date for "Present".
- Count only periods for which the relevant type of work is supported.

### CTX-2 — Parenthetical lists

- "e.g." / "such as" → examples, non-exhaustive.
- "or" → alternatives.
- A bare comma-separated list → cumulative listed scope, unless the grammar
  clearly signals examples.

### INS-1 — Requirement scope

Every explicit obligation or condition stated anywhere in the job description
must be considered. Anything outside the numbered requirement list must either:

- be represented using `additional_requirements`; or
- be explicitly excluded, with a reason, in the trajectory.

The Run 2 wording must not name or hint at any specific unnumbered duty.

### WS-1 — Working files

- Run 2 will contain an approved `scratch/` directory.
- Persistent helper scripts, temporary working files and intermediate
  artifacts may exist only inside that directory.
- Harness scratchpads, `/tmp`, home-directory files and any other storage
  outside the workspace are prohibited.

### CODE-1

Already fixed and tested in Milestone 4. No Run 2 action is needed beyond using
the fixed renderer.
