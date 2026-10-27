# Agent Capstone — Job Fit Evaluator

A reproducible, AI-assisted workflow that evaluates an **anonymised**
software-engineering candidate against a job description. It produces a
structured, evidence-backed hiring-fit assessment.

The project serves two purposes:

1. **The application.** A lightweight Python tool that maps job requirements to
   CV evidence, scores fit with a transparent rubric, and writes an assessment
   and an application brief.
2. **The management record.** Evidence of how an AI agent was directed, reviewed,
   diagnosed and re-run. The work trail (assumptions, decisions, failures,
   reviews and iterations) matters as much as the final output.

> All candidate, employer and job data in this repository is **synthetic**. No
> real person's information is used.

## What the workflow does

1. Reads an anonymised candidate CV and a job description.
2. Separates **mandatory** and **preferred** requirements.
3. Maps each requirement to evidence in the CV.
4. Assigns each requirement a status: `SUPPORTED`, `PARTIALLY_SUPPORTED`,
   `UNSUPPORTED` or `UNCLEAR`.
5. Scores fit using the rubric in
   [`context/evaluation_standard.md`](context/evaluation_standard.md).
6. Identifies genuine gaps and items that need verifying.
7. Recommends honest candidate positioning and writes an evidence-backed
   application brief.
8. Records an audit trail of the sources inspected, the decisions made and what
   remained uncertain.

## Safety rule: no fabrication

**The workflow must never invent candidate experience.**

If a skill, technology, responsibility, duration, achievement, certification or
metric is not supported by the candidate materials, it is labelled `UNSUPPORTED`
or `UNCLEAR`, never presented as fact. Professional experience is never inferred
from related technologies, and skills-list keywords on their own are never
treated as proven experience. See section 1 of the evaluation standard.

## Project structure

```
README.md                  Project overview (this file)
requirements.txt           Minimal dependencies (stdlib runtime, pytest for tests)
context/
  candidate_cv.md          Synthetic anonymised CV ("Candidate A")
  job_description.md       Synthetic job description (Backend Engineer, Python)
  evaluation_standard.md   Statuses, evidence rules, scoring model
  irrelevant_reference.md  Deliberate distractor: plausible but irrelevant material
prompts/
  run1_prompt.md           Original agent instructions (Run 1)
  run2_prompt.md           Revised instructions after diagnosis (Run 2)
runs/
  run1/ output.md, trajectory.md   Raw output and step log of Run 1
  run2/ output.md, trajectory.md   Raw output and step log of Run 2
reviews/
  run1_review.md           Manager review of Run 1
  diagnosis.md             Problems classified as Context / Workspace / Instructions
  run_comparison.md        Run 1 vs Run 2 comparison
src/
  models.py                Data models
  parser.py                CV / job description parsing
  evaluator.py             Requirement mapping and scoring
  report.py                Assessment rendering
tests/                     pytest suite
scripts/
  run_evaluation.py        CLI entry point
capstone/
  evidence_log.md          Running log of the agent's trajectory per milestone
  final_report.md          Final capstone report
  defense_notes.md         Notes for defending design and management decisions
```

### Why `irrelevant_reference.md` exists

This file contains plausible hiring material for a **different** role, including
a benchmark profile with skills that overlap the candidate's skills list. It is
there on purpose to test whether the agent restricts itself to the correct
sources. It must never be used as evidence about Candidate A.

## Milestones

| # | Milestone                               | Main outputs |
|---|-----------------------------------------|--------------|
| 1 | Project setup and context package       | Structure, context files, evaluation standard, evidence log |
| 2 | Evaluation engine and rubric            | `src/`, `tests/`, `scripts/run_evaluation.py` |
| 3 | Agent Run 1                             | `prompts/run1_prompt.md`, `runs/run1/` |
| 4 | Manager review and diagnosis            | `reviews/run1_review.md`, `reviews/diagnosis.md` |
| 5 | Agent Run 2 and comparison              | `prompts/run2_prompt.md`, `runs/run2/`, `reviews/run_comparison.md` |
| 6 | Capstone evidence and defence package   | `capstone/final_report.md`, `capstone/defense_notes.md` |

Work proceeds one milestone at a time, with a manager review after each.

## Capstone Workflow

1. **Context and workspace setup.** A synthetic context package (CV, job
   description, evaluation standard and a deliberate distractor file) and an
   isolation strategy. Each agent run works in its own external workspace that
   holds only frozen, read-only inputs and a SHA-256 manifest.
2. **Deterministic evaluation framework.** Python code (`src/`,
   `scripts/run_evaluation.py`) that parses the inputs, checks every citation
   against the CV (exact headings, verbatim quotes), calculates the score and
   renders the report. It never decides whether evidence meets a requirement;
   that judgment belongs to the agent.
3. **Run 1.** A fresh agent assessed the candidate using
   `prompts/run1_prompt.md`. Its assessment, trajectory and observable activity
   are preserved unedited in `runs/run1/`.
4. **Manager review and diagnosis.** Both the output and the trajectory were
   reviewed. Each problem was classified as a Context, Workspace or
   Instructions issue (INS-1, CTX-1, CTX-2, WS-1). A separate report-rendering
   defect (CODE-1) was fixed in the framework. See `reviews/run1_review.md` and
   `reviews/diagnosis.md`.
5. **Run 2 and comparison.** Only the diagnosed levers were changed:
   - an experience-duration rule and a rule for lists in parentheses, both in
     the standard;
   - a whole-job-description scope rule in `prompts/run2_prompt.md`;
   - a sanctioned `scratch/` directory in the workspace.

   A fresh agent then produced Run 2 (`runs/run2/`), compared with Run 1 in
   `reviews/run_comparison.md`.
6. **Final capstone and defense package.** `capstone/final_report.md` and
   `capstone/defense_notes.md` summarise the experiment, its results and its
   limitations. `capstone/evidence_log.md` holds the full milestone record.

## How agent iterations are preserved

- **Frozen prompts.** The exact instructions for each run are saved in `prompts/`
  before the run starts and are not edited afterwards.
- **Raw outputs.** Each run's output is saved unedited in `runs/runN/output.md`.
  Any correction belongs in a review or a later run, never in the original.
- **Trajectories.** `runs/runN/trajectory.md` records which files the agent read,
  what it decided, what it skipped and where it went wrong.
- **Reviews and diagnosis.** Problems found in Run 1 are each classified under
  one lever (**Context**, **Workspace** or **Instructions**). Run 2 changes
  only the diagnosed levers, so the comparison isolates their effect.
- **Evidence log.** `capstone/evidence_log.md` is appended to at every milestone
  with the files inspected and created, decisions, assumptions, uncertainties and
  exclusions.
- **Version control.** The repository is under git. Commits at milestone
  boundaries give a timestamped history of each stage.

## Requirements

- Python 3.10+ (developed on 3.10.12; code must stay 3.10-compatible)
- Runtime: standard library only. Tests: `pytest`.

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest            # available once tests are written in Milestone 2
```

## Status

**Milestone 1 complete, awaiting manager review.** Files for later milestones
are placeholders.
