# General academic rules

These portable rules define the shared academic workflow. Each assignment and its applicable local instructions determine the specific format. Write academic deliverables in Russian; English instructions do not change Russian style or literal output requirements.

- Before reading PDF, DOC, DOCX or PPTX, reuse existing neighboring Markdown with the same basename or use `file-to-markdown`. Do not process audio.
- For new work, use `university-work-planner`, then `university-work-executor`. Set interaction and deliverable modes independently: `автономно`/`итерационно` and `с отчётом`/`только артефакты`.
- Do not invent completed actions, measurements, program outputs or personal data. Preserve user decisions and actual results in one plan.
- Use `university-writing-style` for discussion and drafts; use `university-report-writer` and `humanize-ru-academic` for the final report based on completed substantive work.
- Each report has one canonical Markdown source. For completed or substantively changed reports, invoke `university-text-critic` as a separate agent. The author must not approve their own text.
- Generate DOCX with `university-docx-report` only after valid hash-bound approval. Every generator calls `require_approval` before document construction and immediately before saving. Do not bypass the gate with another exporter or intermediate DOCX.
- Use only the supplied Word template. If a required resource or independent agent is missing, stop with the specific reason.
- Request personal fields only when required by the output format. Read the local profile or approved memory; ask once for missing required values. Substitute them only into deliverables, never skills or examples.
- After review, report status, remaining recommendations and reasons for leaving them unapplied. Do not hide limitations behind successful approval.
