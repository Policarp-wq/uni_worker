# Caller contract

## Before launch

One folder contains one work and one canonical Markdown source. Put independent
works in separate folders before their first launch. Preserve state/history during
transfer; mismatched recorded paths require a human decision.

Write UTF-8 `.critic-context.json` beside the work. JSON paths resolve relative to
that file. All fields are required except `assignment_files` and `decisions`. This
is a fictional Russian-language assignment example, not a mandatory subject:

```json
{
  "subject": "Проектирование информационных систем",
  "topic": "Практическая работа 2. Модель платёжного шлюза",
  "requirements": ["Описать события, участников и границы ответственности"],
  "previous_exists": true,
  "previous": ["../PR1/PR1.md"],
  "assignment_files": ["задание.md"],
  "decisions": ["Провайдер проводит платёж; шлюз передаёт запрос и хранит статус"]
}
```

With no earlier works, set `previous_exists: false` and `previous: []`. Missing files
are not evidence that earlier works never existed. For `true`, supply readable,
nonempty local MD/TXT/RST, not PDF, DOCX, URLs or nonexistent names. The caller owns
list completeness. Derive requirements from the assignment/user, not author guesses.
Include readable assignment materials in `assignment_files` when available. Put
user decisions and allowed deviations in `decisions`.

Do not spend an attempt on incomplete context: `begin` validates inputs first. The
separate agent reads local files through the selected client; do not send them to
additional services without the user's request.

## Commands

`SKILL_DIR` is the absolute skill-folder path; `REPORT` is the report's Markdown path.
Substitute actual paths and quote them. Run all commands with `python3`.

```sh
python3 "$SKILL_DIR/scripts/critic_gate.py" begin --source "$REPORT" --context /absolute/work/.critic-context.json
python3 "$SKILL_DIR/scripts/critic_gate.py" check --source "$REPORT"
```

Before the first `begin` of a report, run the compression round from the core:

```sh
python3 "$SKILL_DIR/scripts/prose_gate.py" baseline --source "$REPORT"
python3 "$SKILL_DIR/scripts/prose_gate.py" lint --source "$REPORT"
python3 "$SKILL_DIR/scripts/prose_gate.py" compress --source "$REPORT"
```

Run `baseline` on the uncompressed final version, cut, then `compress`. `compress`
exits nonzero with `COMPRESSION_REQUIRED` and the measured numbers until prose shrinks
by at least 10% and no hard lint findings remain; on success it writes
`.compress-state.json` and `.compress-approve`. `begin` checks them and that prose
has not grown by more than 5% since. Only an explicit human decision may be passed as
`compress --waive 'decision'`.

`begin` returns JSON containing `cycle`, `attempt`, `ticket`, `report`, `source` and
`context`. Save and pass them to the critic. `begin`, `finish`, `cancel` and `resolve`
modify only this work's state files; `check` only validates permission.

Example standalone critic assignment (instructions in English, review in Russian):

```text
You are an independent academic text critic with no conversation history.
Read SKILL.md at the supplied absolute path and execute only the critic branch.
Subject: …; topic: …; previous works: yes/no, paths: …
JSON context: …; current Markdown: …; requirements: …
Cycle: …; attempt: …/3; ticket: …; your agent ID/invocation label: …
critic_gate.py path: …; write the Russian review to: …
Previous reviews and author responses: … / first invocation.
Check style, concision, veil, assignment fulfillment, continuity and every figure.
Do not edit sources or generate DOCX. Complete through finish.
Return a brief verdict and file paths. Preserve the literal Russian review template.
```

If the client exposes no agent ID, assign a unique label for the real independent
invocation, such as `critic-<ticket>`. It does not authorize self-review. The script
accepts a nonempty label but does not verify that an agent exists.

If ID becomes known only after launch, send it to that same agent before `finish`.
This is part of one invocation, not another review. Do not let the child execute
this skill's caller branch recursively.

The critic writes the review to the assigned path and then runs:

```sh
python3 "$SKILL_DIR/scripts/critic_gate.py" finish --source "$REPORT" --ticket TICKET --reviewer AGENT_ID --verdict approve
```

Other `--verdict` values: `revise`, `context_error`. Technical cancellation:
`cancel --source ... --ticket ... --reason 'specific reason'`. After `3/3`, the author
may resolve the concrete dispute and open a cycle with
`resolve --source "$REPORT" --decision 'brief author decision'`. This preserves old
attempts and the decision; the next launch is `1/3`, with no approval granted.
Run only after an explicit author decision; never edit the ledger manually.

A nonzero exit code means an incomplete transition. `check` verifies source, context,
previous works, assignment materials and the latest attempt of the current cycle.
SKILL.md defines exact limits/error handling. An author decision does not replace
`APPROVE`; a new cycle requires new approval.

## Executable DOCX approval gate

Connect `scripts/critic_gate.py` to every generator; call `require_approval(source)`
before document construction and immediately before saving. On failure, create no
academic DOCX, even temporarily. Add both calls to new generators before their first
run. Do not bypass through Pandoc, LibreOffice, MCP or another script.

```python
import runpy
gate = runpy.run_path(str(skill_dir / "scripts" / "critic_gate.py"))
gate["require_approval"](source)
# Construct the document from that exact source.
gate["require_approval"](source)
document.save(output)
```

The generator must read the approved Markdown, not its own alternative text. Keep
inputs unchanged during construction. Hash checks do not automatically compare
DOCX content with Markdown; the generation skill verifies output integrity.

AGENTS.md and connected writing/generation skills trigger review. This is not a
background file watcher: the agent starts review when prose is ready, not on every
draft save. The mechanism does not intercept arbitrary DOCX writes across the OS.

## After three attempts

Use this Russian human-handoff template when stopped by the SKILL.md limit. An
explicit author decision permits `resolve`, not a manual reset:

```text
Работа: …; в текущем цикле использовано 3/3 попытки; DOCX заблокирован.
Спорный фрагмент: «…» (раздел/строки).
Критик требует: …; основание: пункт задания или критерий стиля.
Автор возражает: …; основание: требование, сохранение смысла или решение пользователя.
Что уже изменяли: …; что осталось нерешённым: …
Нужно решение человека: выбрать формулировку A/B, уточнить требование или явно
изменить правило допуска. Рекомендация автора: …, потому что …
Рецензии: ссылки на все попытки и циклы.
```

Without a text dispute, identify the technical stopping reason and consumed attempts.
Do not present a technical failure as a disagreement.

`resolve` also opens a new cycle when the third attempt was `approve` but the work changed afterwards, so the approval is stale and `check` fails: the human decides that the further edits need review. It never works while the approval is still valid.

## Final human handoff

After `APPROVE`, stopping or exhaustion, the caller briefly reports:

- Actual work/approval status.
- All optional recommendations from the latest review.
- Other known gaps, limits and risks outside the result.
- The specific reason for rejecting/deferring each unapplied item.

Do not delegate this responsibility to the critic or present optional suggestions
as approval blockers. Explicitly state when no recommendations/known gaps remain.
