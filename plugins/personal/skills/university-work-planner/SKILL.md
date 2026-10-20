---
name: university-work-planner
description: Plan a university practical, lab or coursework assignment before creating code, notebooks, calculations, diagrams or reports. Identify requirements, decisions, artifacts, checks and DoD; do not execute the assignment or write its report.
---

# Academic work planner

Shared roles and transitions: [UNIVERSITY_WORKFLOW.md](../UNIVERSITY_WORKFLOW.md).

Think before execution. Turn the assignment and source materials into a verifiable
plan that the next stage can execute without reinterpreting requirements. Do not
create substantive artifacts, calculate instead of the executor or write report
prose. Academic deliverables remain in Russian.

## Two independent settings

Before analysis, establish:

1. **Interaction mode:** `автономно` (autonomous) or `итерационно` (iterative).
2. **Deliverable mode:** `с отчётом` (with report) or `только артефакты` (artifacts only).

The first controls agreement steps; the second controls deliverables. All four
combinations are valid. If a setting is absent and cannot be recovered unambiguously
from context, request it together with the work's location in one message.

`Только артефакты` means required code, notebooks, calculations, experiments,
diagrams or other results without a report draft, critic or DOCX. Still plan to
preserve actual results and limitations so a later report needs neither invention
nor repeated execution.

## Analysis and plan

1. Identify one working folder and read the full assignment, criteria, appendices,
   related previous works and existing solution. Use `file-to-markdown` for protected
   formats first.
2. State the goal and substantive result. Distinguish source requirements, author
   decisions and requirements only for report formatting.
3. Map **ID → exact quotation and source → task → artifact/evidence → DoD → check → status**.
4. Plan the smallest execution method, dependencies, substantive decisions, risks
   and blocking uncertainties. Add no technology or files unrelated to requirements.
   Where the assignment asks to choose or justify an approach, plan a brief comparison
   of genuine alternatives for each such decision (for example monolith versus
   microservices, or several database technologies), not one option per table.
5. For `с отчётом`, schedule documentation after substantive artifacts are ready and
   verified. For `только артефакты`, mark report requirements deferred, not completed
   or cancelled.
6. For every figure, record the required notation, tool and level of detail from the
   assignment text and its sample (for example numeric multiplicities versus crow's
   foot, ArchiMate business objects, UML classes). Record that images contain only
   the diagram: legends, notes and verification remarks go to text or nowhere.
   Plan a check that names, counts and multiplicities in each figure match the tables.
   For processes and state machines, list every failure case (no answer, problem not
   fixed, result still unknown at the deadline) with its explicit outcome. Do not
   remove a case with an assumption; an outcome missing in the plan becomes a hidden
   dead end in the model.
7. For `с отчётом`, draw a report boundary in the plan: list what the assignment asks
   the report to show, and what stays only in the plan (how artifacts were produced,
   scripts and tools used, rejected options, questions of earlier works the assignment
   does not reopen). The writer uses this list to keep the veil out of the report.
8. Save one plan in the existing planning file; otherwise use `execution_plan.md` in
   the work folder. Do not create parallel copies. Record both modes, sources, user
   decisions, questions, tasks, DoD, expected artifacts, commands/check methods and
   space for actual results.

## Agreement

- In autonomous mode, present the goal, full plan, decisions, assumptions and
  questions together. Execution starts only after explicit plan approval.
- In iterative mode, present the full plan and DoD; the executor then agrees each
  not-yet-accepted substantive decision before its iteration.
- Changing the topic, dataset, research object or mandatory method requires a user
  decision in either mode.

## Handoff to the executor

Pass the working folder, plan path, both settings, requirements, agreed decisions
and open blockers to `university-work-executor`. A plan is ready only when it makes
clear what to create, how to check it and where to save evidence. Planned is not done.
