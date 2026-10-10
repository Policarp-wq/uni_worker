# Contents and privacy

The export starts with 21 previously audited text files: ten original skills and their resources, the shared academic workflow and global instructions. Packaging adds manifests, setup, general instructions for academic and development folders, client adaptations for independent review, documentation and package checks. The exact final list is in [FILES.md](../FILES.md).

Excluded:

- Populated personal profiles, memory, chat history and runtime critic state.
- Codex/Claude configuration, tokens, keys, `.env` and GitHub credentials.
- System skills, third-party plugins, their caches and old snapshots.
- Academic reports, PDF, DOCX, images, datasets and application source code.
- Instructions for individual subjects or projects, their generators, requirements and Word templates.

Personal placeholders are `{{STUDENT_FULL_NAME}}`, `{{STUDENT_GROUP}}`, `{{INSTITUTION_NAME}}` and `{{TEACHER_FULL_NAME}}`. Configure values at the first task that requires them; store them only in an excluded local profile or user-approved memory. The explicitly fictional examples «Иванов И. И.» and «ИКБО-00-00» are not user settings.

Portable copies also adapt workspace discovery to the current environment and provide a new general academic parent profile where the original shared file was unavailable. These new templates do not claim to restore missing files. Each assignment and its local instructions determine its format; another subject's profile does not.

Instructions are in English; Russian linguistic examples and literal output templates remain in Russian. The academic workflow, reasoning requirements and Russian writing rules are unchanged.

`scripts/check.py` checks the package structure and known classes of leaks. It is a heuristic: regular expressions cannot reliably identify a new personal name or arbitrary document content. Review diffs and explicitly exclude personal information before adding materials. Binary documents are not accepted in this package.
