---
name: setup
description: Set up this portable personal plugin in a new Codex or Claude workspace, merge instruction templates, configure scoped profiles and check required tools without exporting personal data.
---

# Portable package setup

Use on first connection, explicit setup requests or updates to transferred
instructions. Installing a plugin and configuring its profiles are separate actions.

## Initial reading

Read [client adaptation](../../instructions/CLIENTS.md),
[global instructions](../../instructions/global/AGENTS.md) and the
[academic workflow](../UNIVERSITY_WORKFLOW.md). Identify the OS, client, working
directory, Git root and active user/project instructions. Do not assume the original
home path or author's folder. Instruction language is English; preserve Russian
academic output and the existing conversation-language rules.

## Connect instructions

A setup request authorizes merging portable rules with local instructions. Preserve
all existing rules and user edits; do not overwrite a whole file. Resolve substantive
conflicts with the user while continuing independent setup. Repeated runs must not
duplicate already added blocks.

1. Merge communication style and personal profile rules into the applicable user
   AGENTS.md or project rules according to the selected scope. For Claude, configure
   reading the same text according to CLIENTS.md.
2. Determine which folders are needed: academic work and/or development projects.
   Do not copy all instructions into the root. Do not ask again when folders and
   scope are already specified.
3. General instructions are in `instructions/workspace/university/AGENTS.md` and
   `instructions/workspace/work_projects/AGENTS.md`. Their plugin layout illustrates
   scope, not mandatory paths on a new machine. Read subject/project requirements
   from the assignment and existing local instructions; no such profiles are bundled.

Do not create title pages or populate personal profiles during setup when the task
does not require them. At the first task that does, read the configured profile or
approved memory and ask only for missing required fields. Use `{{STUDENT_FULL_NAME}}`,
`{{STUDENT_GROUP}}`, `{{INSTITUTION_NAME}}` and `{{TEACHER_FULL_NAME}}`. Do not treat
fictional example values as user values.

Store supplied values in the user's global AGENTS.md, a Git-ignored local AGENTS.md
under `Local personal profile — exclude from export`, or user-selected memory.
Verify the file is untracked first; choose another local configuration if tracked.
Do not write profiles into the plugin or tracked instructions. Substitute values
only into requested outputs.

## Capability checks

- Critic: Python 3.10+ and a real separate agent. On native Windows, report that
  `fcntl` is unavailable and file locking must be replaced; critic review and its
  dependent DOCX gate remain unavailable. Do not bypass this restriction.
- Conversion: check `markitdown` in the active environment or local `.venv`.
  Install dependencies for the actual task, not every possible package in advance.
- DOCX: supplied Word template, `python-docx`, generator calling `require_approval`.
- Development projects: SDKs and platform checks come from the project; do not
  install subject-specific tools as global plugin dependencies.
- External plugins: connect current upstream distributions according to repository
  documentation. Skill text does not restore accounts or MCP services.

Finally list only actually configured files, active profiles and specific unavailable
capabilities. Do not call a profile ready with missing required resources. For
updates, repeat the safe merge; personal profiles remain local.
