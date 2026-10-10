# Academic skills: roles and workflow

These skills form a pipeline, not competing authors. Do not run all skills for every
request. Enter at the stage matching the actual task and advance only after the
current stage is complete. Academic drafts, reports and required review templates
remain in Russian despite English instructions.

## Local profile

At the first task requiring personal information, configure only necessary fields
in a local AGENTS.md or user-selected memory, following global profile rules. Portable
templates retain `{{STUDENT_FULL_NAME}}`, `{{STUDENT_GROUP}}`, `{{INSTITUTION_NAME}}`
and `{{TEACHER_FULL_NAME}}`; substitute values only into requested outputs. Standalone
skills without global instructions follow the same rules: read the local profile,
ask for missing required fields, and store values only locally with an export-exclusion
marker. Examples remain fictional.

## Main route

```text
university-work-planner
        ↓
university-work-executor
        ├─ artifacts only → stop
        └─ with report
              ↓
university-report-writer
              ↓
university-text-critic
              ↓
university-docx-report (only when DOCX is needed)
```

`university-writing-style` is a side route for discussing meanings and revising drafts.
`file-to-markdown` is an input converter, not an assignment-execution stage.

## Skill responsibilities

| Skill | When to use | Result | Exclusions |
| --- | --- | --- | --- |
| `university-work-planner` | First analysis and execution planning | One agreed plan with requirements, decisions, artifacts and DoD | No code, calculations or report writing |
| `university-work-executor` | Execute substantive work from a ready plan | Verified code, notebook, calculations, diagrams, data and evidence | No final report or approval |
| `university-writing-style` | Collaborate on meanings, wording or options | Agreed decisions and working draft | No final report conversion or review on every edit |
| `university-report-writer` | Completed substantive work needs final prose | One canonical report Markdown | No repeated experiments, self-approval or DOCX |
| `university-text-critic` | Independently review final Markdown | Review and, on success, hash-bound approval | No report rewriting or executor substitution |
| `university-docx-report` | Transfer approved Markdown into Word | One final DOCX with matching basename | No content changes or intermediate DOCX |
| `file-to-markdown` | Source exists only as PDF/DOC/DOCX/PPTX | Readable Markdown rendition | Not a writer or critic |

## Two independent execution settings

Establish both before planning:

| Question | Choices | Effect |
| --- | --- | --- |
| How to interact? | `автономно` (autonomous) / `итерационно` (iterative) | When to agree decisions |
| What to deliver now? | `с отчётом` (with report) / `только артефакты` (artifacts only) | Stop after execution or continue to documentation |

All four combinations are valid. `Автономно` does not mean «обязательно с отчётом»;
`итерационно` does not mean «только драфт».

## Quick routing

- «Выполни практическую без отчёта» → planner → executor → stop.
- «Выполни практическую и оформи» → planner → executor → writer → critic; DOCX only
  by request or submission requirement.
- «Отчёт теперь нужен по уже готовому коду/ноутбуку» → writer reads completed plan,
  artifacts and results → critic → DOCX if needed. Do not repeat verified execution.
- «Давай сначала обсудим смысл/структуру» → `university-writing-style`; after agreement,
  use writer or planner depending on substantive-work readiness.
- «Проверь готовый отчёт» → critic. Do not run the executor without a separate request
  to verify actual artifacts.
- «Собери DOCX» → validate current critic approval, then use the DOCX skill.

## File ownership

- Planner owns one `execution_plan.md` or continues the existing plan; no renamed copy.
- Executor owns substantive artifacts and records actual commands, results, checks
  and limits in the plan.
- `draft.md` appears only in `с отчётом` as factual writer input.
- Writer owns one canonical Markdown matching the future DOCX: `PR3.md` → `PR3.docx`.
- Critic owns `.critic-*` and the review. Approval applies only to the registered source.
- DOCX skill creates one final matching-basename file after all edits and valid approval.

Do not keep several competing canonical reports (`report.md`, `final.md`, `PR3.md`).
Older drafts may remain as materials with their status explicitly recorded in the plan.

## Stage handoff

Each stage passes source paths, accepted decisions, actual results, limitations and
open items. Verify previous-stage status using files and satisfied DoD, not «готово».

After the critic, the caller reports final status, every optional recommendation,
known remaining gaps and why each item was not applied. Successful approval must
not conceal deferred limitations.
