# Evidence Log

A running record of the agent's trajectory. One section per milestone. Entries are
added as each milestone progresses and are not rewritten later.

---

## Milestone 1 — Project setup and context package

**Date:** 2026-10-27
**Agent role:** Implementation agent
**Status:** Complete, awaiting manager review

### 1. Files inspected

| What | Finding |
|------|---------|
| Project root `agent-capstone-job-fit-evaluator/` (`ls -la`, `find`) | Empty directory. No existing files, so nothing was overwritten. |
| Git status | Not a git repository at the start. |
| Python version (`python3 --version`) | **3.10.12**, which is below the 3.11+ target. See Uncertainties. |

No real project inputs (CV, job description) were supplied, so all context is
synthetic.

### 2. Files created

**Substantive content**
- `README.md`
- `.gitignore`
- `requirements.txt`
- `context/candidate_cv.md`
- `context/job_description.md`
- `context/evaluation_standard.md`
- `context/irrelevant_reference.md`
- `capstone/evidence_log.md` (this file)

**Placeholders** (each states its purpose and the milestone that fills it)
- `prompts/run1_prompt.md`, `prompts/run2_prompt.md`
- `runs/run1/output.md`, `runs/run1/trajectory.md`
- `runs/run2/output.md`, `runs/run2/trajectory.md`
- `reviews/run1_review.md`, `reviews/diagnosis.md`, `reviews/run_comparison.md`
- `capstone/final_report.md`, `capstone/defense_notes.md`
- `src/__init__.py`, `src/models.py`, `src/parser.py`, `src/evaluator.py`, `src/report.py`
- `tests/test_parser.py`, `tests/test_evaluator.py`
- `scripts/run_evaluation.py`

Python placeholders contain only a module docstring, so they import cleanly.

**Workspace change**
- `git init -b main`, done at the manager's request mid-milestone. **No commits
  have been made.** The first commit is left to the manager.

### 3. Important decisions

1. **Synthetic data is labelled in three ways.** Each context file opens with a
   "SYNTHETIC" banner, every organisation is marked *(fictional)*, and the
   candidate is "Candidate A".
2. **The CV and job description were designed as test fixtures.** The CV
   deliberately includes a range of evidence strengths so that later runs can
   show whether the agent keeps them apart:
   - direct professional evidence;
   - compound requirements where only part is evidenced;
   - experience from a personal project rather than professional work;
   - keywords that appear only in the skills list;
   - vague metrics with no numbers;
   - an in-progress certification;
   - a part-time role that affects the years-of-experience calculation;
   - a CV "last updated" date that differs from today's date.
   The job description lists mandatory and preferred requirements under labelled
   headings (M1–M6, P1–P6). It also states an obligation in the Responsibilities
   prose that is not repeated in the requirements lists, to test whether the
   agent extracts requirements beyond the labelled lists.
3. **No answer key in the repository.** Per-requirement expected statuses are
   deliberately not written down. Any agent run in this workspace could read
   them, which would contaminate Run 1. Where to keep an answer key is a manager
   decision (see section 7).
4. **The distractor file is a plausible near-miss.**
   `irrelevant_reference.md` holds panel notes for a different role (Senior
   Frontend). Its "benchmark profile" includes Kubernetes, Kafka, mentoring and
   an AWS certification, all of which overlap keywords in Candidate A's skills
   list. Misuse would therefore show up as fabricated or inflated evidence. The
   file body does not say "do not use"; the README explains its purpose.
5. **The evaluation standard leaves the distractor rule to the prompts.** An
   early draft of `evaluation_standard.md` said that only the CV and job
   description are evidence sources. I removed that line and replaced it with
   the neutral rule "evidence about the candidate must come from the candidate's
   own materials". Your brief says later *instructions* will exclude the
   distractor. Keeping that rule in the prompts, not the shared standard, keeps
   the Run 1 / Run 2 comparison clean.
6. **The scoring model follows the suggested 70 / 20 / 10 split, kept simple:**
   - status credit: 1.0 for SUPPORTED, 0.5 for PARTIALLY_SUPPORTED, 0 for
     UNCLEAR or UNSUPPORTED. UNCLEAR earns nothing so that unverified claims are
     not rewarded;
   - equal weights within each category;
   - evidence quality grades A = 1.0, B = 0.5, C = 0, averaged across all
     requirements into the 10-point component;
   - fit bands ≥ 75 / 55–74.9 / < 55;
   - a mandatory-gap flag that does not change the band automatically.
   The standard includes a worked example that Milestone 2 can reuse as a test.
7. **Conservative tie-breaking.** When a status or requirement type is
   ambiguous, the standard picks the less favourable option.
8. **Minimal dependencies.** The runtime uses only the standard library;
   `pytest` is the only listed dependency. No LangChain, database, Docker,
   frontend or external API was added.
9. **`runs/` is not git-ignored**, because run outputs are capstone evidence.

### 4. Assumptions

- The project has no real candidate or job inputs yet, so synthetic stand-ins
  are acceptable.
- The final mandatory/preferred weights may be revised after Run 1, so the
  standard is versioned as 0.1.
- Fit bands, status credits and evidence grades are my initial choices; the
  brief specified only the 70 / 20 / 10 split.
- Placeholder files should state their purpose but contain no draft content.

### 5. Uncertainties

- **Python version mismatch.** The spec says 3.11+, but the machine has 3.10.12.
  Nothing has been executed yet, so there is no impact so far. Milestone 2 should
  either install 3.11+ or keep the code 3.10-compatible (avoid `tomllib`,
  `ExceptionGroup`, `typing.Self`, etc.).
- **Hidden-requirement fixture.** The on-call obligation in the Responsibilities
  prose of the job description is a deliberate test, and section 2 of the
  evaluation standard states the matching rule. It is your call whether that
  rule should stay in the shared standard or move into Run 2's instructions only.
- **How strict the standard is.** Treating ambiguous requirement types as
  mandatory, and giving UNCLEAR zero credit, may produce low scores. That is
  intentional for safety but could be debated.
- **Weak evidence-quality signal.** The confidence component overlaps with
  status credit (a C grade usually coincides with zero credit). It may need
  redesign once real outputs exist.

### 6. Deliberately excluded

- Any scoring or parsing implementation (Milestone 2).
- Any content in the run prompts, outputs, trajectories or reviews.
- An answer key of expected statuses (see decision 3).
- Real names, employers, institutions or vacancies.
- Commits, CI configuration, virtualenv creation and package installation.

### 7. Open questions for the manager

1. Should a per-requirement answer key exist, and if so, where (outside the
   repository, or added only after Run 2)?
2. Should the on-call / hidden-requirement rule stay in `evaluation_standard.md`?
3. Python 3.11+ installation or 3.10 compatibility?
4. Should I make the first git commit now that Milestone 1 is reviewed?

### 8. What remains for Milestone 2

- `src/models.py`: Requirement, Evidence, Status (enum), EvidenceGrade, Assessment.
- `src/parser.py`: extract M*/P* requirements and CV sections from the markdown.
- `src/evaluator.py`: implement the scoring formulas, bands and mandatory-gap
  flag from section 6 of the standard, without automating judgement calls on
  status.
- `src/report.py`: render the eight required output sections.
- `tests/`: parser tests against the context files, and scoring tests, including
  the worked example (expected total 52.1).
- `scripts/run_evaluation.py`: CLI wiring.

---

## Milestone 1 — Addendum: manager-directed changes after review

**Date:** 2026-10-27
**Trigger:** Manager review of Milestone 1 (passed with minor required changes).
The entries above are kept as originally written. Where this addendum conflicts
with them, the addendum takes precedence.

### Changes applied

1. **Python version (manager-directed environment decision).** The development
   environment is Python 3.10.12. The documented requirement changes from 3.11+
   to **3.10+** in `README.md` and `requirements.txt`. No other Python version
   will be installed, and all code must stay 3.10-compatible (no `tomllib`,
   `ExceptionGroup`, `typing.Self`, `except*`, etc.). This resolves the
   "Python version mismatch" uncertainty and open question 3.
2. **On-call clue removed from the shared standard.** In section 2 of
   `context/evaluation_standard.md`, the Mandatory row read "...and any
   obligation stated as expected elsewhere in the description". It now reads
   "Requirements listed as mandatory or required." The standard no longer tells
   the evaluator to look outside the labelled requirement sections, and it does
   not mention on-call.
   **Why:** it is a methodological choice. Run 1 should show whether the agent
   *independently* notices requirements embedded elsewhere in the job
   description. A hint in the shared standard would hide that behaviour. The job
   description is unchanged. This resolves open question 2.
3. **No answer key in the repository (manager decision).** No answer key or
   expected-result file will be created anywhere in this repository. The manager
   keeps expected-result material outside the agent-visible workspace. This
   resolves open question 1.
4. **Baseline commit authorised** after validation. This resolves open question 4.

### Explicitly unchanged (per manager)

The synthetic CV, the synthetic job description, `irrelevant_reference.md`, the
scoring weights, UNCLEAR = zero credit, conservative tie-breaking, evidence-quality
scoring and all deliberate test cases are unchanged. The overlap between
evidence quality and status credit has been acknowledged and is deliberately left
as-is until evaluator behaviour has been observed.

---

## Milestone 2 — Evaluation engine and rubric

**Status:** Not started. This section opens with a pre-milestone manager
directive. Implementation entries will follow when Milestone 2 begins.

### Decision M2-1: workspace isolation for semantic agent runs (manager-directed)

**Date:** 2026-10-27

**Problem.** The manager's review of Milestone 1 found that `README.md` and this
evidence log describe the deliberate evaluation test cases (the embedded
requirement fixture, the distractor file and the evidence-strength variants). A
semantic agent run with access to the full repository could read them, which
would invalidate Run 1 as a test of the agent's independent behaviour.

**What is *not* done.** The historical evidence is not removed or rewritten.
Milestone 1 entries in this log and in the README stay as committed in
`a27f9ab`. Hiding the trail would weaken the capstone's audit value. The fix is
to control access, not to edit history.

**Decision.** There are two execution contexts with different access:

| Context | Who | Access |
|---------|-----|--------|
| **Deterministic framework** | `src/`, `tests/`, `scripts/` (parsing, scoring arithmetic, report rendering) | The full repository. It applies fixed rules and makes no semantic judgements, so seeing test-case notes cannot bias it. |
| **Semantic agent run** | The agent performing Run 1 / Run 2 (requirement extraction, evidence mapping, status judgements, positioning, brief) | **Only a restricted run workspace** whose contents are explicitly listed. |

**Run-workspace source package (explicit allowlist).** Only these files are placed
in a run workspace:

- `context/candidate_cv.md`
- `context/job_description.md`
- `context/evaluation_standard.md`
- `context/irrelevant_reference.md`. It is included on purpose: the distractor
  test only works if the file is reachable. Whether the agent is told to ignore
  it is a matter for the run prompt, not for workspace contents.
- the run's own prompt (`prompts/runN_prompt.md`)

Everything else is excluded by default, because the package is an allowlist, not
a denylist. This explicitly covers:
- `README.md`;
- `capstone/` (including this log);
- `reviews/` and `tests/`;
- `src/` and `scripts/`, plus any implementation notes;
- other runs' prompts, outputs and trajectories;
- `.git/`, whose history contains all of the above;
- any manager-only expected results, which are not in the repository anyway.

**Design constraints for the future implementation** (to be built in Milestone
3, not now):
1. **Location.** The run workspace is created **outside the repository tree**,
   so relative navigation (`..`) from the workspace cannot reach the repository.
2. **Provenance.** The workspace includes a generated manifest listing each
   copied file with its SHA-256 hash and the commit it came from. The
   trajectory can then prove exactly what the agent could see.
3. **Prompt hygiene.** The run prompt must not mention the repository's path,
   the test-case design or the manager's expectations.
4. **Fresh session.** The agent is started as a fresh session whose working
   directory is the run workspace, with no inherited conversation context from
   the implementation agent.
5. **Returning outputs.** Outputs are written inside the run workspace and then
   copied back unedited to `runs/runN/` by the framework or the manager, never
   by the agent writing into the repository.

**Residual risk.** Copy-based isolation stops *automatic* access, not
*deliberate* access. An agent with general filesystem tools could still find the
repository by absolute path. Mitigations: the workspace sits outside the
repository, the prompt contains no repository path, and the manager's review of
each trajectory checks for any read outside the workspace. Stronger sandboxing,
such as containers or OS-level permissions, is out of scope under the "no
Docker" constraint. If this leaves too much risk, it should be revisited in
Milestone 3.

**Effect on Milestone 2 architecture.** The scoring engine does not need a
workspace helper, so none is built now. In Milestone 3, a small builder (a
fixed allowlist constant plus a copy-and-manifest function, standard library
only) is expected in `src/` or `scripts/`. Milestone 2 code will read context
files through explicit paths passed in by the caller rather than scanning the
repository, so the same parser can run unchanged inside a restricted workspace.

**Note on the agent writing this entry.** I (the implementation agent) know the
test-case design and therefore must not be the agent that performs the semantic
runs. This is consistent with requirement 4 above.

### Milestone 2 — implementation log

**Date:** 2026-10-27
**Status:** Implementation complete, awaiting manager review. **Not committed**,
per instruction. Agent Run 1 was **not** performed.

#### 1. Files inspected

| What | Finding |
|------|---------|
| `git log`, `git status` | Two commits (`a27f9ab`, `b14842a`); clean tree at start. |
| `context/job_description.md`, `context/candidate_cv.md` | Structure only: heading layout, the `N. **ID** — text` item format, wrapped continuation lines. |
| `context/evaluation_standard.md` | Sections 3 to 7: statuses, citation rules, grades, formulas, bands, output sections. |
| Decision M2-1 (above) | Workspace-isolation constraints, so the parser takes explicit paths. |
| Python environment | `python` is not on PATH outside a venv (pyenv offers it only for 3.12.15, which was not used). `/usr/bin/python3` is 3.10.12. pytest was not installed. |

`context/irrelevant_reference.md` was **not** opened in this milestone.

#### 2. Files changed

**Implemented (were placeholders):** `src/__init__.py`, `src/models.py`,
`src/parser.py`, `src/evaluator.py`, `src/report.py`,
`scripts/run_evaluation.py`, `tests/test_parser.py`, `tests/test_evaluator.py`.

**New:**
- `tests/test_report.py`, `tests/test_cli.py`, `tests/test_boundaries.py`;
- `tests/support.py` (shared paths and builders);
- the neutral fixtures `tests/fixtures/job_description_fixture.md`,
  `tests/fixtures/cv_fixture.md`, `tests/fixtures/assessment_fixture.json` and
  `tests/fixtures/assessment_malformed.json`;
- `pytest.ini`.

**Local only (git-ignored):** `.venv/`, a Python 3.10.12 virtualenv.

**Unchanged:** all of `context/`, `README.md`, `requirements.txt`, and the
Milestone 1 entries and Decision M2-1 in this log.

#### 3. Architectural decisions

1. **The deterministic/semantic boundary.**
   - **Python does:** parse labelled structures, validate supplied judgements,
     calculate scores, render the report.
   - **Python never does:** assign a status or grade, match keywords to
     experience, infer equivalence or years of experience, or call a model.
   - **Enforcement:** `tests/test_boundaries.py` asserts that framework code
     imports only the standard library and itself, and nothing network-,
     subprocess- or LLM-related.
2. **Explicit paths everywhere.** Every parse and load function takes a path
   argument, and nothing scans directories. A test patches `Path.read_text` to
   prove that only the two named files are read when a sentinel
   `irrelevant_reference.md` sits beside them. The CLI adds the repository root
   to `sys.path` only to import `src` (the code); data always comes from CLI
   arguments. The CLI is tested from a foreign working directory.
3. **JSON assessment format, schema_version 1.**
   - Top level: `candidate_id`, `sources_inspected`, `sources_excluded`
     (`{path, reason}`), `assessments`, `positioning`, `application_brief`,
     optional `uncertainties`, optional `additional_requirements`.
   - Each assessment: `requirement_id`, `status`, `evidence_grade`, `evidence`
     (a list of `{location, quote}`), `rationale`, optional `uncertainty`,
     optional `verification_question`.
   - Unknown keys are **rejected** so that a typo such as `evidense` cannot
     silently drop data.
   - All errors are collected and reported together.
4. **Deterministic anti-fabrication check.**
   - Each evidence `location` must resolve to a CV heading, given either as
     `Heading` or as `Parent → Heading`, with ancestry checked.
   - Each `quote` must appear **verbatim** inside that section's text.
   - Normalisation strips only Markdown `*` and backticks, unifies dashes and
     collapses whitespace. Quotes stay case-sensitive.
   - This is string containment, not semantic matching: it proves a quote
     exists, not that it supports the requirement.
5. **Structural consistency rules derived from the standard's definitions:**
   - every status except UNSUPPORTED needs at least one citation (section 4);
   - UNSUPPORTED requires grade C ("no evidence", section 5);
   - SUPPORTED cannot have grade C (decision rule 2);
   - UNCLEAR requires a `verification_question` (section 7, item 5);
   - every rationale must be non-empty.
6. **`additional_requirements` (agent-identified requirements).**
   - **Why it exists:** without it, the evaluator would reject any requirement
     ID outside M*/P*. The framework would then structurally prevent the agent
     from scoring a requirement it found elsewhere in the job description. That
     would be a Workspace-lever confound in the Run 1 test.
   - **Rules:** IDs must match `A1`, `A2`, …; the agent must choose the type;
     the `source_quote` must appear verbatim in the job description. These
     requirements are scored like any other and are marked † in the report.
   - **Hint risk:** the field's existence could hint at the test. Whether to
     describe it in the Run 1 prompt is an open manager decision (section 7).
7. **Exact arithmetic.** Credits and grades are `Fraction`s; only the final
   total is rounded, half-up, to one decimal (`Decimal`). This avoids float
   noise and Python's round-half-even. Fit bands use the rounded total, so the
   displayed number and the band always agree (e.g. 74.95 → 75.0 → Strong).
8. **Constants live in code; the standard is checked, not executed.** The
   weights, credits and grade values are constants in `src/evaluator.py`.
   `check_standard_consistency()` (CLI `--standard`) parses the standard's
   tables and fails on any drift. The rules are not read from Markdown at run
   time, which would be fragile.
9. **No mandatory requirements → `ScoringError`.** The standard defines a rule
   when there are no *preferred* requirements (mandatory weight becomes 90), but
   none when there are no *mandatory* ones. Rather than invent a rule, the
   evaluator refuses.
10. **The fixtures are deliberately not about Candidate A.** The CLI and scoring
    fixtures use a neutral "Tool Alpha…Zeta" job description and CV. Real
    context files are used only for structural parser tests (IDs, text, types).
    So there is still **no answer key** for the capstone candidate anywhere in
    the repository. The fixture's statuses mirror the standard's worked example.
11. **Strict job-description parsing.** Both labelled requirement sections must
    exist, appear once and contain at least one item. Any line that is not an
    item or an indented continuation fails. Wrapped item text is joined with
    single spaces; otherwise the text is preserved exactly.
12. **unittest-style tests.** Every test is a `unittest.TestCase` (see
    section 5), so the suite runs under both `python -m unittest` and pytest,
    which collects TestCase classes natively.

#### 4. Assumptions

- The "Location" in section 4 of the standard maps to CV headings. The
  standard's own illustrative example (*Professional experience → Software
  Engineer, Example Logistics Ltd*) uses a comma where the heading has an em dash
  and omits "(fictional)", so it would **fail** validation as written. See
  section 7.
- Section 7 items 1 to 5 can be computed from supplied data. Items 6 to 8
  (positioning, brief, uncertainties) are agent narrative, rendered verbatim and
  not checked for fabrication.
- Fit-band thresholds apply to the rounded total.
- Component scores are displayed to two decimals as presentation only.

#### 5. Failures encountered and how they were handled

1. **pytest could not be installed.**
   - `pip install -r requirements.txt` inside the new venv failed with
     `Network is unreachable` (sandboxed network).
   - Retrying with the sandbox disabled was **denied** by the auto-mode
     permission classifier. I did not attempt to work around that.
   - No usable local 3.10 pytest existed; only 3.12 venvs in other projects had
     one.
   - **Mitigation:** the tests are written as `unittest.TestCase`, so they run
     under pytest unchanged. Validation used `python -m unittest discover -s
     tests`.
   - **`pytest -q` has not been executed.** The manager needs to run
     `pip install -r requirements.txt` with network access, then `pytest -q`.
2. **`python` was missing from PATH.** Resolved by the project venv, created from
   `/usr/bin/python3` (3.10.12): inside it, `python --version` reports 3.10.12.
   No other Python was installed.
3. **The worked example in the standard is arithmetically inconsistent (my
   Milestone 1 error).**
   - The example lists grades A, A, B, C, B, C and states their sum as "2.0 / 6",
     giving 52.1.
   - Under the standard's own values (A = 1.0, B = 0.5, C = 0) the sum is
     **3.0**, so the confidence component is 5.0 and the total is
     43.75 + 5.0 + 5.0 = 53.75 → **53.8**.
   - My Milestone 1 "validation" of 52.1 re-typed the example's own 2.0 instead
     of deriving it from the grades: it was circular and did not check anything.
   - The implementation follows the normative formulas. The tests assert 53.8,
     with a docstring explaining the discrepancy.
   - **`context/evaluation_standard.md` was not edited**, because it is
     agent-visible context under manager control.
4. **Test bug: missing `re.MULTILINE`.** The report test
   `test_every_requirement_id_has_a_row` anchored `^` without multiline mode, so
   6 subtests failed on the first run. I fixed the test; the renderer was
   correct.
5. **Unused import.** An AST-based unused-import scan (no linter available) found
   one, `FIXTURE_JD` in `tests/test_parser.py`. Removed.

#### 6. Validation performed

- `python --version` → Python 3.10.12 (venv).
- `python -m compileall src scripts` → exit 0.
- `pytest -q` → **not runnable** (pytest not installed, see 5.1).
- `python -m unittest discover -s tests` → **91 tests, OK**.
- CLI with the valid fixture and `--standard` → exit 0, report written,
  total **53.8**, Weak fit, all 8 sections in order.
- CLI with the malformed fixture → exit 1, all 4 structural errors listed.
- CLI with a structurally valid but invalid assessment → exit 1, 6 errors
  listed: fabricated quote, unknown ID M9, missing M3 and P2, and UNCLEAR
  without citation or question.
- CLI with a drifted copy of the standard → exit 1, mismatch named.

#### 7. Unresolved issues (manager decisions needed)

1. **Worked-example arithmetic.** Should section 6 of the standard be corrected
   before Run 1? Either the stated sum becomes 3.0 and the total 53.8, or the
   listed grades change to match 52.1. The standard is agent-visible, so an
   uncorrected error could mislead a Run 1 agent. Fixing it is a Context change,
   best made **before** Run 1, not as a Run 2 lever.
2. **Location format.** The standard's citation example does not match real CV
   headings and would fail validation. Either correct the example, or have the
   Run 1 prompt specify "copy the CV heading". This is an Instructions/Context
   question, and leaving it as-is may produce validation failures in Run 1.
3. **Disclosing `additional_requirements`.** Describing this field in the Run 1
   prompt may hint at embedded requirements. Leaving it out means the agent has
   no structured way to record one, although it could still mention it in
   narrative or uncertainties.
4. **Two-stage error reporting.** Structural (loader) errors are reported first;
   evidence and coverage errors appear only after the structure is valid. That is
   acceptable, but an agent may need two fix cycles.
5. **Narrative sections are not checked.** Positioning, the application brief
   and uncertainties are rendered verbatim. The framework cannot detect
   fabrication in free text; manager review must cover them.
6. **Evidence-quality / status overlap.** Acknowledged and left unchanged, per
   the manager.
7. **Commit pending manager review.**

#### 8. Rejected approaches

- **Reading the scoring rules from the standard's Markdown at run time.** Too
  fragile; replaced by code constants plus a drift check.
- **A pydantic or attrs schema.** Rejected as an unnecessary dependency; plain
  dataclasses with a hand-written loader are enough.
- **Fixtures built on Candidate A's real context.** Rejected because they would
  amount to an answer key in an agent-adjacent repository.
- **Case-insensitive or fuzzy quote matching.** Rejected as too permissive for
  an anti-fabrication check. Only formatting is normalised.
- **Silently ignoring unknown JSON keys.** Rejected, because it could drop
  evidence without notice.
- **Inventing a scoring rule for zero mandatory requirements.** Rejected; the
  evaluator raises an error instead.
- **Building the run workspace now.** Deferred to Milestone 3, per Decision
  M2-1.

#### 9. What remains for Milestone 3

- Manager decisions on section 7, items 1 to 3, before writing the Run 1 prompt.
- Install pytest with network access and confirm `pytest -q`.
- Build the run-workspace builder per Decision M2-1: an allowlist, a location
  outside the repository, and a manifest with SHA-256 hashes and the source
  commit.
- Write and freeze `prompts/run1_prompt.md`, including the JSON assessment
  schema the agent must produce.
- Perform Run 1 in a **fresh** agent session confined to the run workspace, not
  by this implementation agent.
- Copy the outputs back into `runs/run1/` unedited. Run the CLI on the agent's
  JSON and record any validation failures as Run 1 evidence, not as defects to
  fix silently.

### Milestone 2 — manager review: decisions and correction results

**Date:** 2026-10-27
**Trigger:** The manager review passed Milestone 2, subject to two context
corrections and final validation. Milestone 3 has not started. Nothing has been
committed. The entries above are kept as written; this subsection adds to them.

#### Manager decisions

1. Correct the arithmetic of the worked example in `evaluation_standard.md`
   from the existing rules, without changing any rule to reach a target number.
2. Correct the citation example so that locations use exact CV headings and
   quotes are copied verbatim. `candidate_cv.md` is not to be changed.
3. Keep `additional_requirements` as an optional framework field. The standard
   must not tell an agent to search for hidden, embedded, on-call or
   out-of-section requirements. (Resolves open item 3 of the implementation log.)
4. Make no further network installation attempt. Record the pytest limitation
   accurately.
5. Preserve the history of test failures.

#### Defect classification

**Context defects (found before Run 1)**

- **CTX-1: worked-example arithmetic (introduced by me in Milestone 1).**
  - **Defect:** section 6 stated the sum of grades A, A, B, C, B, C as 2.0,
    giving a confidence score of 3.33 and a total of 52.1.
  - **Recalculated from the documented rules only:**

    | Component | Calculation | Result |
    |-----------|-------------|--------|
    | Mandatory | (1 + 1 + 0.5 + 0) / 4 = 0.625 → 70 × 0.625 | **43.75** (unchanged) |
    | Preferred | (0.5 + 0) / 2 = 0.25 → 20 × 0.25 | **5.0** (unchanged) |
    | Confidence | (1 + 1 + 0.5 + 0 + 0.5 + 0) / 6 = 3.0 / 6 = 0.5 → 10 × 0.5 | **5.0** (was 3.33) |
    | Total | 43.75 + 5.0 + 5.0 = 53.75, rounded to one decimal | **53.8**, Weak fit (< 55, band unchanged) |

  - **Fix:** corrected the grade sum, the confidence calculation and the total.
    No weight, credit, grade value or band was changed.
  - **Note:** 53.75 is an exact tie at one decimal. The standard says "round to
    one decimal place" but not how to round a tie. Half-up (the evaluator) and
    half-even both give 53.8; only rounding ties downward would give 53.7. No
    rounding rule was added to the standard; this is listed as unresolved below.
- **CTX-2: citation-location example did not match the CV.**
  - **Defect:** section 4 gave *Professional experience → Software Engineer,
    Example Logistics Ltd*. The CV heading is `Software Engineer — Example
    Logistics Ltd *(fictional)*`, with an em dash, not a comma, plus
    "(fictional)". A location written that way fails validation.
  - **Fix:** the Location rule now requires the exact CV heading, optionally
    preceded by its parent heading and `→`, which matches what the validator
    accepts. The example uses a real Candidate A heading, in both forms. The
    Quote rule now requires a verbatim copy from that section, with no
    paraphrasing, shortening or splicing.
  - **No example quote** from Candidate A's CV was added: it would imply which
    requirement the text supports, acting as a partial answer key.
    `candidate_cv.md` is unchanged.

**Code defects**

- None found in this review cycle. `src/` and `scripts/` are unchanged by this
  subsection.

**Test defects**

- **TST-1 (first Milestone 2 run, recorded above in 5.4).** The first
  `unittest` run produced **6 failures**, all subtests of
  `test_report.TestReport.test_every_requirement_id_has_a_row`. The cause was a
  missing `re.MULTILINE` flag in the test's `^`-anchored regex. Investigation
  showed the rendered report did contain every row, so the renderer was correct.
  The test was fixed, and the suite then passed (91 tests).
- **TST-2: stale docstring.** After CTX-1, the docstring of
  `test_worked_example_inputs_from_standard` still said the standard states
  2.0 and 52.1. Updated to describe the corrected example and its history.
  The assertions were already 53.8 and are unchanged.
- **TST-3: new regression test with a bad filter.** I added two tests that read
  the standard directly:
  - `test_worked_example_total_in_standard_matches_evaluator` checks that the
    stated total and band equal the computed result;
  - `test_standard_citation_example_locations_exist_in_candidate_cv` checks
    that the example locations resolve against Candidate A's real headings.

  The second test **failed on its first run**. Its code-span filter excluded
  only `→`, so it also picked up the two `` `UNSUPPORTED` `` spans in section 4
  as "locations". Fixed by excluding status names as well. The standard was
  correct: both example locations resolve.

**Environment and workspace limitations**

- **ENV-1: pytest.**
  - `pytest -q` was requested by the manager.
  - pytest was **not available** in the environment: it is neither installed
    system-wide for Python 3.10 nor in the project venv.
  - Installing it required network access. The sandboxed install failed with
    `Network is unreachable`, and the request to run it outside the sandbox was
    **not permitted** by the permission system.
  - On the manager's instruction, no further installation was attempted.
  - **pytest itself has never been executed in this project.** No pytest result
    is claimed.
  - The complete suite was run with the standard-library runner instead:
    `python -m unittest discover -s tests`.
  - Results: **91 tests passed** before this review, and **93 tests passed**
    after it (91 plus the two regression tests from TST-3).
  - The tests are `unittest.TestCase` classes and `pytest.ini` is present, so
    pytest should collect them unchanged. This is expected but unverified.
- **ENV-2: `python` on PATH.** Outside a venv, `python` resolves only to a
  pyenv 3.12.15 install, which was not used. All validation ran in `.venv`,
  built from `/usr/bin/python3` 3.10.12.

#### Validation after the context corrections

| Check | Result |
|-------|--------|
| `python --version` | Python 3.10.12 |
| `python -m compileall src scripts` | exit 0 |
| `python -m unittest discover -s tests` | `Ran 93 tests` … `OK` |
| Standard internally consistent | Weight, credit and grade tables match the evaluator (`--standard` passes). The stated worked-example total equals the computed total (53.8, Weak fit; regression test). Both citation-example locations resolve to real CV headings (regression test). |
| CLI, valid fixture with `--standard` | exit 0, total 53.8, Weak fit, all 8 sections in order |
| Negative: malformed structured input | exit 1, 4 errors (invalid status, unknown field `evidense`, missing `evidence`, invalid grade `E`) |
| Negative: fabricated quote (otherwise valid fixture) | exit 1, "quote not found verbatim in CV section …" |
| Negative: standard-weight mismatch (copy with mandatory weight 65) | exit 1, "'Mandatory requirements' is 65 in the standard but 70.0 in the evaluator" |
| No LLM/API dependency | No model, HTTP or socket references in `src/`, `scripts/` or `requirements.txt` (pytest only). Enforced by `test_boundaries.py`. |
| No keyword-based semantic matching | The only text comparisons in `src/` are the verbatim check of an agent-supplied quote within its cited section, and heading matching. Requirement text is only rendered, never compared with the CV. |
| No Candidate A answer key | No answer-key files. No JSON assigns statuses to capstone IDs. Fixtures use the neutral Tool Alpha…Zeta job description and CV. The standard now names a Candidate A *heading* (CTX-2) but no status, grade or quote. |
| `irrelevant_reference.md` never implicitly loaded | Not referenced in `src/` or `scripts/`; no directory scanning. The `Path.read_text` recording test passes. |
| Protected context files | `candidate_cv.md`, `job_description.md` and `irrelevant_reference.md` are unchanged since `b14842a`. |
| Standard has no hidden-requirement hints | No "on-call", "embedded", "hidden", "elsewhere", "outside" or "additional" wording. |

#### Still unresolved

1. **Rounding of ties.** The standard does not specify how to round a total
   that falls exactly halfway; the evaluator rounds half-up. The worked example
   is such a tie (53.75). This is a manager decision whether to state it.
2. **Location matching is more lenient than the standard.** The standard says
   "exact heading". The validator also tolerates differences in case,
   Markdown `*`/backticks, dash style and whitespace. Quotes stay
   case-sensitive. The validator therefore never rejects a location the standard
   allows.
3. **pytest has not been run** (ENV-1).
4. **Narrative sections are not machine-checked** for fabrication (carried
   over).
5. **The Milestone 2 commit** is pending manager instruction.

### Milestone 2 — final deterministic-rule corrections (manager review 3)

**Date:** 2026-10-27
**Trigger:** Milestone 2 approved, subject to two deterministic-rule corrections.
Milestone 3 has not started. Nothing has been committed. All earlier entries are
kept as written.

#### Manager decisions

1. Add an explicit **ROUND-HALF-UP** rule for the final total, and state that
   intermediate weighted components are not rounded. The worked example must
   remain 53.8.
2. Make **location validation** follow the standard: exact CV heading text,
   with no normalisation of case, wording, dash characters or meaningful
   spacing. Keep the optional `Parent → Child` form.
3. Make no further pytest installation attempt; the evidence record must stay
   accurate.
4. Add **no** automated semantic or fabrication checking of free-text sections.
   Reviewing them remains a manager responsibility.

#### RULE-1: explicit rounding rule (a previously unspecified deterministic rule, clarified before Run 1)

- **Before:** the standard said only "Round only the final total, to one decimal
  place", with no tie-breaking rule. The evaluator already used half-up, so the
  code was stricter than the document.
- **Standard change:** a new `### Rounding` subsection in section 6. The final
  total is rounded to one decimal using ROUND-HALF-UP; weighted components are
  not rounded before the total; fit bands apply to the rounded total. It gives
  two examples: 56.25 → 56.3, a case where half-even would give 56.2, and
  53.75 → 53.8.
- **Implementation (confirmed and documented, behaviour unchanged):**
  - components are exact `fractions.Fraction` values;
  - `round_total()` converts the exact total with `Decimal(numerator) /
    Decimal(denominator)`, then calls `.quantize(Decimal("0.1"),
    rounding=ROUND_HALF_UP)`;
  - the built-in `round()` is never used in `src/` (verified by grep), and the
    docstring now says why;
  - the report's `:.1f` is applied only to an already-rounded total, and `:.2f`
    only to component values that are displayed, never used in the calculation.
- **New regression tests:**
  - `test_half_up_differs_from_half_even_on_ties_after_an_even_digit` covers
    53.65, 56.25, 61.25 and 0.05. Each case asserts that HALF-EVEN would give a
    different answer, so the test really discriminates.
  - `test_scored_tie_uses_half_up_not_builtin_round`: a real scoring case whose
    exact total is 56.25 gives 56.3, while the built-in `round(56.25, 1)` gives
    56.2.
  - `test_non_tie_values_round_to_nearest`.
  - `test_rounding_happens_before_banding`: 74.95 → 75.0 → Strong.
  - `test_standard_states_round_half_up`.
- **Worked example:** still **53.8, Weak fit**. The existing regression test
  confirms that the standard's stated total equals the computed one.

#### ALIGN-1: location matching vs. the standard (an implementation/standard alignment issue found during managerial review)

- **Discrepancy:**
  - In the previous review I strengthened the standard to require the "exact
    heading". The validator still compared headings after casefolding,
    stripping `*` and backticks, converting em and en dashes to hyphens, and
    collapsing whitespace. It also accepted an undocumented `>` separator.
  - The validator was therefore **more lenient** than the standard. I had
    reported this as unresolved, but not as a defect.
- **Fix in `src/evaluator.py`:**
  - The location is split only on the documented separator `→`. Only the
    whitespace immediately around each part is trimmed (`Parent → Child` and
    `Parent→Child` are equivalent).
  - Each part is compared **character for character** with heading text as the
    parser stores it: the line minus its leading `#` markers and surrounding
    whitespace.
  - Case, wording, dash characters, inner spacing and inline formatting such as
    `*(fictional)*` must all match. Ancestry is checked for the parent form.
  - `>` is no longer accepted.
- **Diagnostic hint:** when a location fails but a heading would match under
  the old lenient comparison, the error names that heading ("closest heading is
  …; case, dash characters and formatting must match exactly"). The hint is
  diagnostic only; such locations are **never accepted**.
- **Standard (section 4):** added one sentence saying matching is exact, listing
  case, wording, dash characters, spacing and inline formatting, and noting that
  only the heading's `#` markers are left out. No other rule changed.
- **Fixture:** `tests/fixtures/assessment_fixture.json` had two locations
  without the `*` emphasis (`… Fixture Org (fictional)`). They now use the
  exact heading `Experience → Engineer — Fixture Org *(fictional)*`. The
  fixture's statuses, grades and score are unchanged (53.8).
- **Tests changed:**
  - `test_location_and_quote_ignore_markdown_formatting_only` asserted the old
    lenient behaviour and was removed. It is replaced by
    `test_inexact_location_fails_with_closest_heading_hint`, which tests a
    wrong-case, wrong-dash location, and by
    `test_quote_tolerates_line_wrapping_whitespace`, which keeps the
    quote-whitespace coverage.
  - `test_location_path_must_match_ancestry` now uses the exact child heading,
    so that only the ancestry is wrong.
- **New `TestLocationExactness`:** runs against Candidate A's real headings, but
  resolves locations only, with no statuses or quotes, so it is not an answer
  key. Coverage:
  - the exact heading passes (and `Skills`);
  - the exact `Parent → Child` form passes;
  - spacing around `→` does not matter;
  - wrong case fails (four variants);
  - a hyphen or en dash instead of the em dash fails;
  - a missing `*` emphasis fails;
  - doubled spacing fails;
  - nonexistent headings or ancestry fail;
  - the `>` separator fails;
  - empty parts fail.
- `candidate_cv.md` is unchanged.

#### Test defects in this cycle

- **TST-4.** My new sentence in section 4 added `` `*` `` and `` `#` `` code
  spans. That broke
  `test_standard_citation_example_locations_exist_in_candidate_cv` (4 spans
  found instead of 2): the test filtered code spans by exclusion, which is the
  same weakness as TST-3. I changed it to extract only the spans between "For
  example:" and "Matching is exact". The first version of that fix failed too
  (5 spans), because the source text wraps between "Matching" and "is exact".
  It now uses a whitespace-tolerant regex. The standard was correct throughout;
  both examples resolve exactly.

#### Code defects in this cycle

- **ALIGN-1** (above) is the only code change. It was a misalignment between the
  validator and the standard, not a crash or a wrong score.

#### Environment and workspace limitations (unchanged)

- **ENV-1 (restated for accuracy).** pytest itself has **not** been executed.
  It is unavailable in the environment, and installing it required network
  access that was not permitted; no further attempt was made. For this
  milestone, the authoritative test run is `python -m unittest discover -s
  tests`.

#### Validation results

| Check | Result |
|-------|--------|
| `python --version` | Python 3.10.12 (project venv) |
| `python -m compileall src scripts` | exit 0 |
| `python -m unittest discover -s tests` | `Ran 109 tests` … `OK` |
| CLI, valid fixture with `--standard` | exit 0, **53.8, Weak fit**, 8 sections |
| Worked example in the standard | `53.75 → **53.8, Weak fit**` (matches the evaluator) |
| Negative: wrong-case location | exit 1, "does not exactly match a CV heading (closest heading is …)" |
| Negative: wrong dash (en dash, and hyphen) | exit 1 for each, same message |
| Negative: nonexistent heading | exit 1 |
| Negative: fabricated quote | exit 1, "quote not found verbatim in CV section …" |
| Negative: malformed assessment | exit 1, 4 structural errors |
| Negative: standard-weight mismatch | exit 1, "is 65 in the standard but 70.0 in the evaluator" |
| Repository hygiene | Only `.venv/` is ignored. Manual reports, mutated JSON and drifted standards were written to the session scratchpad outside the repository. Python caches were removed. The untracked files are exactly `pytest.ini`, `tests/fixtures/` (4 files), `tests/support.py`, `tests/test_boundaries.py`, `tests/test_cli.py` and `tests/test_report.py`. |

#### Still unresolved

1. **Quote matching is still more lenient than "verbatim".** It strips `*` and
   backticks and unifies dash characters, as well as collapsing whitespace
   (which is needed for wrapped lines). Case is preserved. The same applies to
   `source_quote` in `additional_requirements`. This is the same kind of
   alignment issue as ALIGN-1, but quotes were outside this review's scope.
   Decision needed: tighten to whitespace-only normalisation, or document the
   tolerance in the standard.
2. **pytest has not been run** (ENV-1).
3. **Free-text sections** are reviewed by the manager; no automated checking
   (by manager decision).
4. **The Milestone 2 commit** is pending manager approval.

### Milestone 2 — verbatim quote matching (manager review 4)

**Date:** 2026-10-27
**Trigger:** Milestone 2 approved except for one standards-alignment issue.
Milestone 3 has not started. Nothing has been committed. All earlier entries are
kept as written.

#### ALIGN-2: quote matching vs. "verbatim" (a standards-alignment correction found during managerial review)

- **Discrepancy (open item 1 of review 3):** the standard requires quotes to be
  "verbatim". Before validating `Evidence.quote` and `additional_requirements`
  `source_quote`, the validator stripped `*` and backticks, converted em and en
  dashes to hyphens and collapsed all whitespace. Case and punctuation were
  already preserved. A quote with a hyphen where the source has an em dash, or
  with emphasis or backticks removed, therefore passed.
- **Manager decision:** comparison must preserve case, punctuation, dash
  characters, Markdown inline markers, backticks, wording and internal spacing.
  Only CRLF/LF line endings and whitespace surrounding the quote may be
  normalised. The same rule applies to both quote types.

#### Implementation change

- **`src/evaluator.py`:**
  - The new `_contains_verbatim(source, quote)` converts CRLF/CR to LF in both
    strings and strips whitespace only from the ends of the quote, then tests
    plain substring containment. A quote that is empty after stripping never
    matches.
  - It is used for `Evidence.quote` (within the cited CV section's body) and
    for `source_quote` (within the full job-description text).
  - `normalise_text` is no longer imported by the evaluator.
- **`src/parser.py`:**
  - `parse_cv` now builds each section body as an **exact slice** of the source
    text (`splitlines(keepends=True)` joined with `""`). Previously it used
    `splitlines()` joined with `"\n"`, which would silently turn Unicode line
    separators into `\n` and drop the final newline, so a body was not strictly
    source text. A check confirmed that every Candidate A section body is now an
    exact substring of the file.
  - The normalisation helpers are kept only for job-description section-name
    lookup and the diagnostic "closest heading" hint. A comment now says they
    are never used for quote or location validation.
- **Files are read with universal newlines** (`Path.read_text`), so CRLF in the
  CV or JD files is already presented as LF.
- **Standard, section 4:** added the manager's clarification sentence verbatim:
  "Verbatim means character-for-character source text, apart from surrounding
  whitespace and platform line-ending differences." The existing "verbatim"
  wording is unchanged and no examples were added.

#### Exact quote-normalisation policy

| Normalised (allowed) | Preserved (must match exactly) |
|----------------------|--------------------------------|
| CRLF and lone CR → LF, in quote and source | Letter case |
| Leading and trailing whitespace of the quote | Punctuation |
| | Hyphen, en dash and em dash |
| | `*`, `**`, `_` and other inline markers present in the source |
| | Backticks |
| | Wording |
| | Internal spacing, including line breaks **and the indentation of continuation lines** |

#### Fixture changes (neutral fixtures only)

- `tests/fixtures/cv_fixture.md`: added one wrapped bullet under the fixture
  role, ``- Rewrote the `alpha-cli` wrapper — **twice** as fast as the`` /
  `  previous script.`
- `tests/fixtures/job_description_fixture.md`: added one Responsibilities line,
  ``- Maintain the `beta-sync` service — **weekly**, with partner teams.``
- Both give the tests an em dash, backticks, `**` and a line wrap to
  discriminate against. Neither line is cited by
  `assessment_fixture.json`, so the fixture score is unchanged (53.8).
- No Candidate A file was changed, and no Candidate A text was used in quote
  tests.

#### Tests

- **Removed:** `test_quote_tolerates_line_wrapping_whitespace`. It asserted the
  whitespace-collapsing behaviour that is now prohibited.
- **Added `TestVerbatimQuotes` (10 tests, 14 subtests):**
  - **Pass:** exact quote; exact multi-line quote with its original line break
    and indentation; the same quote with CRLF; surrounding whitespace; exact
    `source_quote`.
  - **Fail, for both `Evidence.quote` and `source_quote`:** wrong case, hyphen
    for em dash, en dash for em dash, emphasis markers removed, backticks
    removed, internal spacing altered, punctuation changed.
  - **Fail, evidence quotes:** a line wrap collapsed to a single space; a line
    wrap with its indentation removed; a whitespace-only quote.
- **Mutation check:** with the old normalising matcher patched back in (in
  memory only, no file change), `TestVerbatimQuotes` produced 13 failures: the
  hyphen, en-dash, emphasis, backtick and spacing variants for both quote types
  (10), plus collapsed wrap, re-indented wrap and whitespace-only. Case and
  punctuation were already enforced before, so those variants pass under both
  matchers. The new tests therefore discriminate.
- **Suite:** 109 → **118 tests**: 10 added, 1 removed.

#### Defects in this cycle

- **Code:** ALIGN-2 above, plus the exactness of section bodies. No test defects
  were encountered: the new tests passed on their first run after the
  implementation change.
- **Environment (ENV-1, unchanged):** pytest has not been executed. It is
  unavailable, and installing it requires network access that was not
  permitted. The authoritative run is `python -m unittest discover -s tests`.

#### Validation results

| Check | Result |
|-------|--------|
| `python -m compileall src scripts` | exit 0 |
| `python -m unittest discover -s tests` | `Ran 118 tests` … `OK` |
| CLI, valid fixture with `--standard` | exit 0, **53.8, Weak fit**, 8 sections |
| Positive control: an exact quote containing an em dash, backticks and `**` substituted into M1 | exit 0 |
| Negative: fabricated quote | exit 1, "quote not found verbatim" |
| Negative: hyphen for em dash | exit 1 |
| Negative: en dash for em dash | exit 1 |
| Negative: emphasis markers removed | exit 1 |
| Negative: backticks removed | exit 1 |
| Negative: malformed assessment | exit 1, 4 structural errors |

#### Consequence for Milestone 3 (flagged, no action taken)

Because internal whitespace is no longer collapsed, a quote that spans a
wrapped line in the CV must reproduce the line break **and** the next line's
leading indentation exactly. Many Candidate A bullets wrap across lines. The
Run 1 instructions and JSON schema description will need to say, for example,
"quote within a single source line" or "preserve line breaks and indentation
exactly (as `\n` plus spaces in JSON)". Otherwise, Run 1 may produce validation
failures that come from the format, not from the agent's judgement. This is an
Instructions-lever consideration for the manager when the Run 1 prompt is
written.

#### Still unresolved

1. pytest has not been run (ENV-1).
2. Free-text sections are reviewed by the manager (by decision).
3. The Milestone 2 commit is pending manager approval.

---

## Milestone 3A — Run 1 workspace preparation

**Date:** 2026-10-27
**Status:** Workspace prepared and validated, awaiting manager review. **Run 1
has NOT been executed**, and no candidate evaluation was performed by the
implementation agent. Nothing has been committed.

### Location

- **Workspace:** `~/HamanLabs/agent-capstone-run1/`, created fresh. It did
  not exist before (verified), so nothing was overwritten.
- **Why there:** it sits outside the repository tree, and its parent
  (`~/HamanLabs/`) contains nothing else. An `ls ..` from the workspace
  therefore shows no repository. A sibling directory inside the repository's
  parent folder would have listed the repository next to it.
- **Reusable form:** to recreate, make an empty directory outside the
  repository, copy the four `context/` files at the recorded commit, add the
  frozen prompt, and regenerate the manifest.

### Source commit

`0beeff55ac2b249459c18254a23b079462fb44f0` (`0beeff5`, "Milestone 2: implement
deterministic evaluation framework"). The working tree was clean at copy time.

### Files included (exactly six; no directories)

| File | Role | SHA-256 | Source |
|------|------|---------|--------|
| `candidate_cv.md` | evaluation_source | `89b0b6b29087f460020a883c89701234bc1e2ab7491f6edc905632761bc5de29` | `context/candidate_cv.md` @ `0beeff5` |
| `job_description.md` | evaluation_source | `7f44b76aa738882a78e1ad3a253027c1be4e363eac38bc63f5eb56427f2f57d2` | `context/job_description.md` @ `0beeff5` |
| `evaluation_standard.md` | evaluation_source | `ccedfeea9a0ad52fd71159c062bce3274a80349b6bb625cfd5fe8fda23573318` | `context/evaluation_standard.md` @ `0beeff5` |
| `irrelevant_reference.md` | excluded_source | `4ac442942ee6258df236fa9ff8ca42fdd6568f30c5eebf3811b31a6b15ccc952` | `context/irrelevant_reference.md` @ `0beeff5` |
| `run1_prompt.md` | instruction_file | `2f4422727209b8212ca7941aa4375c38c66a7e35acd533d15869acd4ca8b5f9c` | Created in Milestone 3A; **frozen** |
| `manifest.json` | audit_metadata | `6cd486974af93e11e59f1b481a0b3a0dbeac99d5079677ee82a694024b9a0280` | Created in Milestone 3A; its own hash is recorded here because a file cannot contain its own hash |

All six files are read-only (`chmod 444`), so an agent session cannot silently
alter its inputs. The directory stays writable so that the run can create
`assessment.json` and `trajectory.md`.

### Files intentionally excluded

`README.md`, `.gitignore`, `requirements.txt`, `pytest.ini`, `.git/`,
`capstone/` (including this log), `reviews/`, `runs/`, `prompts/`, `src/`,
`tests/` (including the fixtures), `scripts/`, `.venv/`. No manager notes,
answer keys, milestone history, or other runs' prompts or outputs were copied,
and none exist in the repository to copy.

### Prompt design (run1_prompt.md)

- **Source boundary:** the CV, job description and standard may be used.
  `irrelevant_reference.md` may be seen but must not be used, and the prompt says
  explicitly that it must not be used as evidence or context. The workspace
  boundary sentence is included verbatim, and the prompt adds "Do not use the
  web".
- **Output:** exactly two new files, `assessment.json` and `trajectory.md`;
  existing files must not be modified.
- **JSON shape and validation rules** match the framework exactly:
  - The template's field names were checked programmatically against the
    parser's key sets (top level, assessment, evidence, `sources_excluded` and
    `additional_requirements` items), and `schema_version` = 1. All match.
  - The prompt states the validator's rules: no unknown fields, full and
    non-duplicated coverage, status/grade/evidence consistency, an UNCLEAR
    verification question, the `A1…` ID pattern, exact locations and verbatim
    quotes.
  - Scores are excluded from the JSON, because the framework calculates them.
- **`additional_requirements`** appears in the template as `[]`, with a neutral
  description of its shape: optional, and anything listed must also be
  assessed. The prompt gives no explanation of its purpose and no instruction to
  look for further requirements.
- **Quote rule:** every element the manager required is present. It includes an
  illustration using **invented** text (not Candidate A's), and all four
  accept/reject verdicts in that illustration were confirmed against the real
  validator.
- **Trajectory:** nine required sections of concise decision records and
  observable steps. Private internal reasoning is explicitly not requested.
- **Quality rules:** no fabricated experience, years, technologies,
  certifications or metrics; evidence-backed statuses; explicit uncertainty;
  compliance with the standard.
- **Freeze:** the prompt was finalised before hashing. Its SHA-256 is recorded
  in the manifest and above, and it is not to be modified unless the manager
  rejects Milestone 3A.

### Validation performed

1. **Tree:** 6 files and 0 directories, including hidden entries.
2. **File set:** exactly the six expected files.
3. **Subdirectories:** none.
4. **Prompt leak check:**
   - "hidden test", "on-call", "deliberate trap", "answer key", "Milestone 1"
     and "Milestone 2" each occur **0** times (case-insensitive).
   - A broader scan found no "hidden", "embedded", "trap", "distractor",
     "milestone", "capstone", "manager", "expected", "/home", repository name,
     "Candidate A" or candidate-specific technologies.
   - "deliberate" occurs twice, only in the manager-mandated trajectory headings
     ("Assumptions deliberately avoided", "files you deliberately did not use").
5. **irrelevant_reference.md prohibition:** present.
6. **Workspace boundary sentence:** present verbatim.
7. **Strict quote-formatting instructions:** all elements present.
8. **SHA-256:** independently recomputed with `sha256sum`, not the Python that
   generated the manifest. All five embedded hashes match; the manifest's own
   hash is recorded above.
9. **Byte-for-byte check:** with `cmp`, all four copied files are identical to
   both the repository working tree and the committed `HEAD` blobs
   (`git show HEAD:context/<file>`).
10. **No evaluation run:** no `assessment.json` or `trajectory.md` exists.
11. **Session context:** no `CLAUDE.md` exists in the home directory, its
    ancestors or `~/.claude/`, and this repository's Claude memory directory is
    empty. A fresh session started in the workspace therefore loads no
    project-specific instructions or memory.

### Finding raised for manager decision (no action taken)

**LEAK-1: milestone history in the copied standard.** A sweep of **all**
workspace files, not only the prompt, found that `evaluation_standard.md`
(copied byte for byte, as required) contains:
- line 3: "**Version:** 0.1 (Milestone 1 draft, initial model, subject to
  revision after Run 1)";
- line 7: "…is built in Milestone 2."

These lines date from Milestone 1. They reveal no test design, answers or
traps. They do tell the run agent that the work is staged, that this is "Run 1"
and that the standard may be revised afterwards: a mild observer-effect risk.

The leak checks the manager defined covered `run1_prompt.md` only, so this was
not caught by them. The copy was not edited, because that would break byte
equality with the source commit.

Options:
- **(a)** accept and record it;
- **(b)** neutralise the two lines in `context/evaluation_standard.md` (a
  context change before Run 1), commit, then re-copy and regenerate the
  manifest. The frozen prompt is unaffected.

(`job_description.md` also contains "on-call". That is the unchanged source
material itself, not a leak.)

### Remaining isolation limitations

1. **Isolation is procedural, not enforced by a container.** A Claude Code
   session started in the workspace has the user's normal filesystem
   permissions and could read the repository by absolute path if it chose to.
   The defences are:
   - the location outside the repository, with an empty parent;
   - no repository path or project name in any workspace file;
   - the explicit boundary instruction;
   - the manager's review of the run's trajectory and tool log for any access
     outside the workspace.

   Containers remain out of scope under the "no Docker" constraint.
2. **The session must be started correctly.** The working directory must be
   `~/HamanLabs/agent-capstone-run1/`, the session must be fresh with no
   inherited conversation, and no `--add-dir` may point at the repository. It
   must not be this implementation session, which knows the test design.
3. **The manifest is visible to the agent.** It shows relative source paths
   (`context/…`), the source commit and the label "Milestone 3A", as required.
   These reveal provenance but not test design.
4. **Read-only permissions are a guard, not a guarantee.** The file owner can
   reverse `chmod`. Tampering is detectable by re-hashing against this log.
5. **The prompt cannot be self-checked by the agent against the validator**,
   because no code is in the workspace. Validation happens afterwards, when the
   manager runs the repository CLI on the returned `assessment.json`.

### Not done (by instruction)

- Run 1 has not been executed. No `assessment.json` or `trajectory.md` exists,
  and nothing has been copied into `runs/run1/`.
- `prompts/run1_prompt.md` in the repository is still the Milestone 1
  placeholder. Copying the frozen prompt into it, so that the repository record
  matches SHA-256 `2f442272…5f9c`, is suggested for the manager's approval
  alongside the Milestone 3A commit.

### Milestone 3A — LEAK-1 correction (pre-Run-1 context sanitisation)

**Date:** 2026-10-27
**Manager decision:** LEAK-1 is accepted as a **pre-Run-1 CONTEXT issue** and
is to be corrected before the semantic agent sees the material (option b).
The frozen `run1_prompt.md` is approved unchanged (SHA-256
`2f4422727209b8212ca7941aa4375c38c66a7e35acd533d15869acd4ca8b5f9c`).

**Correction applied to `context/evaluation_standard.md` (metadata only):**

| Line | Before | After |
|------|--------|-------|
| 3 | `**Version:** 0.1 (Milestone 1 draft, initial model, subject to revision after Run 1)` | `**Version:** 0.1` |
| 6–7 | "The scoring engine that applies it is built in Milestone 2." | "Scores are calculated from the recorded statuses and evidence grades using the scoring model in section 6." |
| 91 | `## 6. Scoring model (initial)` | `## 6. Scoring model` |

- **Line 91 was outside the manager's search list.** I changed it on my own
  judgement, because "(initial)" carries the same "will be revised" signal as
  "subject to revision". It is a heading label, not a rule. Flagged for the
  manager to confirm.
- **Unchanged:** scoring rules, weights, status definitions, decision rules,
  evidence grades, citation and verbatim rules, rounding, requirement
  classification, the worked example and the output requirements.
  `git diff` shows only the three lines above.
- **No new wording** about hidden requirements, test cases, iteration,
  experiments, later runs or manager review was added.
- **Search:** "Milestone", "Run 1", "Run 2", "draft", "subject to revision" and
  "initial" each occur 0 times in the standard (case-insensitive).

**Timing:** the semantic agent has **not** seen either version. Run 1 has not
been executed, so the corrected file is the first version any run will see.

**Validation:**
- `python -m unittest discover -s tests` → `Ran 118 tests` … `OK`.
- CLI, valid fixture with `--standard` → exit 0, **53.8, Weak fit**, all 8
  sections. The scoring tables still match the evaluator.
