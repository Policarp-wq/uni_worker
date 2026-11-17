---
name: university-docx-report
description: Create or update a university practical-report DOCX from a Markdown source while preserving a supplied Word style template. Use for styled academic reports, not general document conversion.
---

# University DOCX Report

Shared roles and transitions: [UNIVERSITY_WORKFLOW.md](../UNIVERSITY_WORKFLOW.md).

Academic prose remains in Russian. Preserve approved Russian wording, style names
and literal templates; the English instruction language does not change the output language.

Use one Markdown file as the canonical source for a practical report. It contains the report text, tables, diagram descriptions, and PlantUML code blocks. The only final DOCX is the sibling file with the same basename: `PR3.md` becomes `PR3.docx`. Build it from that source and the user's style-only DOCX template. The report is a section of a later consolidated coursework document; do not add coursework-only front matter, contents, or conclusions unless requested.

## Final-only export

- Keep every content correction in the canonical Markdown. Do not create or refresh a DOCX while the author or critic is still changing that file.
- Export only after all Markdown corrections are complete and the current file has valid critic approval. If review requires another edit, return to Markdown; do not generate an intermediate DOCX.
- Write the final document beside the source as `source.with_suffix(".docx")`. Do not leave alternate, numbered, preview, or temporary DOCX files in the work folder.
- The DOCX must preserve the approved source's headings, prose, lists, table text, captions, and their order. Formatting may differ; content may not be added, omitted, or rewritten during export.

## Required critic approval

If the input is still a meaning-building draft, first use [university-report-writer](../university-report-writer/SKILL.md) to prepare the final Markdown. Before creating or updating a university DOCX, automatically use [university-text-critic](../university-text-critic/SKILL.md). The calling author supplies the subject, topic, requirements, and readable paths to relevant previous works; a separate agent with no inherited conversation performs the review. Reuse a valid approval for unchanged inputs.

Require a valid hash-bound `.critic-approve` beside the canonical Markdown. A file's existence alone is insufficient. Every generator must call `require_approval(source)` from the critic's `scripts/critic_gate.py` before document construction and immediately before saving. Build from that exact source; do not substitute hardcoded report text. Add the checks to new generators before their first run. No alternate exporter, temporary DOCX, or manual marker may bypass this gate.

Changed source or context invalidates approval. Allow at most three critic launches per review cycle across sessions; after exhaustion, stop and present the concrete disagreement to the user. Only an explicit user decision recorded through `resolve` starts a new cycle; it does not grant approval. If an independent agent or valid approval is unavailable, DOCX generation remains blocked.

## Source and template

- Before reading a DOCX, look for its non-empty neighboring Markdown rendition and use it as the text source when available.
- Before writing or changing a generator, search the report directory and repository ancestors for existing `build*docx*.py` generators, shared DOCX templates, and documented style names. Read the closest relevant generator and reuse its template path and style mapping. Do not assume the report directory is the repository root.
- Preserve the style template and build a new DOCX from a copy of it. When a template exists, `Document()` is prohibited: load it with `Document(template_path)`, then clear only its document body while retaining styles and section properties. A direct-DOCX-reading restriction is not a reason to rebuild formatting manually; prepare the required Markdown rendition, then use structural inspection only for styles and layout.
- Treat the template's semantic styles as required inputs. Resolve the heading, main-text, illustration, illustration-caption, list, and other requested styles by their actual names and fail clearly if a required style is absent. Do not silently fall back to `Normal`, manually reproduce the font, or invent a parallel style when the template already supplies one.
- Keep the resolved template path and semantic style mapping in the generator so rerunning it preserves the same formatting. Reuse an existing repository generator before creating a new one.
- Direct DOCX structural inspection is allowed only after Markdown extraction and only to validate styles, formatting, layout, or the generated output.
- Create report-specific paragraph styles when the template lacks one; base them on the user's main-text style rather than applying manual formatting to runs.

## Formatting requirements

All formatting rules are kept in [references/formatting-requirements.md](references/formatting-requirements.md): report structure, contents, the list of abbreviations, tables, formulas, lists, figures and styles, with the ГОСТ 7.32-2017 clauses and teacher requirements behind them. Read that file in full before writing or changing a generator and again before validating its output. Do not format from memory and do not restate its rules here.

When the user, a teacher or a reviewer gives a new formatting remark, add it to that file, then change the generator. A remark that changes report text, such as a missing list of abbreviations, is a content correction: return to the canonical Markdown and obtain a current approval.

## Validation

Run the generator once after final approval and inspect the generated DOCX structurally: confirm the expected template-derived styles, hierarchy, diagram placeholders, and that table cells have no shading. Check every applicable rule of the formatting requirements, at least: contents entry styles have no first-line indent and section entries no left indent; head cells use the centred bold head style and body cells the left-aligned cell style; an empty paragraph stands before and after each display formula; every abbreviation found in the text is either in the list of abbreviations or commonly known. Assert the exact placeholder count and text, the style of every placeholder and heading, and the absence of unrequested title-page paragraphs, tables, borders, and captions. Re-convert that final DOCX to a temporary Markdown file and compare it with the canonical source as a text-integrity check. Account only for representational differences such as Markdown markers, links, and embedded images; every heading, prose passage, list item, table cell, caption, and their order must match. A mismatch is a failed export: fix the generator or source, obtain a current approval if the source changed, and replace the same final DOCX. Do not keep the temporary comparison file in the work folder.

For a minimal `python-docx` implementation pattern, read [references/docx_generation_example.py](references/docx_generation_example.py).
