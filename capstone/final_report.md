# Agent Capstone — Job Fit Evaluator: Final Report

**Date:** 2026-10-27
**Repository state at writing:** `900f89a` (Milestone 5) plus this Milestone 6
package
**Roles:** manager and reviewer (human); implementation agent (framework,
workspaces, review support); two independent semantic agents (Run 1, Run 2)

---

## 1. Executive summary

**Task.** An AI agent evaluates an anonymised software-engineering candidate
against a job description. It produces a structured, evidence-backed fit
assessment and an application brief. A deterministic Python framework then
validates every citation and calculates the score.

**Why it suits an agentic capstone.** The work is multi-step: read three
sources, extract requirements, judge evidence, cite it verbatim, write
narrative, and check its own output. The result is a reviewable artifact
judged against a written quality bar. The obvious failure, fabricating
experience, is easy to define and to check for.

**Structure.**

1. Run 1 was executed by a fresh agent in an isolated, frozen workspace.
2. The manager reviewed both its output and its trajectory.
3. Each problem was diagnosed against the three levers: **Context**,
   **Workspace** and **Instructions**.
4. Only the diagnosed levers were changed.
5. Run 2 was executed by another fresh agent, and the two runs were compared.

**Central result.**

| | Total | Fit band | Mandatory gap | Additional requirements |
|---|---|---|---|---|
| Run 1 | **52.1** | Weak fit | none | 0 |
| Run 2 | **61.8** | Moderate fit | **A1** (on-call rotation) | 2 |

The fit band and the mandatory gap are **separate signals**. The band comes
from the weighted score. The mandatory-gap signal is raised whenever any
mandatory requirement is UNSUPPORTED, and it never changes the band
automatically. Run 2 is therefore "Moderate fit, with a mandatory gap to
resolve".

**Success is not "the score went up."** The two additional requirements
actually *lowered* the score (§11). Success is measured by:

- **better coverage of the job description:** an explicit role obligation is
  now assessed rather than left out;
- **removal of ambiguous rules:** experience duration and parenthetical lists
  are now defined;
- **better workspace discipline:** no files outside the workspace;
- **explicit surfacing of an unsupported obligation:** A1 as a mandatory gap;
- **traceable change:** every difference between the runs is tied to a
  diagnosed intervention or recorded as variance.

## 2. Task selection

**Task:** evaluate an anonymised software-engineering candidate against a job
description and produce an evidence-backed fit assessment and application
brief.

| Capstone requirement | How the task meets it |
|---|---|
| Multi-step | Reading, requirement extraction, per-requirement judgment, verbatim citation, scoring inputs, narrative, trajectory, self-check |
| Reviewable artifact | `assessment.json`, a strict schema checked by code, plus `trajectory.md`, a process record checked against transcripts |
| Realistic context | A full CV, a job description with mandatory and preferred lists, a written evaluation standard, and a distractor file. The materials are realistic in structure but **synthetic** (see the next row) |
| Known quality bar | `evaluation_standard.md` defines statuses, decision rules, evidence grades, citation rules and scoring before any run |
| Safe, anonymised materials | "Candidate A", fictional employers and a fictional vacancy. No real person's data |

## 3. Context package

| File | Purpose | Run policy |
|---|---|---|
| `candidate_cv.md` | The only evidence about the candidate | Use |
| `job_description.md` | The only source of requirements: M1–M6, P1–P6, plus duties and conditions elsewhere in the text | Use |
| `evaluation_standard.md` | Statuses, decision rules, citation rules, grades, scoring, rounding, bands | Use |
| `irrelevant_reference.md` | Frontend design notes, unrelated to the role | **Supplied deliberately but excluded.** It tests whether the agent respects source boundaries. Neither run opened it. |

**The CV contains realistic evidence-quality challenges:**
- keywords that appear only in the Skills list (Kubernetes, Kafka, Terraform);
- a personal project (Docker Compose, Celery);
- a part-time role held during a degree;
- an internship;
- an AWS certification marked *in progress*;
- vague wording ("significantly improved");
- a "last updated" date (June 2024) that anchors "Present".

**Anti-fabrication rules** (standard §1 and §3; prompt §6):
- never present a skill, duration, metric or certification as fact unless the
  CV supports it;
- never infer professional experience from a related technology (Flask is not
  Django; Docker Compose on a personal project is not production
  containerisation);
- a keyword in the Skills list alone → `UNCLEAR`, never `SUPPORTED`;
- an in-progress certification does not satisfy a requirement;
- `UNCLEAR` earns **zero credit**, so unverified claims are never rewarded;
- the most conservative defensible status wins any tie;
- every non-`UNSUPPORTED` status must cite a verbatim quote under an exact CV
  heading, and the code checks this.

## 4. Workspace design

**Run 1** (`~/HamanLabs/agent-capstone-run1`):
- **Isolation:** an external directory whose parent holds no repository, so the
  agent cannot see the README, the reviews, the tests, the code or the evidence
  log.
- **Contents:** exactly six frozen files: the four context files,
  `run1_prompt.md` and `manifest.json`. The manifest holds each file's SHA-256,
  its role and its source commit (`729cff5`); its own hash is recorded
  externally.
- **Read-only inputs:** mode 444. A fresh agent session was started inside the
  workspace.
- **Pre-run leak check:** a sweep found milestone wording in the standard
  ("draft, subject to revision after Run 1"). It was sanitised and recorded as
  LEAK-1 before any agent saw the workspace.

**Run 2** (`~/HamanLabs/agent-capstone-run2`):
- the same isolation model, rebuilt from committed source `bb46cce`;
- six read-only files: `run2_prompt.md` replaces the Run 1 prompt, alongside
  the updated standard;
- a **sanctioned, writable `scratch/` directory**, which started empty and is
  declared in the manifest as `working_directory`;
- all persistent helper and intermediate files must stay inside the workspace,
  and only in `scratch/`.

**Limitation (stated honestly):** isolation is **procedural, not
container-enforced**. Read-only permissions are a guard, not a guarantee. The
agent harness creates its own session scratchpad under `/tmp` by default, and
nothing technically stops the agent from reading or writing outside the
workspace. Compliance is checked after the run by comparing transcripts with
the files.

## 5. Deterministic framework

The Python 3.10 layer uses only the standard library and makes no LLM or
network calls.

| Component | Role |
|---|---|
| `src/models.py` | Typed dataclasses and enums: requirements, evidence, assessments, scores, errors |
| `src/parser.py` | Parses the job description (requirement IDs and types), the CV (exact heading tree and section bodies), the assessment JSON (unknown keys rejected; all errors collected) and the standard's scoring tables |
| `src/evaluator.py` | Validates coverage and status/grade/evidence consistency. **Exact** heading matching for locations; **verbatim** quote matching, normalising only line endings and surrounding whitespace. Scores with exact fractions and ROUND-HALF-UP; assigns bands; flags mandatory gaps; checks the code's constants against the standard to detect drift |
| `src/report.py` | Renders the eight required report sections deterministically |
| `scripts/run_evaluation.py` | CLI: `--job --cv --assessment [--standard] [--output]`. Exit 0 on success, 1 on a framework error, 2 on a usage error |
| `tests/` | **126 tests, all passing under `unittest`** |

**Architectural boundary:**
- **The Python code never decides whether evidence satisfies a requirement.**
  It does not assign statuses or grades and does no keyword matching.
- **The semantic agent makes every judgment.** The deterministic layer
  validates its form and citations and calculates the score.
- This separation means a format or scoring defect cannot be confused with a
  judgment defect.

**Testing note:** `pytest` was **not available** in the environment. Installing
it needed network access, which was not permitted, so pytest was **never run**.
The tests are `unittest.TestCase` classes, compatible with pytest collection.
The authoritative command is
`.venv/bin/python -m unittest discover -s tests`.

## 6. Run 1

| Item | Result |
|---|---|
| Setup | Fresh session; frozen workspace (`729cff5`); prompt `run1_prompt.md` (`2f442272…5f9c`) |
| Sources inspected | prompt, CV, job description, standard |
| Sources excluded | `irrelevant_reference.md` and `manifest.json`, neither opened (confirmed by transcript) |
| Output validity | Valid on the first attempt: 22 verbatim citations, exact headings, complete coverage of M1–M6 and P1–P6 |
| Score | Mandatory 35.00, preferred 10.00, evidence quality 7.08 → **52.1** |
| Fit band | **Weak fit** |
| Mandatory gap | None |
| `additional_requirements` | 0 |

**Useful behaviours:**
- **no fabricated experience,** and no invented metrics ("significantly
  improved" was not quantified);
- **strict citations** that passed exact-match validation, including em dashes
  and `*(fictional)*` formatting;
- **Skills-list keywords not credited:** Kubernetes → UNCLEAR/C; Kafka and
  Terraform not credited;
- **the in-progress AWS certification was not treated as held;**
- **personal-project and part-time contexts were downgraded** rather than
  treated as professional or full-time;
- **uncertainty preserved:** 10 per-requirement notes and 8 overall
  uncertainties;
- **its own interpretation problems recorded** (M1, P5, P6, P4).

The manager accepted Run 1 as the **baseline**, not as correct (see
`reviews/run1_review.md`).

## 7. Run 1 problems

**Three agent-level findings mapped to the capstone levers:**

- **INS-1:** explicit job-description duties outside the numbered lists were
  seen but excluded. The trajectory says the on-call rotation and
  product-manager work "are not numbered requirements; they were not added".
- **CTX-1:** the standard did not define how experience duration is counted
  (calendar time, full-time equivalent, or full-time only). M1 was UNCLEAR, and
  this one ambiguity alone could move the band from Weak to Moderate.
- **CTX-2:** P5's bare list "(structured logging, metrics, tracing)" was
  ambiguous between examples and cumulative scope.

**One process finding:**

- **WS-1:** helper scripts (`build.py`, `check.py`) were written to and run
  from the harness scratchpad **outside** the workspace, despite the boundary
  being stated in both the kickoff message and the prompt.

**One framework defect, which is not one of the three levers:**

- **CODE-1:** our own renderer printed `**Mandatory (⚠ MANDATORY GAP):**` above
  `_None._` when no gap existed. The label was hard-coded, and the existing
  test had passed vacuously because it looked for the wrong substring. This
  was a defect in the deterministic code, not in the agent's context,
  workspace or instructions, so it was fixed directly.

## 8. Diagnosis

| Finding | Evidence | Lever | Why | Intervention |
|---|---|---|---|---|
| INS-1 | `additional_requirements: []`; trajectory §9 explains the exclusion; the M6 rationale mentions on-call | **Instructions** | The agent read the material. The prompt described the field's format and called it optional, but never said *when* to use it | A whole-job-description scope rule in the Run 2 prompt, naming no specific duty |
| CTX-1 | M1 UNCLEAR; the rationale depends on part-time hours; trajectory §9 notes the conflicting status signals | **Context** | The same facts supported UNCLEAR, PARTIAL or SUPPORTED (52.1, 57.9 or 63.8) | A duration rule in the standard |
| CTX-2 | P5 rationale; trajectory §9 ("could be read as examples or as the full scope") | **Context** | The job description uses "e.g.", "or" and bare lists, and the standard covered none of them | A rule for lists in parentheses in the standard |
| WS-1 | Trajectory steps 4–5; transcript calls 3–4; scripts recovered from `/tmp` | **Workspace** (contributing: Instructions) | The boundary was stated twice, but the environment offered an outside scratchpad by default and the workspace had nowhere sanctioned for working files | A sanctioned `scratch/`, with explicit prohibition of outside storage |
| CODE-1 | `runs/run1/report.md` §4 | **Framework defect** | A hard-coded label, and a vacuous test | Renderer fix plus regression tests |

**Why the trajectory mattered:** Run 1's output validated perfectly, so WS-1
was invisible from the artifact. It was found only by reading the trajectory,
which disclosed the scratchpad, and then confirming it against the session
transcript and the recovered scripts. A review of the output alone would have
passed a run that broke the isolation contract.

## 9. Interventions

Only the following changes were made between the runs. The CV, the job
description, the irrelevant reference, scoring weights, credits, grades, bands,
rounding and citation rules were unchanged.

- **CTX-1** (standard §3, "Experience-duration requirements"):
  - qualifying professional experience is counted by **calendar duration**
    unless the job description explicitly requires full-time equivalent;
  - part-time professional work counts;
  - no conversion to full-time equivalent;
  - an unstated "full-time" label does not by itself create uncertainty;
  - overlapping periods are not double-counted;
  - "Present" means the CV's last-updated date;
  - only periods with supported relevant work count;
  - decision rule 5 (flag part-time and internship periods) still applies.
- **CTX-2** (standard §3, "Lists in parentheses"):
  - "e.g." / "such as" → examples, non-exhaustive;
  - "or" → alternatives;
  - a bare comma list → cumulative listed scope, unless the grammar clearly
    signals examples.
- **INS-1** (prompt §1 "Scope", §4.1, trajectory item 10):
  - consider every explicit obligation, condition or qualification anywhere in
    the job description;
  - represent relevant items outside the lists in `additional_requirements`,
    with a verbatim `source_quote`, a type based on the wording, and their own
    assessment;
  - otherwise record the exclusion and its reason in the trajectory.
- **WS-1** (prompt §2, §3, §8, trajectory item 11; workspace):
  - an empty, writable `scratch/` directory;
  - all helper files, intermediate files and temporary code only in
    `scratch/`;
  - harness scratchpads, `/tmp`, the home directory and other repositories are
    prohibited;
  - every scratch file is declared in the trajectory.
- **CODE-1** (`src/report.py` plus 8 tests): the gap label appears only when a
  mandatory gap exists. Tests cover no gap, one gap and several gaps.

## 10. Run 2

- **Setup:** a fresh agent session in a frozen workspace built from `bb46cce`,
  with a sanctioned `scratch/`. The candidate and job materials were identical
  to Run 1; only the standard and the prompt were updated.
- **Validation:** valid on the first attempt; validator exit 0.
- **Score:** mandatory 43.75, preferred 11.67, evidence quality 6.43 →
  **61.8, Moderate fit**.
- **Mandatory gap:** **A1**, the on-call rotation, UNSUPPORTED/C.
- **Additional requirements:** **A1**, and **A2** (remote work in EMEA time
  zones, SUPPORTED/B).
- **Changed numbered requirements:**
  - **M1:** SUPPORTED/B, by explicit calendar-duration reasoning;
  - **P4:** SUPPORTED/B. **P4 was not targeted by any intervention** (§13).
- **Process:**
  - 7 tool calls, all inside the workspace;
  - one helper file, `scratch/validate.py`, retained and declared;
  - `irrelevant_reference.md` and `manifest.json` were not opened.

## 11. Run 1 vs Run 2 comparison

| | Run 1 | Run 2 |
|---|---|---|
| M1 | UNCLEAR / B | **SUPPORTED / B** |
| P4 | PARTIALLY_SUPPORTED / B | **SUPPORTED / B** |
| A1 | — | **UNSUPPORTED / C** (mandatory) |
| A2 | — | **SUPPORTED / B** (mandatory) |
| Other 10 numbered requirements | — | identical status and grade |
| Additional requirements | 0 | 2 |
| Mandatory / preferred / quality | 35.00 / 10.00 / 7.08 | 43.75 / 11.67 / 6.43 |
| Total, band | 52.1, Weak fit | 61.8, Moderate fit |
| Mandatory gap | none | A1 |

**Score decomposition** (evaluator applied to the run data in memory; no file
changed):

| Step | Total | Band / gap |
|---|---|---|
| Run 1 | 52.1 | Weak |
| Only M1 changed to SUPPORTED | 63.8 | Moderate |
| P4 also changed to SUPPORTED | 65.4 | Moderate |
| Add A1 only | 58.2 | Moderate, gap A1 |
| Add A1 and A2 (= Run 2) | **61.8** | **Moderate, gap A1** |

- **M1 and P4 account for the whole numerical increase.** M1 alone moves the
  band from Weak to Moderate.
- **A1 and A2 together lower the score by 3.6,** relative to the state with
  only the M1 and P4 changes. A1 adds a zero-credit mandatory item and a
  grade-C item; A2 partly offsets it.
- **A1 makes the assessment more complete but creates a mandatory gap.**
- So a higher score is not the measure of a better run. The intervention that
  most improved coverage reduced the number.

## 12. Intervention outcomes

| Lever | Outcome | Evidence |
|---|---|---|
| CTX-1 | **Successful** | Run 2's M1 rationale applies the calendar rule point by point and says hours are "not needed since full-time equivalence is not required". The status now follows from a written rule. |
| CTX-2 | **Successful stabilisation, no status change** | P5 stayed PARTIALLY_SUPPORTED/A, now justified as "a bare comma-separated list, treated as cumulative scope". It is no longer listed as an interpretation problem. |
| INS-1 | **Successful** | 0 → 2 additional requirements. The obligation Run 1 saw but excluded is now a scored requirement and a mandatory gap. Every other excluded item is reasoned in trajectory §10. |
| WS-1 | **Successful, with an attribution limitation** | No outside-workspace files; only `scratch/validate.py`. The empty harness scratchpad was created by the harness, not the agent. |
| CODE-1 | **Successful framework fix** | Run 2's real gap renders in the banner, the row and the subsection; Run 1's report shows none. |

**WS-1 attribution limitation:** the Run 2 kickoff message also told the agent
to put helper files only in `scratch/`. Run 1's kickoff did not. The workspace
improvement is therefore attributed to the **combined** setup (prompt,
workspace design and kickoff instruction), not to the prompt alone.

## 13. Untargeted variance — P4

- **Run 1:** PARTIALLY_SUPPORTED/B. "Helped onboard two interns" was read as a
  contributing role, and the conservative tie-break was applied.
- **Run 2:** SUPPORTED/B. "Mentoring **or** onboarding" was read as
  alternatives, so onboarding evidence meets the requirement. The "helped"
  wording was reflected in grade B and the uncertainty note.
- **No intervention targeted P4.** The evidence, the requirement and the
  governing rules were the same.

**Classification: untargeted judgment variance.** It must not be counted as
intervention-driven improvement:

- there is no diagnosed cause;
- both readings are defensible under the standard;
- with one run per configuration, it cannot be separated from ordinary
  run-to-run variance.

Run 2's phrasing echoes the new CTX-2 "or" rule, but that rule covers only
parenthetical lists, so any spillover is unproven. P4 contributes +1.6 points.

## 14. Residual issues

- **A1 type.** Run 2 followed the conservative rule ("ambiguous type → treat as
  mandatory") and recorded the ambiguity. The standard does not say explicitly
  that an obligation outside both lists counts as "ambiguous type", so the
  reading is sound but inferred.
- **A2 scope: defensible but debatable.**
  - *For:* a real working condition, cautiously graded B.
  - *Against:* it comes from the job description's header block, whose sibling
    lines (Employer, Team, Level) Run 2 treated as descriptive. As a supported
    mandatory item it *raises* the score (58.2 → 61.8).
- **Scope calibration.** The whole-job-description rule worked, but its
  boundary is a judgment call: in-person team weeks and the product-manager
  duty were excluded while on-call was included. A future iteration should
  state which *kinds* of statement are assessable conditions without naming
  specific items.
- **Procedural isolation.** It is not container-enforced, and the harness
  creates an outside scratchpad by default.
- **One run per configuration.** The experiment cannot separate ordinary agent
  variance from intervention effects with statistical confidence. Attribution
  rests on the rationale text matching the intervention text.
- **The kickoff message is not frozen** with the workspace, and it differed
  between the runs.

## 15. What the feedback loop demonstrated

- **A good output is not enough.** Run 1's output validated perfectly but
  broke the workspace boundary.
- **The trajectory matters.** It revealed WS-1, the deliberate scope exclusion
  (INS-1) and the agent's own interpretation problems (CTX-1, CTX-2).
- **Context ambiguity can change conclusions.** One undefined duration rule was
  enough to decide the fit band.
- **Instruction scope determines coverage.** The agent covered exactly what it
  was told was in scope. Run 1 saw the on-call duty and still left it out.
- **Workspace design affects process compliance.** Giving the agent a
  sanctioned place for working files removed the reason to go outside.
- **Deterministic validation separates the kinds of correctness.** Format,
  citation and scoring errors are caught by code, so the review can focus on
  semantic judgment.
- **Iterate on diagnosed levers.** Changing only four targeted things made each
  Run 2 difference explainable. Rewriting everything would have made the
  comparison uninterpretable.

## 16. Evidence index

**Commits:**

| Commit | Content |
|---|---|
| `a27f9ab` | Milestone 1 baseline: context package, standard, project structure |
| `b14842a` | Workspace isolation strategy documented |
| `0beeff5` | Milestone 2: deterministic framework and tests |
| `729cff5` | Context sanitisation before Run 1 (LEAK-1) |
| `054bf89` | Run 1 workspace freeze (Milestone 3A) |
| `2e255ef` | Run 1 preservation (Milestone 3B) |
| `238fb83` | Run 1 review and diagnosis; CODE-1 fix (Milestone 4) |
| `bb46cce` | Run 2 preparation: standard and prompt (Milestone 5A) |
| `c2e52f0` | Run 2 workspace freeze record (Milestone 5A) |
| `900f89a` | Run 2 execution, preservation and comparison (Milestone 5) |

**Artifacts:**

| Path | Content |
|---|---|
| `prompts/run1_prompt.md` | Frozen Run 1 instructions (`2f442272…5f9c`) |
| `prompts/run2_prompt.md` | Frozen Run 2 instructions (`24c1eff5…6e71`) |
| `context/` | CV, job description, standard (Run 2 version `d7627be4…126c`), irrelevant reference |
| `runs/run1/` | `assessment.json` (`e4430998…a73c`), `trajectory.md` (`244bd307…5a92`), reports before and after the CODE-1 fix, `provenance/` (activity log, recovered scripts, hashes) |
| `runs/run2/` | `assessment.json` (`fdfdc789…6086b`), `trajectory.md` (`b1d2aaad…2ee3`), `report.md`, `provenance/` (activity log, `scratch/validate.py` `acd8fd7a…5824`, hashes) |
| `reviews/run1_review.md` | Manager review of Run 1 |
| `reviews/diagnosis.md` | Lever diagnosis and manager decisions for Run 2 |
| `reviews/run_comparison.md` | Run 1 vs Run 2 comparison |
| `capstone/evidence_log.md` | Append-only record of every milestone, decision, correction and hash |
| `capstone/defense_notes.md` | Interview preparation |
