# DOCX formatting requirements

Formatting rules for every university DOCX built by `university-docx-report`. Read this file
before writing or changing a generator and again before validating its output. The skill
describes the process (source, template, approval gate, validation); this file is the only
place where formatting rules are kept. Add new teacher or reviewer remarks here, not to the skill.

Clause numbers refer to ГОСТ 7.32-2017. Precedence when sources disagree:

1. an explicit requirement of the teacher or the assignment;
2. ГОСТ 7.32-2017;
3. the defaults of the supplied Word template.

When a teacher requirement departs from the standard, keep the rule and name the departure
next to it, as done for bold table heads below. Do not quote a clause from memory: if a rule
is not listed here, read the standard before applying it.

Express every rule through paragraph styles derived from the template's main-text style.
Direct paragraph or run formatting is a last resort, because Word drops it when a field or a
style is refreshed.

## Report structure

- Read the [shared report core](../../university-text-critic/references/report-core.md) for
  content structure, headings, references and diagram descriptions. Preserve the approved
  Markdown hierarchy and wording during export. If a content change is necessary, update the
  canonical Markdown and obtain a current approval before export; do not silently edit the
  text in DOCX.
- Order of structural elements when the report has them (section 4): титульный лист, реферат,
  содержание, термины и определения, перечень сокращений и обозначений, введение, основная
  часть, заключение, список использованных источников, приложения. Include an optional element
  only when the assignment, the user or the accepted structure requires it.
- Headings of structural elements («СОДЕРЖАНИЕ», «ПЕРЕЧЕНЬ СОКРАЩЕНИЙ И ОБОЗНАЧЕНИЙ»,
  «ВВЕДЕНИЕ», «ЗАКЛЮЧЕНИЕ», «СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ», «ПРИЛОЖЕНИЕ») are centred,
  upper-case, unnumbered, without a full stop. Every structural element and every section of
  the main part starts on a new page (6.2.1).
- Bold type is allowed only for headings of sections, subsections and structural elements
  (6.1.1). The single agreed exception is the table head, see «Tables».
- Do not generate or fill a title page. If the folder supplies a ready title-page document and
  the user has not said they will insert it themselves, insert that file unchanged before the
  contents through the builder; a rule against creating or filling a title page does not forbid
  this. If the user says they will insert it, or none is supplied, omit it entirely; do not add
  a replacement, a blank title page, institution details, signatures, or inferred metadata.
- Apply section-based figure and table numbering, for example `рисунке 1.1`, consistently with
  the source. Before export, inspect whether the template styles already generate numbers for
  headings and captions. If they do, remove only those number prefixes from the text passed to
  `add_paragraph`; Word must render each number once. Keep the approved Markdown and its
  references unchanged. Verify the rendered numbering after export, including chapter resets
  for figures and tables.
- Keep the template's first-line indent on every body paragraph: also on a paragraph that
  refers to a figure or table, on the first paragraph after a heading and on the «где»
  paragraph after a formula. Never zero the indent for them; `keep_with_next` is enough to hold
  a reference with its figure or table. Only table-cell paragraphs, table captions, contents
  entries and abbreviation-list entries have zero first-line indent.
- Keep the figure immediately after its reference. Insert supplied or requested diagram
  images; otherwise use a styled placeholder only when this handoff is agreed.
- Placeholder wording and layout are content requirements. If the user requests a plain-text
  placeholder, emit exactly one paragraph with the requested text in the illustration style. Do
  not expand its wording or convert it into a table, bordered box, shaded block, bracketed note,
  caption, or reference unless those elements are also present in the canonical Markdown or
  explicitly requested.

## Contents

Applies when the report has «СОДЕРЖАНИЕ» (5.4.1, 6.13).

- The contents list starts with «Введение» and includes sections, subsections, «Заключение»,
  «Список использованных источников» and appendices. «Реферат», «Содержание» and «Перечень
  сокращений и обозначений» are not listed unless the teacher requires it. Give such headings
  a style outside the outline levels the `TOC` field collects, otherwise Word adds them on the
  next field update.
- Every entry is a separate left-aligned paragraph. The page number is right-aligned and joined
  to the title by a dot leader.
- Section entries and structural-element entries have no indent at all: neither left nor
  first-line. The template's `toc N` styles usually inherit the main-text first-line indent;
  reset it explicitly.
- Subsection entries are indented by two characters relative to section entries, clause
  entries by four. For 14 pt text use 0.5 cm and 1 cm.
- A title that wraps continues from the position where the title starts on its first line, not
  from the page margin: use a hanging indent in the subsection entry style.
- Set these properties on the template's `toc 1`, `toc 2`, `toc 3` styles in the generator.
  Word rebuilds the entries from those styles whenever the field is updated, so direct
  formatting of generated entries does not survive.

## Abbreviations

Applies to every report (5.6, 6.15).

- Every abbreviation used in the text, for example «ПР1», «ВКР», «НФТ», must be expanded in
  «ПЕРЕЧЕНЬ СОКРАЩЕНИЙ И ОБОЗНАЧЕНИЙ». The list is required when the report has three or more
  abbreviations that need an explanation; with fewer, expand them at first mention instead.
- Commonly known abbreviations are not listed: «ГОСТ», «ИСО», «МЭК», «ФЗ», «ФИО», «PDF», «ID»,
  «IP», «HTTPS», «URL». HTTP method names, product names and abbreviations that occur only on
  the title page or in the list of sources are not listed either.
- Before composing the list, extract all abbreviations from the text and show them to the user
  with proposed expansions; compose the list only from the confirmed set. Take an expansion
  from the source the report analyses when it defines one; do not guess.
- The list is report content. It lives in the canonical Markdown and passes the critic like
  any other section. If the approved Markdown has abbreviations but no list, stop and return to
  the Markdown; do not add the list in the DOCX.
- Place the element after «СОДЕРЖАНИЕ» and before «ВВЕДЕНИЕ», on a new page. It is not listed
  in the contents, see «Contents».
- The element starts with the sentence «В настоящем отчёте применяют следующие сокращения и
  обозначения:».
- Entries form a column: one paragraph per abbreviation, without first-line indent,
  left-aligned, the abbreviation, an en dash, the expansion, no punctuation at the end of the
  line. Order is alphabetical: Cyrillic entries first, then Latin ones, case-insensitive. A
  numbered family is listed once by its stem: «ПР – практическая работа» covers «ПР1»–«ПР4».

## Tables

- A table caption sits above its table: `Таблица N – Наименование` with an en dash,
  left-aligned, zero first-line indent and `keep_with_next` (6.6.3). If the template has no
  table-caption style, derive one from the main-text style; every table needs a reference by
  number before it. Type the number only when the template does not generate it.
- A caption of two lines or more is single-spaced (6.6.3): give the caption style single line
  spacing.
- A table that continues on another page repeats its head; the following parts are labelled
  «Продолжение таблицы N» on the left above them (6.6.3).
- Column and row headings start with a capital letter, have no full stop at the end and are in
  the singular (6.6.5): «Повтор», «Предусловие», not «Повторы», «Предусловия». The wording is
  report text: it is fixed in the canonical Markdown (see the shared report core), the generator
  does not rewrite it.
- Body cells: a dedicated paragraph style derived from the template's main-text style, zero
  first-line indent, left-aligned. Do not keep the main text's justified alignment in cells.
- Head cells (column headings): a second style derived from the body-cell style, centred
  (6.6.6) and bold. Bold is a teacher requirement and a deliberate departure from 6.1.1; apply
  it through the head style, never to body cells or table captions.
- Keep tables to rows and columns with no fill or shading. Never use a table merely to draw or
  position an image placeholder.
- Give narrow numeric columns explicit widths when automatic layout would displace row numbers
  or make them wrap.

## Code

Applies to every fenced code block of the canonical Markdown: request and response examples,
configuration, scripts, command output. This is a user requirement; ГОСТ 7.32-2017 does not
regulate program text in the body of a report.

- Place each code block in its own table of one row and one column with the template's grid
  style («Table Grid»), so the frame sets the code apart from the body text. The table has no
  caption, number, head or fill and is not counted among the numbered tables.
- Every source line is a separate paragraph in the template's «Код» style (monospace font,
  single spacing). Keep leading spaces; an empty source line becomes an empty «Код» paragraph.
  Use no other style inside the cell, do not change the font through direct formatting and do
  not derive a parallel code style when the template has «Код». Without such a style, derive
  one from the main-text style: monospace font, single spacing, zero first-line indent.
- A line wider than the cell wraps. If wrapping hides the structure of the example, shorten it
  in the Markdown; do not shrink the font.
- The row does not break across pages (`cantSplit`) when the block fits on one page, and the
  paragraph introducing the block keeps with it (`keep_with_next`).

## Formulas

- A display formula is written on its own line as `$$formula \tag{n}$$`, a symbol or short
  formula inside prose as `$...$`. The generator emits native Word equations (OMML), never plain
  text with Unicode subscripts. Use [docx_math.py](docx_math.py): LaTeX subset with `\frac`,
  `^`, `_`, `\sum`, `\times`, `\cdot`, `\approx`, `\le`, `\ge`, `\text`/`\mathrm`, round
  brackets; Cyrillic letters are upright.
- Display structure copies the user's formula example: a main-text paragraph holding
  `m:oMathPara > m:oMath > m:eqArr`, with the formula, a space, `#` and the number inside `m:d`,
  so Word right-aligns the number. The author types the numbers and they run consecutively; the
  generator does not renumber.
- Leave one free line above and one below every display formula (6.8.1): an empty main-text
  paragraph before the formula paragraph and another after it. Chain the first empty paragraph
  and the formula with `keep_with_next` so that a page break cannot separate them from the
  «где» paragraph. These empty paragraphs are layout, not content: skip them in text comparisons.

## Lists, figures and styles

- A Markdown line starting with `- ` is an item in the template's list style, resolved by name
  like any other semantic style. A generator that rejects or flattens such lines is defective:
  add list support instead of rewriting the report into prose.
- Apply the template's heading, main-text, illustration and illustration-caption styles. Let
  styles handle boldness, numbering and caption formatting; do not emulate them with direct run
  formatting. Never type a heading or figure number into a paragraph whose style already
  supplies that number.
- The placeholder for an absent image or diagram uses the illustration style and preserves its
  source text exactly. Add a caption only when the canonical Markdown contains one; its
  paragraph uses the illustration-caption style and contains only the source caption text, not
  a manually typed figure number.
