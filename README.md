# Agent Kit

Portable personal instructions and ten original skills for development and academic work. One repository serves as a marketplace for Codex and Claude Code. The `setup` skill connects instructions to a new environment; populated personal profiles stay local and are excluded from export.

Instructions and documentation are written in English. Academic deliverables remain in Russian: preserve the Russian wording, examples, terminology and typography specified by the skills. English instructions do not authorize translating Russian output templates or changing the writing rules.

## Install from GitHub

Replace `OWNER/REPO` with the repository. Public repositories are accessible to everyone; private repositories require access and configured GitHub authentication on the recipient's machine.

Codex CLI:

```sh
codex plugin marketplace add OWNER/REPO --ref main
codex plugin add personal@agent-kit
```

In a new session, ask: "Read and run the setup skill from the personal plugin." If the interface offers onboarding, start there.

Claude Code:

```text
/plugin marketplace add OWNER/REPO
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

Exact file list: [FILES.md](FILES.md). Export boundaries: [docs/EXPORT.md](docs/EXPORT.md). Dependencies and limitations: [docs/DEPENDENCIES.md](docs/DEPENDENCIES.md).

## Local checks

```sh
python3 scripts/check.py
PYTHONDONTWRITEBYTECODE=1 python3 plugins/personal/skills/university-text-critic/scripts/test_critic_gate.py -v
```

The critic runs on Linux/WSL and macOS with Python 3.10+. On native Windows, it stops because `fcntl` is unavailable: replace the file locking implementation while preserving protection against concurrent writes before using it. This restriction applies to the critic and its dependent DOCX approval gate, not the entire plugin.

## Publish

Create an empty GitHub repository and give its URL to the agent. Publish only this folder's contents. Academic submissions, personal memory, account settings and third-party plugins are excluded.

Install third-party plugins from current upstream sources without pinning their versions. Version `1.0.2` belongs only to this package and enables client cache updates.
