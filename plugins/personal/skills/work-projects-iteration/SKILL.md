---
name: work-projects-iteration
description: Continue projects in work_projects through small verifiable GitHub PRs, preserving architectural decisions and development state between sessions. Use for continuing a project, adding a feature, fixing a bug or preparing a PR in these projects, or explicit invocation. Do not apply to academic work or tasks outside work_projects without an explicit request.
---

# Ongoing development through small PRs

Example Russian requests: «продолжи проект», «добавь функцию», «исправь ошибку»,
«подготовь PR».

Maintain the existing project. Aim for changes the user understands, stable
subproject boundaries and a working result from every iteration.

## Core rules

- A new session is not a new project. Continue ongoing work and preserve decisions;
  do not restart an audit, design or plan without a reason.
- One iteration is one small PR with one explainable purpose. Do not stack dependent
  implementations on decisions awaiting user review.
- Logic, APIs, data, integrations, configuration, dependencies and architecture
  require user review. Do not merge without explicit approval of the current
  substantive changes.
- Pure GUI presentation does not require line-by-line user review. This exception
  excludes calculations, application state, permissions, storage, network requests
  and contracts, even in UI files. It does not authorize automatic GUI merges.
- Follow applicable AGENTS.md and existing conventions. Permission to work on a
  task does not authorize rewriting the project or publishing unrelated changes.

## Inputs and state

Identify the repository and task from the request, working directory and available
files. Discover the workspace from the current environment; do not assume a fixed
home path. Check WSL/Windows UNC equivalence only in a relevant environment. Find
the actual root through Git, not the folder name. If several repositories match
and the choice affects edits, clarify before editing.

Use existing README files, architecture notes, tasks and PRs. If persistent state
is absent, create one short `docs/development-state.md` in the repository. This is
a generated artifact, not a required input. Follow the project's documentation
language. Do not create a parallel tracker when an existing one suffices.

Keep only what continuation needs: current goal; branch, base and PR if any;
decisions and supporting links; completed and remaining work; latest checks and
known failures; pending review and the next small step. Update the existing record
rather than adding a daily action journal. Do not present local notes as current
GitHub state without verification.

## Work cycle

### 1. Restore context

Read applicable instructions, development state, Git status and relevant documents.
Check the branch, uncommitted changes and relevant recent commits; with GitHub
access, check PR status, CI and comments. Exclude others' and unrelated changes.

On first contact, map subproject responsibilities, dependency direction, entry
points, contracts and check commands. Investigate the selected scenario along its
actual execution path. Do not turn onboarding into a full repository audit. Save
stable findings in existing documentation or the state record.

On continuation, read the map and changes since the last recorded point, then only
the affected scenario and consumers. Investigate further if the map is missing,
stale or the task changes system boundaries. Verify doubtful notes against code.

Proceed when the current result, unfinished work, scope and baseline checks are
clear. Address an existing PR's requested fixes first.

### 2. Select the next iteration

Give a short plan: result, affected subprojects, substantive decision, verification
and completion criterion. For a large task, outline a sequence of small PRs but
implement only the next agreed step. Update the list and consult it after context
loss.

Aim for 100–300 changed lines of substantive code per PR. About 400 lines or several
independent decisions signal a need to split. This is a guide, not a reason to
compress code or produce broken intermediate states. Tests count toward the
substantive diff. Show generated files, lock files and mechanical changes separately
and explain their origin; they must not conceal large amounts of handwritten code.

If the goal exceeds that size, find a smaller complete result first. For a genuinely
indivisible change, explain its reason, expected size and review path before
implementation and agree on an exception with the user. Do not prepare a huge diff
and only then suggest splitting it.

Do not mix functionality with mass formatting, renaming or unrelated refactoring.
Separate GUI and user-reviewed logic into different PRs where possible; if separation
would break the result, explicitly mark the files and sections requiring review.

### 3. Preserve architectural boundaries

Before changing code, trace callers, all consumers of the changed contract and
subproject dependencies. Identify the existing owner of the behavior. Fix shared
failure causes where they originate.

Place domain logic where it can be tested without GUI; keep platform details at
existing platform boundaries. Extend existing mechanisms. Add an interface, layer
or service only for a concrete current need, such as isolating an external device
or multiple actually existing implementations.

When subproject boundaries, dependency direction, data format or a public contract
change, briefly record the decision, reason, consumers and compatible transition.
For a substantive choice, first present a recommendation and wait for the user's
decision before dependent implementation. Do not reopen an agreed decision without
new circumstances.

Proceed to code when the change fits existing boundaries or the required boundary
change has been agreed.

### 4. Implement and verify

Work on a separate branch from the repository's accepted base. Continue the current
branch if it already belongs to this task. Do not commit directly to the main branch.

Before edits, run available relevant checks or use a recent confirmed result for
the same revision and environment. Record baseline failures separately. After edits,
build and check affected behavior; for contract changes, check consumers and
subproject interactions. Follow mandatory repository checks.

Leave a reproducing check for a bug fix. For new nontrivial logic, add a minimal
observable-behavior check using existing project tools. For a purely visual change,
check startup and the relevant user scenario; do not delegate GUI code reading to
the user.

Review your own diff for unrelated changes, size, boundary violations and unexplained
dependencies. Do not declare the iteration complete while mandatory items remain
open. Record a blocker as a blocker and future iterations as remaining work.

### 5. Prepare the PR and obtain review

If publishing is requested or already authorized in the session, push the branch
and create or update the PR through an available GitHub tool. Otherwise prepare
local commits and exact PR text, then request only necessary publishing permission.
Do not create a second PR to address comments on the first.

The PR description must stand alone:

- Problem and observable behavior after the change.
- Key decision and affected boundaries, if changed.
- Review path: a few files in reading order and decisions to assess; mark pure GUI
  separately.
- Executed commands and check results; unverified parts and known limitations.
- Remaining work only where needed to understand the PR's scope.

Verify the published diff, target base and that CI status belongs to the current
commit. A ready PR and a merged PR are different states. Leave the PR as a draft
with the reason if checks are unavailable or a required check fails.

Stop dependent implementation at the review boundary. Address comments in the same
PR and rerun affected checks. Obtain renewed review after substantive changes
following approval. Merge only with merge authorization and satisfied repository
rules, after approval.

### 6. Preserve the continuation point

Before ending the session, update state: what was actually done and checked, the PR,
what is pending and where to resume. After merging, verify that it occurred and
base the next iteration on the updated base. Do not restart design.

Briefly report the result, PR or local artifact link, verification and next step.
If the user must respond, specify the actual decision or review needed.

## Failures and recovery

- **No GitHub access:** complete available local work, prepare the diff and PR text,
  save state and state the missing access. Do not claim a PR exists or CI passed.
- **Baseline build failure or a check needs another OS/hardware:** distinguish old
  and new failures, run available checks and identify the exact missing check.
  Do not bypass mandatory checks to merge or expand to repairing the whole system
  without agreement.
- **Conflict with others' work or stale state:** reconcile Git, the PR and recorded
  state while preserving others' edits. If intent cannot be recovered unambiguously,
  record the specific conflict and clarify before conflicting edits.
- **Scope grows:** stop expansion, preserve the working part and reconsider this
  PR's boundary. Do not present a partial result as completion of the whole task.

## Decision examples

- **«Продолжи поддержку устройства».** An open PR has contract comments: restore its
  state, fix comments and check consumers. Deliver an updated PR, not a new device
  support implementation.
- **«Добавь экспорт и кнопку».** Propose a small PR with export format, logic and
  verification for user review first, followed by GUI using that accepted contract.
  Do not put export calculations in the button handler.
