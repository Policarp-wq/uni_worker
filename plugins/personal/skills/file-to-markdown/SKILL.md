---
name: file-to-markdown
description: Use an existing same-basename Markdown rendition, or convert PDF, DOC, DOCX and PPTX to Markdown before reading their contents. Images, spreadsheets, HTML and other text formats may be read directly. Reading, transcribing or converting audio is prohibited.
---

# File To Markdown

Mandatory conversion applies only to `.pdf`, `.doc`, `.docx` and `.pptx` (case-insensitive). Images, spreadsheets, HTML, plain text and other formats do not require this skill and may be read directly with appropriate tools.

Do not read, listen to, transcribe, convert or otherwise process audio files. This prohibition also applies to `markitdown` and other converters. Listing filenames is allowed and does not authorize processing their contents.

## Reuse Markdown before conversion

Before reading a protected document, check for a `.md` file with the same basename next to it: `assignment.docx` → `assignment.md`. If a non-empty, valid UTF-8 rendition exists, read it directly. Do not run a converter, create a second rendition or overwrite the existing Markdown merely because the original document was named in the request. Use an explicitly identified existing rendition at another path if one was already created for this task.

Convert only when no usable rendition exists. If a current rendition was edited by the user or its relationship to the source is unclear, preserve it; do not silently replace it.

For DOCX files, direct inspection of document structure is allowed only to validate the formatting, styles or layout of a document that has already been converted to Markdown. Do not use structural inspection as a substitute for reading its textual content. Creating a new output file is not reading a source document.

## Conversion

- If `markitdown` is not on `PATH`, check the current workspace's `.venv/bin/markitdown` (Linux/WSL/macOS) or `.venv/Scripts/markitdown.exe` (Windows); use it only if it exists.
- Prefer the installed `markitdown` CLI: `markitdown <input> -o <output.md>`.
- For university practical work whose source is inside a writable workspace, keep the conversion beside the source with the same basename so later turns can reuse it. Determine the writable workspace from the current environment.
- Only leave persistent conversions inside a writable workspace. For sources outside the workspace, do not create a neighboring persistent Markdown file; use an explicitly authorized workspace destination or a temporary path instead.
- Otherwise, place the output next to the source with the same basename unless the user specifies a destination. Keep conversions inside the authorized working folder when that is a task constraint.
- Retain the original document. For batches, check for existing Markdown separately for each source and convert only missing renditions.
- Never route audio through this workflow, even if the converter technically supports it.

## Validate before reading

- Confirm conversion succeeded and that the result is non-empty and valid UTF-8.
- Inspect the beginning, end and structurally important portions before relying on it. For PDFs, check page coverage when page markers or page counts are available.
- Check for replacement characters, garbled encoding and missing sections. State material loss or ambiguity to the user.
- If the source is a scan or conversion yields no readable text, use an available OCR-capable path for the document or report that OCR is needed; never silently treat it as empty content.

Tables and complex layouts may lose their visual structure during conversion. Distinguish a formatting limitation from loss of textual content. Direct viewing of images is permitted and needs no Markdown conversion.
