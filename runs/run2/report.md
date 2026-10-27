# Job Fit Assessment — Candidate A

- **Job:** Job Description — Backend Software Engineer (Python)
- **Total score:** 61.8 / 100
- **Fit band:** Moderate fit

> **⚠ MANDATORY GAP:** unsupported mandatory requirement(s): A1.

## 1. Sources inspected

**Inspected:**

- `candidate_cv.md`
- `job_description.md`
- `evaluation_standard.md`

**Excluded:**

- `irrelevant_reference.md` — Designated 'Do not use' in run2_prompt.md; not opened and not used as evidence or context.
- `manifest.json` — Workspace audit metadata, designated 'Do not use' in run2_prompt.md; not opened and not used as a source.
- `run2_prompt.md` — Task instructions only; not a source of candidate evidence or role requirements.

## 2. Requirements assessment

| ID | Type | Requirement | Status | Grade | Evidence location | Quote | Reasoning |
|----|------|-------------|--------|-------|-------------------|-------|-----------|
| M1 | mandatory | At least 3 years of professional software engineering experience using Python for backend development. | **SUPPORTED** | B | Summary<br>Candidate CV — Candidate A<br>Software Engineer — Example Logistics Ltd *(fictional)*<br>Software Engineer — Example Logistics Ltd *(fictional)*<br>Junior Developer (part-time, alongside final year of degree) — Example Pay Startup *(fictional)*<br>Junior Developer (part-time, alongside final year of degree) — Example Pay Startup *(fictional)* | “Backend-focused software engineer working mainly in Python.”<br>“- **CV last updated:** June 2024”<br>“**March 2022 – Present**”<br>“- Built and maintained REST APIs with Django REST Framework for an internal”<br>“**January 2021 – February 2022**”<br>“- Developed Flask endpoints for a payments dashboard.” | Python backend work (Django REST Framework APIs; Flask endpoints) is evidenced in two professional roles. Counting calendar duration with 'Present' read as the CV's June 2024 date: Example Logistics March 2022 – June 2024 (about 27–28 months) plus Example Pay Startup January 2021 – February 2022 (about 13–14 months, part-time, flagged) gives roughly 40–42 months, and at least about 38 months even on the most conservative reading of month boundaries; the periods do not overlap. The standard counts part-time professional work by calendar duration, so the 3-year minimum is met. The June–August 2020 internship (CSV data scripts, not backend) is excluded. Grade B because reaching the threshold depends on a part-time role. |
| M2 | mandatory | Experience designing and building REST APIs. | **PARTIALLY_SUPPORTED** | A | Software Engineer — Example Logistics Ltd *(fictional)*<br>Junior Developer (part-time, alongside final year of degree) — Example Pay Startup *(fictional)* | “- Built and maintained REST APIs with Django REST Framework for an internal<br>  shipment-tracking service used by three internal teams.”<br>“- Developed Flask endpoints for a payments dashboard.” | Building REST APIs is directly evidenced in a professional role. The requirement is compound ('designing and building'); the CV does not state that the candidate designed the APIs (only that they built and maintained them), so per decision rule 4 the status is PARTIALLY_SUPPORTED. |
| M3 | mandatory | Experience with relational databases (e.g. PostgreSQL, MySQL), including schema design and query performance tuning. | **PARTIALLY_SUPPORTED** | A | Software Engineer — Example Logistics Ltd *(fictional)*<br>Junior Developer (part-time, alongside final year of degree) — Example Pay Startup *(fictional)* | “- Designed PostgreSQL table schemas and wrote database migrations for new”<br>“- Wrote MySQL queries for reporting features.” | Relational database use and schema design are directly evidenced in a professional role (PostgreSQL schemas and migrations; MySQL queries). Query performance tuning, an explicit part of the requirement ('including'), was searched for (tuning, indexing, optimisation, performance, slow queries) and not found. Compound requirement, so PARTIALLY_SUPPORTED. |
| M4 | mandatory | Experience writing automated tests (unit and integration) and working with continuous integration (CI) pipelines. | **PARTIALLY_SUPPORTED** | A | Software Engineer — Example Logistics Ltd *(fictional)*<br>Software Engineer — Example Logistics Ltd *(fictional)* | “- Wrote unit tests with pytest for the API layer and significantly improved test”<br>“- Set up a GitHub Actions workflow that runs the test suite on every pull request.” | Unit testing with pytest and setting up a CI workflow (GitHub Actions) are directly evidenced in a professional role. Integration testing, an explicit part of the requirement ('unit and integration'), was searched for and not found. Compound requirement, so PARTIALLY_SUPPORTED. The 'significantly improved test coverage' wording is vague and is not credited as a metric. |
| M5 | mandatory | Experience with Git-based collaboration, including code review. | **SUPPORTED** | A | Software Engineer — Example Logistics Ltd *(fictional)*<br>Junior Developer (part-time, alongside final year of degree) — Example Pay Startup *(fictional)* | “- Took part in code review for the team's pull requests.”<br>“- Took part in code reviews using GitHub pull requests.” | Git-based collaboration via GitHub pull requests and participation in code review are directly evidenced in two professional roles, covering both parts of the requirement. |
| M6 | mandatory | Experience deploying and operating services on a public cloud provider (AWS, GCP or Azure). | **PARTIALLY_SUPPORTED** | A | Software Engineer — Example Logistics Ltd *(fictional)* | “- Deployed services to AWS EC2 using a scripted release process.” | Deploying services to a public cloud provider (AWS EC2) is directly evidenced in a professional role. Operating those services (monitoring, incident response, production support, scaling) was searched for and not explicitly found; the structured-logging bullet is not tied to operating on AWS. Compound requirement ('deploying and operating'), so PARTIALLY_SUPPORTED. The AWS Cloud Practitioner certification is in progress and is not credited. |
| P1 | preferred | Experience using Docker or other containerisation in production. | **PARTIALLY_SUPPORTED** | B | Parcel Notifier *(personal project)*<br>Skills | “background jobs, and runs locally with Docker Compose.”<br>“GitHub Actions, AWS, Docker, Kubernetes, Kafka, Terraform, Redis, Celery, Linux.” | Docker use is evidenced only through Docker Compose run locally on a personal project, plus a skills-list keyword. The requirement asks for containerisation in production; per the standard, local Docker Compose on a personal project is not production containerisation, so this meets the requirement only in a weaker context: PARTIALLY_SUPPORTED, grade B. |
| P2 | preferred | Experience with Kubernetes. | **UNCLEAR** | C | Skills | “GitHub Actions, AWS, Docker, Kubernetes, Kafka, Terraform, Redis, Celery, Linux.” | Kubernetes appears only as a keyword in the Skills list, with no supporting experience in any role or project. Per decision rule 2 this is UNCLEAR, grade C. |
| P3 | preferred | Experience with message queues or asynchronous task processing (e.g. Celery, RabbitMQ, Kafka). | **PARTIALLY_SUPPORTED** | B | Parcel Notifier *(personal project)* | “- A side project that sends delivery notifications. Uses Celery and Redis for<br>  background jobs, and runs locally with Docker Compose.” | Asynchronous task processing with Celery and Redis is directly described, but only in a personal side project, not a professional role. Personal-project experience is a weaker context, so PARTIALLY_SUPPORTED, grade B. Kafka appears only in the Skills list and is not credited. |
| P4 | preferred | Experience mentoring or onboarding less experienced engineers. | **SUPPORTED** | B | Junior Developer (part-time, alongside final year of degree) — Example Pay Startup *(fictional)* | “- Helped onboard two interns to the codebase.” | The requirement accepts mentoring or onboarding as alternatives; helping onboard two interns to the codebase is direct evidence of onboarding less experienced engineers in a professional role. Grade B because the role was part-time and the wording ('helped') indicates a shared contribution. |
| P5 | preferred | Experience with observability tooling (structured logging, metrics, tracing). | **PARTIALLY_SUPPORTED** | A | Software Engineer — Example Logistics Ltd *(fictional)* | “- Added structured JSON logging to the tracking service.” | The parenthetical '(structured logging, metrics, tracing)' is a bare comma-separated list, treated as cumulative scope. Structured logging is directly evidenced in a professional role; metrics and tracing were searched for and not found. PARTIALLY_SUPPORTED. |
| P6 | preferred | Bachelor's degree in Computer Science or a related field. | **SUPPORTED** | B | Education | “- **BSc Computer Science** — Example State University *(fictional)*, 2021.” | A completed BSc in Computer Science (2021) is stated, meeting the requirement in full. Grade B because the evidence is from education rather than a professional role, per the grade definitions. |
| A1 † | mandatory | Participate in the team's on-call rotation (roughly one week in six). | **UNSUPPORTED** ⚠ MANDATORY GAP | C | No evidence cited | — | Searched the whole CV for on-call, rota/rotation, pager, incident response, out-of-hours or production support; none found. The CV gives no evidence of on-call experience or of availability for an on-call rotation. |
| A2 † | mandatory | Work remotely within EMEA time zones. | **SUPPORTED** | B | Candidate CV — Candidate A | “- **Location:** Remote, EMEA” | The CV states the candidate's location as 'Remote, EMEA', directly matching the role's remote EMEA time-zone condition. Grade B rather than A because this is a personal detail in the CV header, not evidence from a professional role. |

_† Requirement identified by the assessor outside the labelled requirement lists._

## 3. Score breakdown

| Component | Weight | Score |
|-----------|-------:|------:|
| Mandatory requirements | 70 | 43.75 |
| Preferred requirements | 20 | 11.67 |
| Evidence quality / confidence | 10 | 6.43 |
| **Total** (rounded to one decimal) | 100 | **61.8** |

**Fit band:** Moderate fit

_Component scores are shown to two decimals for display; only the total is rounded under the standard._

## 4. Genuine gaps

**Mandatory (⚠ MANDATORY GAP):**

- **A1** — Participate in the team's on-call rotation (roughly one week in six).

**Preferred:**

_None._

## 5. Items to verify

- **P2** — Experience with Kubernetes.
  - Question for the candidate: Where have you used Kubernetes (professionally or otherwise), and what did you do with it — e.g. writing manifests or Helm charts, deploying services, or operating a cluster?

## 6. Recommended positioning

Position Candidate A as a Python backend engineer with professional experience from January 2021 to June 2024 (the first role part-time) building REST APIs with Django REST Framework and Flask, designing PostgreSQL schemas and writing migrations, writing pytest unit tests, setting up a GitHub Actions CI workflow, deploying services to AWS EC2 via a scripted release process, adding structured JSON logging, and taking part in GitHub pull-request code review. Supporting points: helped onboard two interns, holds a BSc in Computer Science (2021), is based remotely in EMEA, and has used Celery, Redis and Docker Compose on a personal project. Do not claim API design ownership, query performance tuning, integration testing, operating cloud services, production containerisation, Kubernetes, Kafka, metrics/tracing, on-call experience or a completed AWS certification; mandatory gap: no evidence of on-call experience or availability (A1), which must be addressed directly.

## 7. Application brief

Candidate A is a remote, EMEA-based backend engineer working mainly in Python. At Example Logistics Ltd (March 2022 – present, CV dated June 2024) they built and maintained REST APIs with Django REST Framework for an internal shipment-tracking service used by three internal teams, designed PostgreSQL table schemas and migrations, wrote pytest unit tests for the API layer, set up a GitHub Actions workflow running the test suite on every pull request, deployed services to AWS EC2 using a scripted release process, added structured JSON logging, and took part in code review. Previously, in a part-time role (January 2021 – February 2022), they developed Flask endpoints, wrote MySQL reporting queries, reviewed code via GitHub pull requests and helped onboard two interns. They hold a BSc in Computer Science (2021); an AWS Cloud Practitioner certification is in progress. Points to verify: API design responsibility, query tuning, integration testing, operating services, Kubernetes, and on-call availability.

## 8. Uncertainties and assumptions

- Mandatory gap: the CV contains no evidence of on-call experience or availability for the on-call rotation (A1).
- M1 duration is computed from month-level dates with 'Present' read as June 2024 (CV last-updated date); it relies on a part-time role (January 2021 – February 2022) whose hours are not stated. The internship (June–August 2020) is excluded.
- Responsibilities and the 'Location' line were judged to be explicit obligations/conditions; on-call (A1) and location (A2) were not labelled mandatory or preferred in the job description and were treated as mandatory per the standard's rule for ambiguous types.
- 'Significantly improved test coverage' is vague and was not credited as a metric.
- Kubernetes, Kafka and Terraform appear only in the Skills list; Docker appears professionally nowhere and only locally in a personal project.
- The AWS Certified Cloud Practitioner certification is in progress and was not treated as held.
- The 'quarterly in-person team weeks' condition under 'What we offer' was not assessed as a requirement; the CV gives no information on travel availability.

**Per-requirement notes:**

- **M1:** Exact start/end days within the stated months are not given; the part-time role's hours are unknown (not needed since full-time equivalence is not required). The Logistics role does not name Python explicitly; it is evidenced through Django REST Framework and the Summary.
- **M2:** Whether the candidate was responsible for API design (resource modelling, contracts, versioning) is not stated.
- **M3:** No evidence on query performance tuning; writing reporting queries does not establish tuning experience.
- **M4:** Whether the candidate has written integration tests is not stated; the size of the coverage improvement is unquantified.
- **M6:** Extent of the candidate's operational responsibility for the deployed services is not stated.
- **P1:** No evidence of containers in any professional or production deployment; the professional deployment cited is to AWS EC2 via a scripted release process.
- **P2:** Context and depth of any Kubernetes experience are unknown.
- **P3:** No professional use of message queues or task queues is evidenced; Kafka experience is unverified.
- **P4:** The extent of the candidate's onboarding role and any ongoing mentoring are not described.
- **P5:** No evidence of metrics or tracing tooling; the specific logging tooling used is not named.
- **A1:** This is an obligation of the role that a CV may not address; the gap reflects absent evidence, not a stated unwillingness.
- **A2:** The specific country or time zone within EMEA is not stated.

---

_Rendered deterministically by the Job Fit Evaluator framework. Statuses, evidence grades, rationale and narrative sections were supplied by the assessor; the framework validated citations and calculated scores but made no semantic judgements._
