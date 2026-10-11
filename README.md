# Agent Kit

Portable personal instructions and ten original skills for development and academic work. One repository serves as a marketplace for Codex and Claude Code. The `setup` skill connects instructions to a new environment; populated personal profiles stay local and are excluded from export.

Instructions and documentation are written in English. Academic deliverables remain in Russian: preserve the Russian wording, examples, terminology and typography specified by the skills. English instructions do not authorize translating Russian output templates or changing the writing rules.

## Install from GitHub

Install from [Policarp-wq/uni_worker](https://github.com/Policarp-wq/uni_worker). You need an up-to-date Codex CLI or Claude Code, Git and your own access to the chosen agent.

If the repository is private, its owner must grant your GitHub account access and you must accept the invitation. Authenticate Git on the machine where you will install the plugin. With GitHub CLI installed, run these commands once:

```sh
gh auth login --hostname github.com --git-protocol https
gh auth setup-git --hostname github.com
```

These commands use your own GitHub account. A repository owner does not need to share credentials. If Git already has working access to the repository, skip this authentication step.

Codex CLI:

```sh
codex plugin marketplace add Policarp-wq/uni_worker --ref main
codex plugin add personal@agent-kit
```

In a new session, ask: "Read and run the setup skill from the personal plugin." If the interface offers onboarding, start there.

Claude Code:

```text
/plugin marketplace add https://github.com/Policarp-wq/uni_worker.git
/plugin install personal@agent-kit
/personal:setup
```

To update Codex, run `codex plugin marketplace upgrade agent-kit`, then `codex plugin add personal@agent-kit`, and check the installed version with `codex plugin list`. In Claude, open `/plugin`, go to Marketplaces and enable updates for this marketplace or update it manually. The agent merges updates to previously copied local instructions separately, preserving existing rules and the local profile.

Formats and commands: [Codex plugins](https://developers.openai.com/plugins/build/plugins), [Claude marketplaces](https://code.claude.com/docs/en/plugin-marketplaces), [Claude installation and updates](https://code.claude.com/docs/en/discover-plugins).

## Included

- Ten original skills, a shared academic workflow, the Python critic approval gate and its tests.
- Communication style and local personal profile rules.
- General instructions for academic and development folders, without subject-specific or project-specific rules.
- Setup for both clients and a separate reviewer agent for Claude.
- A Claude Code `PreToolUse` hook (`plugins/personal/hooks`) that blocks direct `Bash` and `Read` access to PDF/DOC/DOCX/PPTX and audio files, pointing to an existing Markdown rendition or `file-to-markdown`. Codex needs its own copy of the guard in its user hooks configuration.

Exact file list: [FILES.md](FILES.md). Export boundaries: [docs/EXPORT.md](docs/EXPORT.md). Dependencies and limitations: [docs/DEPENDENCIES.md](docs/DEPENDENCIES.md).

## Local checks

```sh
python3 scripts/check.py
PYTHONDONTWRITEBYTECODE=1 python3 plugins/personal/skills/university-text-critic/scripts/test_critic_gate.py -v
PYTHONDONTWRITEBYTECODE=1 python3 plugins/personal/hooks/test_document_read_guard.py
```

The critic runs on Linux/WSL and macOS with Python 3.10+. On native Windows, it stops because `fcntl` is unavailable: replace the file locking implementation while preserving protection against concurrent writes before using it. This restriction applies to the critic and its dependent DOCX approval gate, not the entire plugin.

## Maintain this repository

Publish updates to `Policarp-wq/uni_worker` from this folder only. Academic submissions, personal memory, account settings and third-party plugins are excluded. To share the plugin while the repository is private, grant the recipient repository access; sending its URL alone does not grant access.

Install third-party plugins from current upstream sources without pinning their versions. Version `1.0.3` belongs only to this package and enables client cache updates.
