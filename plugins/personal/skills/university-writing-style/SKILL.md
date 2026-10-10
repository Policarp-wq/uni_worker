---
name: university-writing-style
description: Collaboratively develop meanings and decisions for Russian academic work, maintain a draft and incorporate user edits. Use when discussing practical reports or coursework; turn an agreed draft into final prose through university-report-writer.
---

# Collaborative academic drafting

Shared roles and transitions: [UNIVERSITY_WORKFLOW.md](../UNIVERSITY_WORKFLOW.md).
Write academic drafts and final deliverables in Russian; these English instructions
do not change the Russian writing rules.

When the user proposes an idea, assess its meaning, boundaries, assumptions and
fit with the assignment. Explain a concrete objection or recommendation before
recording a decision. Already agreed decisions do not need confirmation again:
preserve them and their reasons in the draft.

A draft accumulates meaning and may be long, repetitive and contain alternatives
or working notes. Do not demand final style, cut useful explanations for appearance
or invoke the critic on every discussion iteration.

## Materials and decisions

- Use the user's current assignment as the basis. Identify disagreements in scope
  or requirements between materials; do not silently combine them.
- Distinguish agreed decisions, proposals and open questions. Preserve decisions
  and user edits; do not replace them without discussion.
- Do not invent numbers, completed tests, features or future tasks to fill gaps.
  Label accepted educational values as design assumptions and preserve their basis.
- Before writing diagram code, clarify purpose, boundaries, elements and connections.
  Label connections with a concrete message or action rather than the generic «данные».

## Transition to final work

When the user requests final formatting, or meanings are agreed within a final-report
request, use [university-report-writer](../university-report-writer/SKILL.md). It runs
in the current agent, produces final Markdown and hands it to a separate critic.

For final prose and general style changes, read the
[shared core](../university-text-critic/references/report-core.md). Do not keep a
second copy of its rules. Review and DOCX approval are defined by
[university-text-critic](../university-text-critic/SKILL.md).

## User edits

Distinguish a correction to one work from a general preference. Add an explicitly
general style/structure rule to the shared core so both writer and critic apply it.
If scope is unclear, apply it to the current draft and clarify only generalization.
Keep changes to the discussion process in this skill.
