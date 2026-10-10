# Package validation

Date: 2026-10-10.

- Codex CLI 0.162.0: the local marketplace was registered, and the plugin was actually installed and enabled in an isolated temporary user profile. The user's working configuration was not changed.
- GitHub distribution: `codex plugin marketplace add Policarp-wq/uni_worker --ref main` downloaded the private repository using configured Git credentials. Its published 1.0.2 plugin was installed with all eleven skills in a fresh isolated profile before the installation documentation update.
- All eleven SKILL.md files passed the standard Skill Creator validator.
- All fourteen gate tests passed on Linux: hashes, attempt history, concurrent starts, rejection of corrupt state and native Windows fail-fast behavior.
- `scripts/check.py` checked manifests, version consistency, the file inventory, relative links, absence of symlinks and known classes of personal data/secrets. Embedded assertions verify detection of fictional leaks and rejection of paths leaving the package.
- English instructions retain Russian linguistic examples, required literal wording and output templates. Existing Russian quoted examples were compared against the previous revision; the workflow and executable gate semantics were preserved.

The Windows branch was tested in a separate process with a substituted `sys.platform`; real Windows and macOS were not run. Claude CLI is absent: its manifests and subagent definition follow official documentation, but installation in Claude was not tested. Model behavior for every skill and third-party upstream plugins was not retested.

Instructions for specific subjects and projects are excluded. Supply the Word template locally for the particular DOCX task. Personal data scanning remains heuristic; review newly added files before publication.
