---
name: university-docx-report
description: Create or update a university practical-report DOCX from a Markdown source while preserving a supplied Word style template. Use for styled academic reports, not general document conversion.
---

# University DOCX Report

Общая карта ролей и переходов: [UNIVERSITY_WORKFLOW.md](../UNIVERSITY_WORKFLOW.md).

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

## Report structure

- Read the [shared report core](../university-text-critic/references/report-core.md) for content structure, headings, references, and diagram descriptions. Preserve the approved Markdown hierarchy and wording during export. If a content change is necessary, update the canonical Markdown and obtain a current approval before export; do not silently edit the text in DOCX.
- Do not generate a title page unless it is present in the canonical Markdown or explicitly requested. If the user says they will insert it, omit it entirely; do not add a replacement, a blank title page, institution details, signatures, or inferred metadata.
- Apply section-based figure and table numbering, for example `рисунке 1.1`, consistently with the source. Before export, inspect whether the template styles already generate numbers for headings and captions. If they do, remove only those number prefixes from the text passed to `add_paragraph`; Word must render each number once. Keep the approved Markdown and its references unchanged. Verify the rendered numbering after export, including chapter resets for figures and tables.
- Give the paragraph referring to a figure or table no first-line indent. Keep the figure immediately after its reference. Insert supplied or requested diagram images; otherwise use a styled placeholder only when this handoff is agreed.
- Placeholder wording and layout are content requirements. If the user requests a plain-text placeholder, emit exactly one paragraph with the requested text in the illustration style. Do not expand its wording or convert it into a table, bordered box, shaded block, bracketed note, caption, or reference unless those elements are also present in the canonical Markdown or explicitly requested.

## Styles and tables

- Apply the template's heading, main-text, illustration, and illustration-caption styles. Let styles handle boldness, numbering, and caption formatting; do not emulate them with direct run formatting. Never type a heading or figure number into a paragraph whose style already supplies that number.
- The placeholder for an absent image or diagram uses the illustration style and preserves its source text exactly. Add a caption only when the canonical Markdown contains one; its paragraph uses the illustration-caption style and contains only the source caption text, not a manually typed figure number.
- Never use a table merely to draw or position an image placeholder. Tables are only for tabular report content.
- For table cells, derive a dedicated paragraph style from the template's main-text style. Preserve its justified alignment, but set first-line indent to zero. Apply it to headers and body cells alike.
- Keep tables to rows and columns with no fill or shading. Do not manually bold header cells or table titles.
- Give narrow numeric columns explicit widths when automatic layout would displace row numbers or make them wrap.

## Validation

Run the generator once after final approval and inspect the generated DOCX structurally: confirm the expected template-derived styles, hierarchy, diagram placeholders, and that table cells have no shading. Assert the exact placeholder count and text, the style of every placeholder and heading, and the absence of unrequested title-page paragraphs, tables, borders, and captions. Re-convert that final DOCX to a temporary Markdown file and compare it with the canonical source as a text-integrity check. Account only for representational differences such as Markdown markers, links, and embedded images; every heading, prose passage, list item, table cell, caption, and their order must match. A mismatch is a failed export: fix the generator or source, obtain a current approval if the source changed, and replace the same final DOCX. Do not keep the temporary comparison file in the work folder.

For a minimal `python-docx` implementation pattern, read [references/docx_generation_example.py](references/docx_generation_example.py).
