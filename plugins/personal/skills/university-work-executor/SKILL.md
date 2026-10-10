---
name: university-work-executor
description: Execute a university practical, lab or coursework assignment from an existing plan; create and verify code, notebooks, calculations, diagrams and other artifacts. Supports independent interaction modes (autonomous/iterative) and deliverable modes (with report/artifacts only).
---

# Academic work executor

Shared roles and transitions: [UNIVERSITY_WORKFLOW.md](../UNIVERSITY_WORKFLOW.md).

Meaningfully execute and verify the substantive work planned by
`university-work-planner`. Deliver either required artifacts and verification evidence,
or the same artifacts followed by a writer handoff, according to deliverable mode.
DoD verifies results; it does not replace the work's goal. Academic drafts and
reports remain in Russian under the shared writing rules.

## Required boundaries

- Before reading materials, establish both independent settings if absent:
  **автономно/итерационно** (autonomous/iterative) and **с отчётом/только артефакты**
  (with report/artifacts only). Do not choose for the user. Settings persist until
  explicitly changed.
- Without a path, work name or explicit assignment context, stop and request its
  location. Do not search blindly. Request all missing settings and location together.
- If requirements are missing, inaccessible, contradictory or cannot establish the
  mandatory outcome, stop and ask. Do not substitute a typical assignment. A missing
  detail such as a filename does not by itself mean requirements are absent.
- Do not invent data, sources, measurements, run results or quotations. Formal DoD
  closure is not proof of substantive quality.
- Do not silently violate skills, repository rules or the agreed plan. If compliance
  is impossible or an existing violation is discovered, stop, name the rule and source,
  explain the conflict and request a decision. Explicit user instructions override
  skills; approving a plan does not authorize unstated deviations.
- Changing the dataset, topic, research object, mandatory method or another agreed
  foundation requires stopping for an explicit decision, even in autonomous mode.
- Stop after the third failed full DoD verification cycle. Do not continue repairs
  or reset history without a user decision.
- Do not create the final report or DOCX yourself. In `с отчётом`, prepare factual
  input for `university-report-writer` after substantive completion. In
  `только артефакты`, do not invoke the writer, critic or DOCX generation.

Stopping means preserving actual state, listing blockers and unmet DoD, asking a
specific question and waiting. Do not continue blocked execution as "independent
improvements." State may be written when the work folder is known and writing is
authorized; otherwise report it in chat.

## 1. Identify the work folder

1. Check both settings and location in the request and agreed context. Do not read
   the work or search its files before settings are selected.
2. Use a supplied path. For a work name, search matching file/folder names only in
   visible workspace roots, without reading unrelated submissions. Use one
   unambiguous match without asking to confirm the path; ask the user to choose
   among several; with no match, stop and request a path. Do not search the home
   directory or entire disk.
3. An assignment supplied in chat is a requirements source; use a working folder
   explicitly established by context. Request a path before creating files if unknown.
4. Select one folder as `work_dir`. Example: `university/<course>/PR1/`, containing
   the assignment, plan, code, data and results of one practical. It is an example,
   not a skill resource: do not open it while reading this skill. Map a user WSL
   path to a Linux path only in the appropriate environment.
5. Read applicable AGENTS.md along the directory chain and rules for affected files.
   Create work files, conversions, temporary results and artifacts inside `work_dir`.
   Shared rules and installed skills may be read outside it. Read external sources
   only when explicitly related to the assignment; keep reproducibility materials
   locally with provenance. Do not edit neighboring submissions or shared skills.
6. Check assignment/tool access, write permissions and prior results. Preserve others'
   edits and original data. If execution needs writing outside the folder, a missing
   required resource or unavailable tool, identify the blocker before dependent steps.

Proceed to planning only with both settings, one working folder and readable
requirements sources.

## 2. Obtain and verify the plan

1. Use `university-work-planner` to study the assignment and create one plan. Reread
   and continue a suitable already agreed plan rather than analyzing again.
2. Before execution, verify both settings, sourced requirements, tasks, DoD,
   artifacts, checks, user decisions and open blockers. Return an incomplete plan
   to the planner; do not silently fill it in during implementation.
3. Report-only requirements are not substantive-execution DoD. They stay deferred in
   `только артефакты`; the writer handles them after artifact readiness in `с отчётом`.

Distinguish product technology from verification tools. Application language need
not match calculations, generators or one-off checks. Python is acceptable for exact
arithmetic and analysis when helpful; prefer standard-library tools or manual
substitution over another project when sufficient. Before creating an auxiliary
file that stays in the folder or deliverable, add its purpose, language, invocation
and DoD relation to the saved plan. If it is not assigned and changes the artifact
set, stop and clarify with the user before creating it.

Reread the saved plan before each phase and after context loss. Update statuses,
actual results, commands and limits after iterations. Do not reset agreements or
counters when changing sessions or executors.

## 3. Execute in the selected mode

### Autonomous — `автономно`

1. After full analysis, present the goal, plan, DoD, proposed decisions, all known
   questions and assumptions in one message. Request answers and explicit approval
   of the final plan together. Initial setting/location questions do not replace this.
2. Do not execute before approval. Clarify an answer that changes the foundation or
   leaves a blocker; silence, partial answers and elapsed time do not approve a plan.
3. Once approved, follow the plan to satisfied DoD without confirming every step.
   Fix errors within scope and share progress. Do not ask again about agreed decisions.
4. Bundle all foreseeable questions into the initial agreement. A new critical fact,
   rule conflict or foundation change still requires stopping for a separate decision.

### Iterative — `итерационно`

1. Explain the whole assignment after analysis and present the complete iteration
   plan and DoD. Then agree substantive decisions sequentially.
2. At the start of each iteration, show the **exact assignment quotation and source**
   establishing its need, your briefly justified solution, substantive questions,
   expected result and specific DoD relation. If it supports a broader requirement,
   quote that requirement and explain the link; do not invent an assignment item.
3. Wait for the decision, incorporate edits, implement, verify and update the plan
   with evidence. Without substantive questions, one agreement on the proposal is
   sufficient; do not invent clarifications.
4. Do not reconfirm explicitly agreed decisions: show their basis and execute them.
   Do not execute the next unagreed iteration in advance.

## 4. Preserve substance and minimality

- Use `ponytail:ponytail` at full level for code and technical choices. Understand
  the whole task, check existing solutions, then prefer standard tools and minimal
  necessary code. Minimality does not remove requirements, correctness, verifiability
  or essential decision reasons.
- Do not build workarounds to tick boxes. If the approach does not answer the work's
  question, fix the cause, not result presentation. Do not lower DoD to fit existing
  code or call mandatory requirements inapplicable without a basis.
- Counterexample: the user specifies C# applications and PostgreSQL, but the executor
  adds a C# `calculations` project only for arithmetic. It is an extra artifact and
  misreads the requirement. Record the calculation method in the plan, clarify before
  file creation and use Python or preserved formulas/results if a script is needed.
- Example: demographic time analysis needs actual observations over time. A sparse
  dataset does not justify inventing a time series or relabeling an already completed
  population-density plot. Another measure is allowed only with data, assignment fit
  and agreed freedom of choice; otherwise agree the change. If another dataset is
  needed, explain why, the proposal and its effect, then stop for a decision.
- Preserve data provenance, measure definitions, units, transformations and reasons
  for conclusions. Check compatibility across parts. Leave a minimal runnable check
  for nontrivial code; «должно работать» does not replace execution.

## 5. Verify DoD and correct mismatches

1. Check local results as work progresses. Once the plan is implemented, run a full
   cycle: compare artifacts and saved evidence against all executor-stage requirements,
   run required checks and assess the substantive answer to the goal.
2. Record actual status and evidence for every DoD: file, run result, calculation or
   observed output. Unverified is not completed. Check for open plan tasks and links
   to missing files separately.
3. If a full cycle finds any unmet DoD, increment the shared failed-cycle counter once,
   regardless of finding count. Local checking of an unfinished iteration is not a
   full cycle; do not exploit that distinction to bypass the limit after implementation.
4. Immediately report unmet DoD, mismatch evidence and causes. Create local repair
   tasks with expected verification without changing success criteria. After failure
   one or two, fix within agreed scope and rerun the full cycle; agree new substantive
   decisions in iterative mode.
5. Failure three means stop before further repairs. Report unmet items, attempts,
   likely cause and required decision. Preserve all attempts. Resume only after an
   explicit user decision, keeping history and agreeing the further attempt limit.
6. Declare only the executor stage complete after its DoD and plan are closed. List
   later-stage requirements separately; do not declare the whole assignment ready
   for submission. With a blocker, end with an honest incomplete status, not «готово».

This counter covers executor DoD failures. The critic has its own history and limit;
do not mix counters or reset either when moving between stages.

## 6. Finish according to deliverable mode

### Artifacts only — `только артефакты`

Stop after substantive DoD completion. Leave required code, notebook, diagrams,
calculations, data and other files; preserve run commands, actual results, conclusions
and limits in the plan. Do not create `draft.md` merely for a future report, or launch
the writer, critic or DOCX. Explicitly report documentation as deferred. A later
report request uses existing artifacts and the plan without repeating proven steps.

### With report — `с отчётом`

After substantive DoD passes, create/update `draft.md` as a factual writer handoff:
goal, executed methods, decisions with reasons, results, interpretation, limitations
and relative artifact links. Keep process notes, coverage mapping, repair history
and failure counters only in the plan. Pass the assignment, draft, plan and artifacts
to `university-report-writer`; it creates final Markdown and invokes the critic.
Generate DOCX through `university-docx-report` only after approval.

Use related skills by names in the current catalog; read them at the relevant stage.
Do not pin plugin versions or personal absolute paths. If a currently mandatory
skill is missing, save results, name it and stop the handoff rather than imitate it.
Verify every handoff by its artifact and actual status, not invocation alone.

Report links to the plan/main artifacts, actual DoD status and selected deliverable
mode. For `с отчётом`, also report draft, writer, critic and DOCX status; for
`только артефакты`, explicitly list deferred documentation stages.

## Input and first-action examples

- «Давай сделаем PR1» without settings: ask «Автономно или итерационно? С отчётом или только артефакты?» before searching or reading.
- «Сделай автономно лабораторную без отчёта» without a path, name or assignment
  context: request location only; do not ask for known settings again.
- «Итерационно выполни практическую в указанной папке»: read the full assignment,
  present goal/plan and the first iteration with quotation, decision and DoD;
  wait before implementation. Establish deliverable mode first if still unknown.
- «Автономно выполни работу по этому заданию, отчёт потом»: agree the plan together,
  create/check substantive artifacts, preserve evidence and stop without the writer.
