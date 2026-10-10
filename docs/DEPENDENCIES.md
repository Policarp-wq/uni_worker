# Dependencies

The package contains no third-party snapshots or lock files. Install current supported versions from official sources; check that the required tool exists in the actual environment before using it.

| Capability | Requirements |
| --- | --- |
| Independent critic | Python 3.10+, Linux/WSL or macOS; a separate agent with its own context |
| PDF/Office input | `markitdown` with dependencies for the input format; reuse neighboring Markdown first |
| DOCX generation example | `python-docx`, a user-supplied Word template and valid critic approval |

Native Windows: the critic cannot use `fcntl`. Stop until `fcntl.flock()` is replaced with compatible file locking that preserves atomicity. Do not substitute a no-op or bypass approval. macOS supports the POSIX locking used here; an actual macOS run has not been verified.

## External skills and plugins

- Ponytail: [current upstream](https://github.com/DietrichGebert/ponytail).
- Skill Review: [Mindbox Agent Skills](https://github.com/mindbox-cloud/agent-skills).
- OpenAI Docs, Skill Creator, Skill Installer, Imagegen: use the client's built-in capabilities or the current official distribution. Do not copy an old system cache.
- Visualize, Sites, Work Pets, Plugin Management: install from the client's available marketplace where offered. Copying `SKILL.md` does not transfer services, MCP tools, account permissions or visual renderers.

A missing optional plugin does not block other skills. If a task needs an unavailable capability, identify it and use an available equivalent that preserves the task's requirements. Do not invent an equivalent for independent review without a separate agent or DOCX generation without a required template: stop with the specific reason. SDKs and extra libraries are determined by the task or project.

Runtime sources: [MarkItDown](https://github.com/microsoft/markitdown), [python-docx](https://python-docx.readthedocs.io/), [Python fcntl](https://docs.python.org/3/library/fcntl.html).
