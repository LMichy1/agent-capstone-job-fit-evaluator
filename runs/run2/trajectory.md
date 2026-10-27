# Trajectory — Candidate A job-fit assessment

## 1. Files inspected

1. `run2_prompt.md` (task instructions)
2. `candidate_cv.md` (inspected with visible-character output to confirm em/en dashes)
3. `job_description.md`
4. `evaluation_standard.md`

`irrelevant_reference.md` and `manifest.json` were not opened.

## 2. Steps taken

1. Read the instructions, then the three permitted sources.
2. Listed the CV headings (`grep '^#'`) to get exact `location` strings.
3. Extracted requirement IDs M1–M6 and P1–P6; reviewed every other line of the job description for obligations/conditions.
4. Assessed each requirement against the standard's statuses, decision rules, duration rules and grade definitions.
5. Wrote `assessment.json`.
6. Wrote `scratch/validate.py` and ran it: checks allowed fields, coverage, status/grade/evidence consistency, exact heading locations, verbatim CV quotes within the named section, and verbatim `source_quote` in the job description. Result: OK.
7. Wrote this file.

## 3. Decisions

| ID | Status | Grade | Key reason |
|----|--------|-------|------------|
| M1 | SUPPORTED | B | Python backend work in two non-overlapping professional roles: Mar 2022–Jun 2024 (CV date) + Jan 2021–Feb 2022 (part-time, flagged) ≈ 40–42 months, ≥ 3 years by calendar duration. Internship excluded. B because the threshold relies on a part-time role. |
| M2 | PARTIALLY_SUPPORTED | A | "Built and maintained" REST APIs evidenced; "designing" not stated (compound). |
| M3 | PARTIALLY_SUPPORTED | A | PostgreSQL schema design and MySQL queries evidenced; no query performance tuning. |
| M4 | PARTIALLY_SUPPORTED | A | pytest unit tests and GitHub Actions CI evidenced; no integration tests. |
| M5 | SUPPORTED | A | Code review via GitHub pull requests in two professional roles. |
| M6 | PARTIALLY_SUPPORTED | A | Deployed to AWS EC2; "operating" not evidenced. Certification in progress not credited. |
| P1 | PARTIALLY_SUPPORTED | B | Docker Compose only locally on a personal project; not production. |
| P2 | UNCLEAR | C | Kubernetes only in Skills list; verification question supplied. |
| P3 | PARTIALLY_SUPPORTED | B | Celery + Redis background jobs in personal project only; Kafka skills-only. |
| P4 | SUPPORTED | B | "Helped onboard two interns" (onboarding is an accepted alternative); part-time role. |
| P5 | PARTIALLY_SUPPORTED | A | Structured JSON logging evidenced; metrics and tracing (cumulative list) not. |
| P6 | SUPPORTED | B | BSc Computer Science, 2021; education context. |
| A1 | UNSUPPORTED | C | No on-call/incident/production-support evidence found. Mandatory gap. |
| A2 | SUPPORTED | B | CV location "Remote, EMEA" matches remote EMEA time zones; header detail, not professional role. |

Scores were not written into `assessment.json`, as instructed.

## 4. Key evidence used

- `Candidate CV — Candidate A`: "- **CV last updated:** June 2024"; "- **Location:** Remote, EMEA"
- `Summary`: "Backend-focused software engineer working mainly in Python."
- `Software Engineer — Example Logistics Ltd *(fictional)*`: "**March 2022 – Present**"; "- Built and maintained REST APIs with Django REST Framework for an internal"; "- Designed PostgreSQL table schemas and wrote database migrations for new"; "- Wrote unit tests with pytest for the API layer and significantly improved test"; "- Set up a GitHub Actions workflow that runs the test suite on every pull request."; "- Deployed services to AWS EC2 using a scripted release process."; "- Added structured JSON logging to the tracking service."; "- Took part in code review for the team's pull requests."
- `Junior Developer (part-time, alongside final year of degree) — Example Pay Startup *(fictional)*`: "**January 2021 – February 2022**"; "- Developed Flask endpoints for a payments dashboard."; "- Helped onboard two interns to the codebase."
- `Parcel Notifier *(personal project)*`: Celery/Redis background jobs; "runs locally with Docker Compose."
- `Education`: "- **BSc Computer Science** — Example State University *(fictional)*, 2021."
- `Skills`: Kubernetes, Kafka, Docker as keywords only.

## 5. Uncertainties

- Exact days within start/end months unknown; M1 holds even at the most conservative month reading (~38 months).
- Hours of the part-time role unknown (not needed; FTE not required).
- Whether the candidate designed APIs, tuned queries, wrote integration tests or operated services.
- "Significantly improved test coverage" is unquantified.
- Specific time zone within EMEA not stated.

## 6. Requirements not verifiable

- P2 (Kubernetes): skills-list keyword only; needs candidate confirmation.
- A1 (on-call): a CV cannot show availability; no on-call experience stated.
- Parts of M2, M3, M4, M6, P5 (design, tuning, integration tests, operating, metrics/tracing): not mentioned.

## 7. Assumptions deliberately avoided

- Did not treat "built" as "designed" APIs, or structured logging as operating services.
- Did not treat MySQL reporting queries as query performance tuning.
- Did not treat local Docker Compose as production containerisation, or personal-project Celery as professional use.
- Did not credit skills-list keywords (Kubernetes, Kafka, Terraform, Docker) as experience.
- Did not treat the in-progress AWS certification as held.
- Did not convert part-time to FTE, count the internship, or quantify "significantly improved".
- Did not read "Present" as today's date (used June 2024).

## 8. Files not used

- `irrelevant_reference.md`: designated "Do not use"; not opened.
- `manifest.json`: audit metadata, designated "Do not use"; not opened.
- `run2_prompt.md`: instructions only, not an evidence source.

## 9. Interpretation problems

- M1: the Logistics role does not name Python; Python is evidenced via Django REST Framework and the Summary line.
- Grade for non-professional but direct evidence (degree, location) — the grade table lists education as B; location treated the same way conservatively.
- P1 personal-project Docker: the standard both says "Docker Compose on a personal project is not production containerisation" and lists personal-project experience as a PARTIALLY_SUPPORTED signal; chose PARTIALLY_SUPPORTED/B since some (weaker-context) evidence exists.
- P4 "Helped onboard": judged sufficient for the "onboarding" alternative; uncertainty about extent recorded.
- A1/A2 type: not labelled mandatory or preferred; treated as mandatory per the standard's ambiguity rule.

## 10. Job description items outside the numbered lists

Assessed as additional requirements:
- **A1** (mandatory): "- Take part in the team's on-call rotation (roughly one week in six)." — an explicit obligation with fit implications (availability), not covered by any numbered requirement.
- **A2** (mandatory): "- **Location:** Remote (EMEA time zones)" — an explicit location/time-zone condition.

Considered but not treated as separate assessable requirements:
- Responsibilities "Design and implement RESTful APIs…", "Own services end to end…", "Model data and write efficient queries…", "Review teammates' code…": duties already covered by M2, M4, M6, M3 and M5; assessing them again would double-count.
- "contribute to engineering standards" and "Work with product managers to break down and estimate features": day-to-day duties performed after hire rather than candidate qualifications or employment conditions; noted that the CV has no evidence for either.
- "Level: Mid-level (Engineer II)": a role descriptor; experience level is assessed via M1.
- Employer, Team, "About the role": descriptive context, not obligations.
- "What we offer" (remote with quarterly in-person team weeks, learning budget, leave): framed as benefits, not candidate obligations; the in-person weeks are recorded as an uncertainty (CV gives no travel information).

## 11. Scratch files

- `scratch/validate.py`: created to validate `assessment.json` (schema fields, coverage, consistency, exact headings, verbatim quotes). Retained.
