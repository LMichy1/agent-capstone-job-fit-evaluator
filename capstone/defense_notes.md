# Defense Notes — Agent Capstone: Job Fit Evaluator

Spoken-answer prep for the two interviews. Answers are meant to be said in
your own words; the anchors underneath are what to remember.

---

## One-minute summary — "Tell me about your capstone."

> I had an agent evaluate an anonymised software engineer's CV against a job
> description and produce an evidence-backed fit assessment. Every claim had to
> be quoted verbatim from the CV, and a small Python framework checked the
> citations and calculated the score. The code never made the judgment calls.
>
> Run 1 was honest and valid. It scored 52.1, Weak fit. But when I reviewed
> the trajectory, not just the output, I found four problems:
> - it saw the on-call duty in the job description and deliberately left it
>   out, because it wasn't a numbered requirement;
> - the standard never said how to count years of experience;
> - one requirement's list was ambiguous;
> - it had written helper scripts outside the workspace.
>
> I mapped each problem to context, workspace or instructions, and changed
> only those things.
>
> Run 2 scored 61.8, Moderate fit, and it flagged the on-call duty as a
> mandatory gap. The main lesson: the score isn't the measure. The scope fix
> actually lowered the score. What improved was coverage, clarity and process,
> and I can trace every difference back to a specific change.

---

## Interview questions

### 1. What task did you choose and why?

Job-fit evaluation. You give the agent a CV, a job description and an
evaluation standard, and it returns a structured assessment: a status and
evidence grade per requirement, verbatim citations, gaps, items to verify,
and an application brief. I picked it because quality is checkable. There's an
obvious failure mode, inventing experience, and a written standard to judge
against. And it's realistic work that people actually use AI for.

- Candidate A, fictional employers, synthetic materials
- Output: `assessment.json` + `trajectory.md`
- Failure mode to watch: fabrication

### 2. Why was it suitable for an agent rather than a simple prompt?

It isn't one question, it's a process. The agent has to read three files,
pull out twelve requirements, judge each one against the rules, copy exact
quotes under exact headings, write narrative that only uses supported claims,
and then check its own work. Both of my agents actually wrote small validation
scripts to check their JSON before finishing. That's tool use and
self-verification, not a single answer.

- Multi-file reading, then per-requirement judgment
- Strict output format, validated by code
- Agents self-checked with scripts

### 3. What context did the agent need?

Three files it could use:
- the CV, as the only evidence about the candidate;
- the job description, as the only source of requirements;
- the evaluation standard, which defines statuses, decision rules, evidence
  grades, citation rules and scoring.

I also gave it an irrelevant reference file on purpose and told it not to use
it, to see whether it respected source boundaries. Neither run opened it.

- Use: CV, JD, standard
- See but don't use: `irrelevant_reference.md`, `manifest.json`
- Distractor never opened, in either run

### 4. How did you control what the agent could access?

Each run got its own workspace folder outside the repo, so the agent couldn't
see my code, tests, reviews or notes. It held only the files the run needed,
read-only, plus a manifest with SHA-256 hashes and the source commit. Each run
was a fresh session started inside that folder. I'll be honest that it's
procedural isolation, not a container, so I verified compliance afterwards
from the session transcripts.

- `~/HamanLabs/agent-capstone-run1` / `-run2`
- 444 permissions, manifest with hashes
- Not container-enforced → checked against transcripts

### 5. What did your initial prompt specify?

It specified:
- the goal and the file roles, with a "work only in this workspace" boundary;
- exactly two deliverables, and no other files;
- the exact JSON template and validation rules;
- a strict verbatim-quote rule, with examples of accepted and rejected quotes;
- quality rules: no fabrication, no invented years, no crediting Skills-list
  keywords;
- the trajectory sections, and a final self-check.

Scores were deliberately left out; the code calculates them.

- Template + validation rules + verbatim rule
- No scores from the agent
- `additional_requirements` was there but "optional"

### 6. What happened in Run 1?

It produced a valid assessment first time: 22 citations, all exact, and all
twelve requirements covered. The code scored it 52.1, Weak fit, with no
mandatory gap. It was very conservative, especially on M1, the
three-years-of-Python requirement, which it marked UNCLEAR because of a
part-time role with unknown hours. I accepted it as the baseline, not as the
right answer.

- 52.1, Weak, no gap, 0 additional requirements
- M1 UNCLEAR is what kept it in Weak
- Accepted as baseline, not endorsed

### 7. What did Run 1 do well?

Honestly, a lot:
- it didn't fabricate anything;
- it didn't credit Kubernetes just because it was in the Skills list;
- it didn't treat the in-progress AWS cert as held;
- it didn't turn "significantly improved test coverage" into a number;
- it downgraded the personal-project Docker work.

It also wrote down its own interpretation problems, which is what pointed me
to the context issues.

- No fabrication, no invented metrics
- Skills keywords → UNCLEAR, not SUPPORTED
- It flagged its own doubts (M1, P5)

### 8. What went wrong?

Four things on the agent side, plus one in my own code:
- **INS-1:** it saw the on-call duty and decided it was out of scope because
  it wasn't numbered.
- **CTX-1:** the standard didn't define how to count years of experience.
- **CTX-2:** one requirement had a list in brackets that could mean examples
  or full scope.
- **WS-1:** it wrote its helper scripts outside the workspace, even though it
  was told not to.
- **CODE-1:** my report renderer showed a "MANDATORY GAP" label when there
  wasn't one. That's a framework bug, not an agent problem.

- INS-1, CTX-1, CTX-2, WS-1 + CODE-1
- Output was valid; the problems were in scope, rules and process

### 9. How did you review the trajectory?

I read its `trajectory.md` and then checked it against the actual session
transcript. I only pulled out the observable events, meaning which files were
opened, which commands ran and which files were written, not its private
reasoning. The transcript showed six tool calls, matching its six claimed
steps. Two of them wrote scripts into `/tmp`. I recovered those scripts,
checked they only read workspace files, and preserved them with hashes.

- Trajectory claims → checked against the transcript
- Observable events only, no chain of thought
- That's how WS-1 was found and confirmed

### 10. What is the difference between context, workspace and instruction failures?

- **Context** is what the agent knows: the materials are missing, wrong or
  ambiguous.
- **Workspace** is the environment: what files, tools and writable places it
  has, and what defaults the harness gives it.
- **Instructions** are what it's told to do: scope, process, format.

The test I used: if the agent understood the task and had the right
information but did the wrong thing because of how it was set up, that's
workspace. If it followed its instructions faithfully and they were
incomplete, that's instructions.

- Context = knowledge, workspace = environment, instructions = task
- Ask: did it have the info? was it told? did the setup push it?

### 11. Give one example of each from your project.

- **Context:** the standard didn't define experience duration, so M1 could
  have been UNCLEAR, PARTIAL or SUPPORTED. That's anywhere from 52 to 64, and
  it changes the band.
- **Instructions:** the prompt never said when to use
  `additional_requirements`, so the agent left out the on-call duty even
  though it had read it.
- **Workspace:** the harness gives every session a scratchpad in `/tmp`, and
  the workspace had nowhere sanctioned for helper files, so the agent used the
  outside one.

- CTX-1 / INS-1 / WS-1
- WS-1 happened despite the rule being stated twice → environment cause

### 12. What did you change before Run 2?

Four things:
- a duration rule in the standard: calendar time, part-time counts, no
  full-time-equivalent conversion unless asked;
- a rule for lists in brackets: "e.g." means examples, "or" means
  alternatives, a bare list means all of them;
- a scope rule in the prompt: consider every explicit obligation or condition
  anywhere in the job description, without naming any;
- a `scratch/` folder inside the workspace, plus a rule that all helper files
  go there.

Plus the renderer fix, with tests.

- Duration rule, list rule, scope rule, `scratch/`
- No change to CV, JD, scoring or citation rules

### 13. Why did you change those things instead of rewriting everything?

Because I wanted to know what caused what. If I'd rewritten the prompt and the
standard wholesale, any difference in Run 2 could have come from anywhere.
Changing only the diagnosed levers means I can point at M1 and say that's the
duration rule, and point at A1 and say that's the scope rule. It's basically a
controlled experiment with one variable per problem.

- Targeted changes → attributable results
- Same CV, JD, scoring, citation rules in both runs

### 14. What changed in Run 2?

Four requirement-level differences:
- M1 went from UNCLEAR to SUPPORTED, using the calendar rule;
- P4 went from partial to supported, which nothing targeted;
- A1, the on-call rotation, was added as a mandatory requirement and marked
  unsupported;
- A2, remote in EMEA time zones, was added and supported.

P5 stayed the same, but now it cites the new rule. Process-wise, everything
stayed inside the workspace.

- M1, P4, A1, A2
- Other ten requirements: identical status and grade
- 61.8 Moderate, mandatory gap A1

### 15. Why did the score increase?

Because of M1 and P4, not the new requirements. If you just change M1 to
SUPPORTED, Run 1 goes from 52.1 to 63.8. Add P4 and it's 65.4. Then adding the
two new requirements brings it *down*: A1 alone takes it to 58.2, and A2
partly offsets that, giving 61.8. So the extra requirements cost 3.6 points
overall.

- 52.1 → 63.8 (M1) → 65.4 (P4) → 58.2 (+A1) → 61.8 (+A2)
- Increase = M1 + P4
- A1 + A2 together = −3.6

### 16. Did the higher score mean Run 2 was automatically better?

No, and that's kind of the point. The change that most improved the
assessment, assessing the on-call duty, lowered the score. And P4 went up
without any intervention, which isn't improvement, it's variance. I judged
Run 2 better because:
- it covers more of the job description;
- it uses defined rules instead of guesses;
- it stayed in the workspace;
- it surfaces a real gap;
- I can explain every difference.

- Score up ≠ better
- Criteria: coverage, clarity, compliance, gap surfaced, traceability

### 17. Why did Run 2 identify a mandatory gap when Run 1 did not?

Run 1 never assessed the on-call duty. It saw it, and even mentioned on-call
in its M6 reasoning, but treated anything unnumbered as out of scope. Run 2
was told to consider obligations anywhere in the job description. It added
on-call as A1, found nothing in the CV, and marked it unsupported. Because it
typed A1 as mandatory, using the standard's "if the type's unclear, treat it
as mandatory" rule, that triggers the mandatory-gap flag. The gap was always
there; Run 1 just didn't look at it.

- The gap existed in Run 1, unassessed
- The scope rule made it visible
- Gap flag ≠ band; Run 2 is "Moderate *with* a gap"

### 18. What happened with the workspace scratchpad?

In Run 1, the agent wrote two helper scripts, one to build the JSON and one to
check it, into the harness's `/tmp` scratchpad, outside the workspace. Nothing
in the output showed it; I found it in the trajectory and confirmed it in the
transcript. For Run 2 I added a `scratch/` folder inside the workspace, and it
put its one validator script there. The harness still created an empty
scratchpad for Run 2, but the agent never touched it. That's the harness, not
the agent.

- Run 1: `build.py` + `check.py` in `/tmp`
- Run 2: `scratch/validate.py`, retained and declared
- Empty harness dir ≠ violation
- Caveat: the Run 2 kickoff message also mentioned `scratch/`

### 19. What is the P4 variance and why does it matter?

P4 is "experience mentoring or onboarding". The evidence was the same both
times: "Helped onboard two interns". Run 1 read "helped" as partial and went
conservative. Run 2 read "or" as meaning onboarding alone is enough. Both
readings are reasonable, and nothing I changed targeted it. It matters because
it shows the agent's judgment can shift between runs with the same inputs. So
I can't claim every Run 2 difference came from my changes, and one run per
setup isn't enough to be statistically sure.

- Same evidence, same rules, different call
- Untargeted variance, not improvement (+1.6)
- Argument for repeated runs

### 20. What would you improve in a third run?

- **Calibrate the scope rule.** Say what kinds of statements count as
  conditions, like working hours or location versus benefits and team
  descriptions, without naming items. That's because A2 was debatable, and the
  boundary was a bit uneven.
- **Freeze the kickoff message** alongside the prompt, so it can't confound
  attribution.
- **Run each setup several times** to measure variance properly.

- Scope calibration, frozen kickoff, multiple runs
- Maybe: say explicitly that unlisted items count as "ambiguous type"

### 21. How did you prevent fabricated experience?

Layers:
- **Rules:** no inferring professional experience from related tech; Skills
  keywords alone are UNCLEAR; in-progress certs don't count; UNCLEAR earns
  zero credit, so guessing never pays.
- **Mechanics:** every claim needs a verbatim quote under an exact CV heading,
  and the code rejects anything that doesn't match character for character.
- **Review:** I checked the narrative sections by hand, because code can't
  judge free text.

- Rules + verbatim citations + manual review of the narrative
- UNCLEAR = 0 credit
- Code checks quotes; a human checks claims

### 22. What role did deterministic code play?

It's the referee, not the judge. The agent decides whether evidence meets a
requirement. The code:
- parses the files;
- validates the JSON;
- checks every quote and heading exactly;
- calculates the score with fixed weights and rounding;
- renders the report.

It never assigns a status and never does keyword matching. That separation
meant I could trust the score was arithmetic, and focus my review on judgment.
It's 126 unittest tests. Pytest wasn't available, so I never claimed it ran.

- The agent judges; the code validates and scores
- Exact quotes, exact headings, ROUND-HALF-UP
- 126 unittest tests; pytest not run

### 23. Why did you preserve hashes and manifests?

So I can prove what each agent saw and what it produced:
- every input file is hashed in a manifest, tied to a git commit;
- every output and scratch file is hashed when it's preserved;
- both sets are checked again at every milestone.

It's what lets me say Run 1 and Run 2 had the same CV and job description, and
that nobody edited the outputs afterwards. It also caught small things, like a
leftover "draft" note in the standard before Run 1.

- Inputs → manifest + commit; outputs → hashes
- Immutability checked at every milestone
- Pre-run leak check caught LEAK-1

### 24. What did you learn about managing agents?

- **Review the process, not just the deliverable.** A valid, honest output can
  still hide a process breach.
- **Agents do exactly what the scope says.** Run 1 wasn't lazy; it followed
  its instructions to the letter.
- **When an agent breaks a rule you stated clearly, look at the environment.**
  Repeating the rule louder may not be the fix.
- **Change one diagnosed thing at a time** if you want to learn anything from
  the next run.

- Process > deliverable
- Literal scope-following
- Environment shapes behaviour
- Targeted iteration

### 25. If you did the project again, what would you change first?

I'd freeze the kickoff message with the workspace from the start, and plan for
at least two or three runs per configuration. Those are the two things that
limit how strongly I can attribute the results. I'd also define the scope
boundary, meaning what counts as a role condition, in the first prompt, since
that's where most of the judgment variance ended up.

- Frozen kickoff
- Repeated runs
- Scope boundary defined up front

---

## Rapid-fire fact sheet

| | Run 1 | Run 2 |
|---|---|---|
| Total | **52.1** | **61.8** |
| Band | Weak | Moderate |
| Additional requirements | 0 | 2 (A1, A2) |
| Mandatory gap | none | **A1** (on-call) |
| Mandatory / preferred / quality | 35.00 / 10.00 / 7.08 | 43.75 / 11.67 / 6.43 |
| Helper files | `/tmp` (outside) | `scratch/validate.py` (inside) |

**Changed requirements:**
- M1: UNCLEAR/B → SUPPORTED/B (CTX-1)
- P4: PARTIAL/B → SUPPORTED/B (untargeted)
- A1: new, UNSUPPORTED/C
- A2: new, SUPPORTED/B

**Score path:** 52.1 → 63.8 (M1) → 65.4 (P4) → 58.2 (+A1) → **61.8** (+A2).
The increase comes from **M1 + P4**; A1 + A2 together = −3.6.

**Main diagnoses:**

| ID | Problem | Lever |
|---|---|---|
| INS-1 | Unnumbered duties excluded | Instructions |
| CTX-1 | Undefined duration | Context |
| CTX-2 | Ambiguous bracket lists | Context |
| WS-1 | Scripts outside the workspace | Workspace (+ instructions) |
| CODE-1 | False gap label | Framework, not a lever |

**Main interventions:**
- whole-job-description scope
- duration rule (calendar time)
- parenthetical semantics (e.g. / or / bare list)
- `scratch/`
- renderer fix

**Outcomes:**

| Lever | Outcome |
|---|---|
| CTX-1 | Successful |
| CTX-2 | Stabilised, no status change |
| INS-1 | Successful |
| WS-1 | Successful (kickoff caveat) |
| CODE-1 | Fixed |

**Residual issues:**
- A1 type is inferred
- A2 is debatable
- scope calibration
- procedural isolation
- n = 1 per configuration

**Final tests:** 126 passing `unittest` tests. pytest was not available and was
not run.

**Key commits:**
- `0beeff5`: framework
- `054bf89`: Run 1 freeze
- `238fb83`: diagnosis
- `bb46cce` / `c2e52f0`: Run 2 preparation and freeze
- `900f89a`: comparison
