# Run 1 vs Run 2 — Comparison and intervention analysis

**Date:** 2026-10-27
**Compared:** `runs/run1/` (baseline) and `runs/run2/`. Both are unedited and
immutable.
**Diagnosis being tested:** `reviews/diagnosis.md` (INS-1, CTX-1, CTX-2, WS-1,
CODE-1).

| Output | Run 1 SHA-256 | Run 2 SHA-256 |
|--------|---------------|---------------|
| `assessment.json` | `e44309982cb70671001960d8da6aa02c55eec1e0128d2f0b7aaf8d3aa695a73c` | `fdfdc78982194394d9d96332850a7119a4e16ee9fe1d6fc19853b06e60ce086b` |
| `trajectory.md` | `244bd30707ceeff88128f1b48a8b8e1373f3078e9c6671f83fc1cce831195a92` | `b1d2aaadc934bb50a6b7fdd637a42cccecadd22983fbe786a7408d40ddea2ee3` |
| scratch artifact | (outside the workspace: `build.py`, `check.py`) | `scratch/validate.py` `acd8fd7a30c9b67506ae7b17c9719fb5e73ae35ec5be81fd3000b8709e935824` |

---

## 1. Executive comparison

Run 2 was produced by a fresh agent after four targeted interventions: two
context clarifications, one instruction change and one workspace change. A
framework fix was also in place.

Compared with Run 1, Run 2:

- **Assessed the whole job description.** It added two requirements from
  outside the numbered lists (A1 and A2). One of them, A1, is an unsupported
  mandatory obligation that is now surfaced as a **mandatory gap**.
- **Resolved the band-deciding ambiguity.** M1 moved from UNCLEAR to SUPPORTED
  by applying the new duration rule explicitly.
- **Applied the parenthetical-list rule explicitly.** P5 kept the same status,
  now on a stated basis.
- **Kept all working files inside the workspace,** in the sanctioned
  `scratch/` directory.

The total rose from **52.1 (Weak fit)** to **61.8 (Moderate fit)**. That
increase is not the measure of success here (see §10). One change was not
targeted by any intervention: P4 moved from PARTIAL to SUPPORTED. It is
recorded as variance, not improvement. Two attribution limits apply:

- the Run 2 kickoff message also mentioned `scratch/`;
- each configuration was run only once.

## 2. Run 1 baseline

| Item | Value |
|------|-------|
| Inputs | Standard `7fa9e229…b045`; prompt `run1_prompt.md` `2f442272…5f9c`; source commit `729cff5` |
| Validator | Exit 0 |
| Score | Mandatory 35.00, preferred 10.00, evidence quality 7.08 → **52.1, Weak fit** |
| Mandatory gap | None |
| `additional_requirements` | 0. Responsibilities were seen but deliberately excluded "because they were not numbered requirements" (trajectory §9). |
| Process | Two helper scripts were created and run in the harness scratchpad **outside** the workspace (WS-1). |

## 3. Run 2 result

| Item | Value |
|------|-------|
| Inputs | Standard `d7627be4…126c`; prompt `run2_prompt.md` `24c1eff5…6e71`; manifest `cf047678…85e4`; source commit `bb46cce` |
| Validator | Exit 0; stderr empty |
| Score | Mandatory 43.75, preferred 11.67, evidence quality 6.43 → **61.8, Moderate fit** |
| Mandatory gap | **A1** |
| `additional_requirements` | 2: A1 (mandatory, on-call rotation) and A2 (mandatory, remote EMEA time zones) |
| Process | 7 tool calls, all inside the workspace. One helper file, `scratch/validate.py`, was retained. `irrelevant_reference.md` and `manifest.json` were not opened. |

## 4. Requirement-level changes

All 12 numbered requirements were compared field by field from the two
assessment files.

| ID | Run 1 status | R1 grade | Run 2 status | R2 grade | Changed? | Explanation |
|----|--------------|:--------:|--------------|:--------:|:--------:|-------------|
| M1 | UNCLEAR | B | **SUPPORTED** | B | **Yes** | CTX-1. Run 2 applied calendar duration: about 40–42 months (at least about 38) across two non-overlapping professional roles. The part-time role is flagged and the internship excluded. Run 1 could not reach a decision without a duration rule. |
| M2 | PARTIALLY_SUPPORTED | A | PARTIALLY_SUPPORTED | A | No | Both: building is evidenced; designing is not stated. |
| M3 | PARTIALLY_SUPPORTED | A | PARTIALLY_SUPPORTED | A | No | Both: schema design and queries are evidenced; no performance tuning. |
| M4 | PARTIALLY_SUPPORTED | A | PARTIALLY_SUPPORTED | A | No | Both: unit tests and CI are evidenced; no integration tests. |
| M5 | SUPPORTED | A | SUPPORTED | A | No | Both: code review in two professional roles. |
| M6 | PARTIALLY_SUPPORTED | A | PARTIALLY_SUPPORTED | A | No | Both: deployment to AWS is evidenced; operating is not. |
| P1 | PARTIALLY_SUPPORTED | B | PARTIALLY_SUPPORTED | B | No | Both: Docker Compose locally on a personal project only. |
| P2 | UNCLEAR | C | UNCLEAR | C | No | Both: Kubernetes appears only in the Skills list. |
| P3 | PARTIALLY_SUPPORTED | B | PARTIALLY_SUPPORTED | B | No | Both: Celery and Redis on a personal project; Kafka in Skills only. |
| P4 | PARTIALLY_SUPPORTED | B | **SUPPORTED** | B | **Yes** | **Untargeted variance** (§7). |
| P5 | PARTIALLY_SUPPORTED | A | PARTIALLY_SUPPORTED | A | No | CTX-2 stabilisation (§6): the same status, now justified by the stated rule. |
| P6 | SUPPORTED | B | SUPPORTED | B | No | Both: BSc 2021; education is grade B. |
| A1 | — | — | **UNSUPPORTED** | C | **New** | INS-1. "- Take part in the team's on-call rotation (roughly one week in six)." No CV evidence. Mandatory gap. |
| A2 | — | — | **SUPPORTED** | B | **New** | INS-1. "- **Location:** Remote (EMEA time zones)", matched by the CV's "- **Location:** Remote, EMEA". |

**Totals:** 2 numbered requirements changed (M1, P4) and 2 requirements were
added (A1, A2). No evidence grade changed on any numbered requirement.

## 5. Score comparison

| Component | Run 1 | Run 2 | Basis in Run 2 |
|-----------|------:|------:|----------------|
| Mandatory (70) | 35.00 | **43.75** | 5.0 credits / 8 mandatory requirements (M1–M6, A1, A2) |
| Preferred (20) | 10.00 | **11.67** | 3.5 / 6 |
| Evidence quality (10) | 7.08 | **6.43** | 9.0 / 14 |
| **Total** | **52.1** | **61.8** | |
| Fit band | Weak fit | **Moderate fit** | |
| Mandatory gap | None | **A1** | |

### Why the total rose although Run 2 found a new unsupported mandatory requirement

This is not a contradiction. The total and the mandatory-gap signal measure
different things, and the scoring model averages over whatever requirement set
is assessed. The in-memory sensitivity figures below were computed with the
evaluator; no file was changed.

| Step | Mandatory | Preferred | Quality | Total | Band | Gap |
|------|----------:|----------:|--------:|------:|------|-----|
| Run 1 baseline | 35.00 | 10.00 | 7.08 | 52.1 | Weak | — |
| + M1 SUPPORTED | 46.67 | 10.00 | 7.08 | 63.8 | Moderate | — |
| + P4 SUPPORTED (= Run 2's numbered requirements only) | 46.67 | 11.67 | 7.08 | 65.4 | Moderate | — |
| + A1 only (UNSUPPORTED/C, mandatory) | 40.00 | 11.67 | 6.54 | 58.2 | Moderate | A1 |
| + A1 and A2 (= Run 2) | 43.75 | 11.67 | 6.43 | **61.8** | **Moderate** | **A1** |

- **M1 is the material improvement (+11.7).** On its own it moves the band from
  Weak to Moderate.
- **P4 adds +1.6.** This is untargeted (§7).
- **A1 lowers the score.** It adds a zero-credit item to the mandatory average
  and a grade-C item to the quality average, and it creates the separate
  mandatory-gap signal.
- **A2 adds supported credit** to the expanded mandatory set and partly offsets
  A1.
- **Net effect of the two additional requirements: −3.6.** So the INS-1
  intervention made the score *more* conservative, not less. The whole
  increase in the total comes from the M1 and P4 status changes.

**The mandatory gap is separate from the band.** Under the standard, a mandatory
gap "must be stated prominently, whatever the band. The band is not changed
automatically." Run 2 is therefore *Moderate fit, with a mandatory gap
(on-call rotation) to resolve*. Neither half of that statement overrides the
other.

## 6. Intervention-by-intervention analysis

### CTX-1 — Experience duration: **SUCCESSFUL INTERVENTION**

- **Intervention:** a standard subsection counting qualifying professional
  experience by calendar duration unless the job description requires full-time
  equivalent. Part-time work counts, there is no full-time-equivalent
  conversion, an unstated full-time label alone does not create uncertainty,
  overlapping periods are not double-counted, "Present" means the CV date, and
  only periods with supported work count.
- **Run 1 evidence:** UNCLEAR, because "the CV gives no hours, and the
  employment type of the Example Logistics Ltd role is not stated, so whether
  the 3-year threshold is met cannot be confirmed". Trajectory §9 named the
  conflict between the "falls short" and "impossible to confirm" signals.
- **Run 2 evidence:**
  - The rationale applies the rules point by point: "Counting calendar
    duration … the periods do not overlap. The standard counts part-time
    professional work by calendar duration, so the 3-year minimum is met. The
    June–August 2020 internship (CSV data scripts, not backend) is excluded."
  - The uncertainty says hours are "not needed since full-time equivalence is
    not required".
  - The part-time role is still flagged (rule 5).
  - Grade B is kept because the threshold depends on the part-time role.
- **Why it counts as a success:** the outcome now follows from a written rule
  that Run 2 visibly applied, not from the agent choosing between readings. The
  remaining uncertainty is about facts (exact days within months), not about
  how to interpret the standard. This was the band-deciding ambiguity
  identified in Milestone 4.

### CTX-2 — Parenthetical lists: **SUCCESSFUL STABILISATION / NO STATUS CHANGE**

- **Intervention:** "e.g." / "such as" introduce examples; "or" introduces
  alternatives; a bare comma list is cumulative scope unless the grammar
  clearly signals examples.
- **Observed:** P5 stayed PARTIALLY_SUPPORTED/A.
- **The rule was applied:** the Run 2 rationale reads "The parenthetical
  '(structured logging, metrics, tracing)' is a bare comma-separated list,
  treated as cumulative scope." Run 2 did not list P5 as an interpretation
  problem; Run 1 had ("could be read as examples or as the full scope").
- **Why it counts as a success:** the aim was to remove the ambiguity, not to
  change the answer. The status is now prescribed rather than chosen.

### INS-1 — Whole-job-description scope: **SUCCESSFUL INTERVENTION**

- **Intervention:** consider every explicit obligation, condition or
  qualification anywhere in the job description. Represent relevant items
  outside the numbered lists in `additional_requirements` with a verbatim
  `source_quote`, or exclude them with a reason in the trajectory. The wording
  named no specific duty.
- **Observed:** `additional_requirements` went from **0 to 2**.
- **The key contrast is not perception.** Run 1 *had seen* the material: its
  trajectory names "on-call rotation" and "working with product managers", and
  its M6 rationale cites on-call. It *deliberately excluded* them because they
  were unnumbered. Run 2 represented the obligation structurally (A1, with a
  validator-accepted verbatim source quote and its own assessment). It also
  documented every other item it considered and excluded, with reasons
  (trajectory §10).
- **Effect:** an unsupported role obligation that Run 1 mentioned only in
  narrative is now a scored requirement and a prominent mandatory gap.
- **Caveat on breadth:** see the A2 assessment in §8.

### WS-1 — Working files: **SUCCESSFUL PROCESS INTERVENTION, WITH AN ATTRIBUTION LIMITATION**

- **Intervention:** an approved, empty `scratch/` in the workspace, plus prompt
  rules confining all helper and intermediate files to it and prohibiting
  harness scratchpads, `/tmp`, the home directory and other outside storage.
- **Observed, from the transcripts:**

  | | Run 1 | Run 2 |
  |---|---|---|
  | Helper files | `build.py` and `check.py` in `/tmp/claude-1000/…run1…/scratchpad/`, outside the workspace | `scratch/validate.py`, inside the workspace, retained and listed in trajectory §11 |
  | Paths in tool calls | Two calls referenced the outside scratchpad | All 7 calls use workspace paths |
  | Inputs not to be used | Not opened | Not opened |

- **Agent behaviour versus harness artifacts:** a harness session scratchpad
  directory exists for Run 2. The harness created it at 14:55:56, before the
  first tool call. It is **empty**, as are its `tasks/` sibling and the project
  memory directory, and no tool call references it. It is a harness-created
  filesystem artifact, **not an agent violation**.
- **Attribution limitation:** the Run 2 kickoff message, which is not part of
  the frozen prompt, said: "If you need helper scripts, temporary files,
  intermediate data, or validation artifacts, put them only inside `scratch/`."
  Run 1's kickoff said only to work within the workspace. The improvement can
  therefore **not** be attributed to `run2_prompt.md` alone. It is attributed
  to the **combined Run 2 instruction setup**: the frozen prompt, the workspace
  design (a sanctioned `scratch/`) and the kickoff message. Removing that
  overlap would need a run without the kickoff sentence.

### CODE-1 — Report renderer: **SUCCESSFUL FRAMEWORK FIX**

The fix was made before Run 2. Run 2 has a real mandatory gap, and
`runs/run2/report.md` renders it in all three intended places:

- the header banner: `> **⚠ MANDATORY GAP:** unsupported mandatory requirement(s): A1.`;
- the A1 row marker;
- the `**Mandatory (⚠ MANDATORY GAP):**` subsection listing A1.

Run 1's re-rendered report shows no warning text. The regression tests cover
no gap, one gap and several gaps.

## 7. Untargeted variance — P4

| | Run 1 | Run 2 |
|---|---|---|
| Status / grade | PARTIALLY_SUPPORTED / B | SUPPORTED / B |
| Evidence | "- Helped onboard two interns to the codebase." | identical |
| Key reasoning | "'Helped' indicates a contributing rather than leading role and no mentoring is described, so applying the conservative rule this is partly supported" | "The requirement accepts mentoring or onboarding as alternatives; helping onboard two interns … is direct evidence of onboarding" |

- **Classification: UNTARGETED JUDGMENT VARIANCE.** No intervention targeted
  P4. The evidence, the requirement text and the relevant rules were the same
  in both runs.
- **Why two conservative assessors differed.**
  - Run 1 read "helped" as a partial contribution, treated P4 as unclear in
    degree, and applied decision rule 1 (prefer PARTIAL when in doubt). Its own
    trajectory notes it "could support the requirement fully".
  - Run 2 read "mentoring **or** onboarding" as alternatives, so any direct
    onboarding evidence meets the requirement. It recorded the "helped"
    wording in the grade (B) and the uncertainty instead.
  - Both readings are defensible.
- **Possible spillover, not demonstrated:** Run 2's phrase "accepts … as
  alternatives" echoes the new CTX-2 wording ("'or' introduces alternatives").
  That rule covers parenthetical lists, and P4 has none. With one run per
  configuration, a CTX-2 spillover cannot be told apart from ordinary
  run-to-run variance.
- **This is not claimed as an improvement.** It shows that agent outputs can
  vary on judgment calls even when the sources and the rules that govern them
  are unchanged. Its effect here is +1.6 points.

## 8. Remaining issues

### A1 — type classification (manager assessment: **follows the written rule; minor residual wording gap**)

- **What Run 2 did:** trajectory §9 says "A1/A2 type: not labelled mandatory or
  preferred; treated as mandatory per the standard's ambiguity rule." The
  top-level uncertainties record the same.
- **The standard (§2):**
  - Mandatory means "Requirements listed as mandatory or required"; Preferred
    means "listed as preferred, nice to have, or a plus".
  - "When a requirement's type is ambiguous, record the ambiguity and treat it
    as mandatory. Being conservative here protects against overstating fit."
- **Assessment:** the on-call duty sits in neither list, so its type is not
  determined by the standard's definitions. Treating that as "ambiguous" and
  applying the conservative tie-break is the natural reading. Run 2 also
  recorded the ambiguity, as the rule requires. The prompt's "based on its
  wording" points the same way: "Take part in the team's on-call rotation" is
  phrased as a duty of the role, not as a nice-to-have. **Run 2 followed the
  written rule.**
- **Residual:** the standard does not say explicitly that "ambiguous type"
  covers items that appear in neither list. Its text deliberately does not
  discuss requirements outside the lists, a standing constraint since
  Milestone 1. The reading is sound but inferred. Recorded as a minor residual
  wording issue, not a defect in Run 2.

### A2 — scope (manager assessment: **DEFENSIBLE BUT DEBATABLE**)

**Arguments for:**
- "Remote (EMEA time zones)" constrains *where and when* the person works,
  which is an explicit condition relevant to fit, as INS-1 asks.
- Run 2 cited matching CV text ("- **Location:** Remote, EMEA"), graded it B
  as a header detail rather than professional evidence, and recorded that the
  specific time zone is unstated.

**Arguments against:**
- It appears in the job description's header metadata block, alongside
  Employer, Team and Level. Run 2 treated those three as descriptive, so the
  line between "descriptor" and "condition" was drawn by judgment.
- It is a **SUPPORTED mandatory** item with grade-B evidence, so including it
  *raises* the score. Without A2, Run 2 would be 58.2 rather than 61.8, still
  Moderate.
- The scope boundary was also applied unevenly:
  - Two items are framed as conditions or duties of the role but were
    excluded: the "quarterly in-person team weeks", treated as a benefit and
    recorded as an uncertainty, and the product-manager duty, treated as a
    post-hire duty.
  - Meanwhile on-call, also a post-hire duty, was included on availability
    grounds.

**Conclusion:**
- **INS-1 did not over-expand into everything:** Run 2 excluded the
  overlapping Responsibilities bullets, post-hire duties, the Level line,
  descriptive context and the benefits section, each with a stated reason.
- **But it is broad enough that the boundary is a judgment call,** and those
  calls can move the score in either direction.
- **Recorded as a residual scope-calibration issue.** A future iteration would
  state which kinds of statement count as assessable conditions (for example
  working-time or location constraints versus benefits and team descriptors)
  without naming specific items.

### Other residual items

- **Single run per configuration.** No change is replicated, and P4 shows that
  variance exists. Attribution in §6 rests on the rationale text, not on
  repetition.
- **Different kickoff messages** (WS-1 limitation above). The kickoff is an
  instruction channel outside the frozen prompt and should be frozen and hashed
  with the workspace in future runs.
- **Carried over from Milestone 4, unchanged by design:**
  - education and personal-detail evidence is capped at grade B;
  - Run 2 also flagged the P1 tension between "Docker Compose on a personal
    project is not production containerisation" and personal projects as a
    PARTIALLY_SUPPORTED signal.
- **Isolation is still procedural, not enforced.** The harness creates an
  outside scratchpad by default; Run 2 simply did not use it.

## 9. What the feedback loop demonstrated

1. **Diagnose before changing.** Each Run 1 problem was traced to a lever, and
   only those levers were changed. Scoring, the CV, the job description and the
   framework stayed fixed, apart from the separate CODE-1 fix.
2. **Different levers fix different failure types.**
   - Context changes resolved *interpretive* uncertainty (M1, P5).
   - The instruction change fixed *task scope* (A1, A2).
   - The workspace change, with the kickoff, fixed *process compliance*.
   - A code fix corrected *presentation*.
3. **The changes are traceable.** Every status change in Run 2 can be tied
   either to the text of an intervention, quoted in the agent's own rationale,
   or to recorded judgment variance.
4. **A higher score is not the target.** The scope intervention lowered the
   score (−3.6) while making the assessment more complete. The duration rule
   raised it by removing an artificial UNCLEAR.
5. **Provenance made the review possible.** Frozen, hashed inputs, preserved
   transcripts converted into observable activity logs, and preserved scratch
   files let each run's claims about its own behaviour be checked rather than
   trusted. That is how WS-1 was found in Run 1 and confirmed fixed in Run 2.

## 10. Manager conclusion

**Run 2 is accepted as the improved assessment, and the intervention cycle is
judged successful.**

Success is **not** judged by the move from 52.1 to 61.8. It is judged on five
criteria, each met:

| Criterion | Evidence |
|-----------|----------|
| More complete task coverage | 0 → 2 additional requirements; every other job-description item outside the numbered lists was considered and its exclusion explained |
| Removal of known ambiguity | M1 decided by the written duration rule; P5 by the written list rule; neither is now an interpretation problem |
| Improved workspace compliance | No outside-workspace files; one helper file in `scratch/`, retained and declared (attribution shared with the kickoff message) |
| Explicit surfacing of unsupported role obligations | On-call rotation is now a mandatory gap (A1) in the scored output, not only a narrative note |
| Traceable differences between runs | Four requirement-level differences, each tied to an intervention or recorded as variance (P4); all inputs and outputs hashed |

**Open items for the capstone package:**
- A2's scope calibration is debatable.
- A1's type rests on an inferred reading of the ambiguity rule.
- There was a single run per configuration.
- The kickoff message overlaps with WS-1.

None of these undermines the comparison. They define where a further iteration
would focus.
