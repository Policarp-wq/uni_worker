# Maintaining Agent Kit

Keep the package portable: no personal profiles, contacts, credentials, home paths, agent memory or runtime review state. Templates use placeholders; examples use explicitly fictional values.

Keep the Codex and Claude marketplace manifests consistent. Shared skills live in `plugins/personal/skills`; client-specific reviewer setup is documented in `plugins/personal/instructions/CLIENTS.md`.

Preserve independent academic review and the fail-fast native Windows restriction. Do not add a bypass for missing tools or resources. Do not vendor third-party plugins; document their current upstream installation instead.

When changing shipped files, regenerate `FILES.md` and run `python3 scripts/check.py` plus the critic tests. Increment our own plugin version consistently in the three plugin manifests when publishing an update; third-party dependencies remain unpinned.
