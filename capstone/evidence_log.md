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
