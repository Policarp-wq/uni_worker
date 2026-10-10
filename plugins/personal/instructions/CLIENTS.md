# Client adaptation

## General instructions

`instructions/**/AGENTS.md` files are templates, not automatically loaded global
rules. Installing the plugin does not modify user instructions. The `setup` skill
merges selected templates with applicable instructions in the new environment.

For Codex, use a supported user-level or project AGENTS.md. For Claude, use an
AGENTS.md that the client reads; if CLAUDE.md is needed, add `@AGENTS.md` while
preserving existing rules. In user configuration, account for the actual imported
file location. Do not maintain two diverging texts.

Store populated profiles in user-selected memory or Git-ignored local configuration.
Git's `.git/info/exclude` can avoid changing the shared `.gitignore`. First verify
the file is untracked: ignoring does not exclude an already tracked file.

Instruction language is English. Preserve the configured conversation language and
Russian academic deliverables, linguistic examples and literal templates.

## Independent critic

Read `university-text-critic` and its caller contract before the first invocation.
The caller prepares context and executes `begin`; the critic receives returned paths,
ticket, attempt number and reviewer ID or a unique invocation label.

- Codex: use the client's separate-agent tool with a fresh context and no author
  history (`fork_turns: none` where supported). Pass the standalone assignment from
  the contract. Do not override the model without a separate basis.
- Claude: invoke the registered `personal:university-text-critic` agent through
  Agent/Task. If naming differs in the client version, find its definition in
  `agents/university-text-critic.md`. It defines a separate context and limited tools.
- Other clients: review requires genuinely independent context, access to input
  files and the ability to write the review and execute gate commands.

If independent agents are unavailable, report that the independent-review module
needs a suitable tool or another client. Do not run the critic branch in the author's
context or manually create `.critic-approve`.

The gate checks input hashes and attempt history; reviewer is a nonempty label,
not technical proof of independence. The calling client and instruction compliance
provide independence.

References: [Codex plugins](https://developers.openai.com/plugins/build/plugins),
[Claude subagents](https://code.claude.com/docs/en/sub-agents),
[Claude memory/imports](https://code.claude.com/docs/en/memory).
