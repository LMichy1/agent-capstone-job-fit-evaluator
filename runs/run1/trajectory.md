# Trajectory — Candidate A job-fit assessment

## 1. Files inspected

1. `run1_prompt.md` (task instructions)
2. `candidate_cv.md`
3. `job_description.md`
4. `evaluation_standard.md`

## 2. Steps taken

1. Listed the workspace and read `run1_prompt.md`.
2. Read `candidate_cv.md` (with non-printing characters shown, to confirm the em/en dashes in headings and date lines), `job_description.md` and `evaluation_standard.md`.
3. Assessed each of the 12 numbered requirements (M1–M6, P1–P6) against the CV using the standard's statuses, decision rules and grades.
4. Generated `assessment.json` with a script in the session scratchpad (outside the workspace) so JSON escaping was exact.
5. Ran a validation script (also in the scratchpad) checking allowed fields, ID coverage, status/grade/evidence consistency, that every location matches a CV heading, and that every quote appears verbatim inside the named section. All checks passed.
6. Wrote this file.

## 3. Decisions

| ID | Status | Grade | Key reason |
|----|--------|-------|------------|
| M1 | UNCLEAR | B | Python backend work evidenced, but the main role is ~2 yrs 3 mos to the June 2024 CV date; reaching 3 years depends on a part-time role with unstated hours and an internship. |
| M2 | PARTIALLY_SUPPORTED | A | Building REST APIs evidenced; designing them is not stated. |
| M3 | PARTIALLY_SUPPORTED | A | Schema design (PostgreSQL) and queries (MySQL) evidenced; no query performance tuning. |
| M4 | PARTIALLY_SUPPORTED | A | pytest unit tests and GitHub Actions CI evidenced; no integration tests. |
| M5 | SUPPORTED | A | Code review via GitHub pull requests in two professional roles. |
| M6 | PARTIALLY_SUPPORTED | A | Deployed to AWS EC2; operating services in production not described. |
| P1 | PARTIALLY_SUPPORTED | B | Docker Compose run locally on a personal project only; not production. |
| P2 | UNCLEAR | C | Kubernetes only in the Skills list. |
| P3 | PARTIALLY_SUPPORTED | B | Celery and Redis in a personal project only; Kafka only in Skills. |
| P4 | PARTIALLY_SUPPORTED | B | "Helped onboard two interns" in a part-time role; contributing role, no mentoring described. |
| P5 | PARTIALLY_SUPPORTED | A | Structured JSON logging evidenced; no metrics or tracing. |
| P6 | SUPPORTED | B | Completed BSc Computer Science, 2021; education evidence graded B per the standard. |

No mandatory requirement is UNSUPPORTED, so no mandatory gap applies.

## 4. Key evidence used

- `Candidate CV — Candidate A`: "**CV last updated:** June 2024"
- `Software Engineer — Example Logistics Ltd *(fictional)*`: "**March 2022 – Present**"
- same: "- Built and maintained REST APIs with Django REST Framework for an internal"
- same: "- Designed PostgreSQL table schemas and wrote database migrations for new"
- same: "- Set up a GitHub Actions workflow that runs the test suite on every pull request."
- same: "- Deployed services to AWS EC2 using a scripted release process."
- same: "- Added structured JSON logging to the tracking service."
- `Junior Developer (part-time, alongside final year of degree) — Example Pay Startup *(fictional)*`: "**January 2021 – February 2022**", "- Helped onboard two interns to the codebase."
- `Parcel Notifier *(personal project)*`: "Uses Celery and Redis for … runs locally with Docker Compose." (quoted in full, across the wrapped line, in `assessment.json`)
- `Education`: "- **BSc Computer Science** — Example State University *(fictional)*, 2021."

## 5. Uncertainties

- Full-time-equivalent Python experience (M1): hours in the part-time role and employment type of the current role are not stated.
- Whether the candidate designed APIs, tuned queries, wrote integration tests or supported services in production.
- Size of the "significantly improved" test coverage.
- Any real use of Kubernetes, Kafka or Terraform (Skills list only).

## 6. Requirements not verifiable

- **M1:** the duration cannot be confirmed from the CV; marked UNCLEAR with a verification question.
- **P2:** Kubernetes appears only as a skills keyword; marked UNCLEAR with a verification question.

## 7. Assumptions deliberately avoided

- Did not count the part-time role or the internship as full-time years, and did not estimate years.
- Did not interpret "Present" as today's date; used the June 2024 last-updated date.
- Did not treat the in-progress AWS Cloud Practitioner certification as held.
- Did not treat Docker Compose on a personal project as production containerisation, or Celery on a personal project as professional experience.
- Did not credit Skills-list keywords (Kubernetes, Kafka, Terraform, Docker) as experience.
- Did not infer API design from schema design, operations from deployment, or integration tests from unit tests.
- Did not turn "significantly improved test coverage" into a metric.

## 8. Files not used

- `irrelevant_reference.md`: the instructions say not to use it; it was not opened.
- `manifest.json`: workspace audit metadata, not a source; it was not opened.

## 9. Interpretation problems

- M1: the standard lists both "duration falls short" (PARTIALLY_SUPPORTED) and "employment type makes the duration impossible to confirm" (UNCLEAR). UNCLEAR was chosen because whether 3 years is met depends on unstated part-time hours, and it is the more conservative status.
- P5: "(structured logging, metrics, tracing)" could be read as examples or as the full scope; it was read as scope, giving partial credit.
- P6: the grade table classes education as grade B even when the requirement itself is a degree; B was applied as written.
- P4: "Helped onboard" could support the requirement fully; decision rule 1 (prefer PARTIALLY_SUPPORTED when in doubt) was applied.
- Responsibilities in the job description (e.g. on-call rotation, working with product managers) are not numbered requirements; they were not added as additional requirements.
- The standard's required output sections include a score breakdown, but the prompt says not to include scores in `assessment.json`; scores were left to the framework.
