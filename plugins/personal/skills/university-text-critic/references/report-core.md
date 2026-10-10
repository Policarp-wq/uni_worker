# Shared academic writing rules

This is the single source of final-prose requirements for writer and critic. Update
this file when shared requirements change, not separate copies in skills. Explicit
user/assignment formats take precedence over general preferences; clarify specific
incompatible requirements. Write academic deliverables in Russian. Russian literals
below are intentional wording examples or output requirements, not untranslated
instructions.

## Draft and final prose

A draft accumulates facts, decisions, arguments, calculations and open questions.
Long explanations, repetition, informal notes, alternatives and unfinished structure
are acceptable and are not inherently draft defects. The following rules apply to
final work.

Final Markdown addresses the report's reader. Exclude discussion history, assistant
addresses, critic comments, promises to «добавить позже», unprocessed TODO and
unselected alternatives. Open substantive questions are acceptable when recording
them is itself assigned. Ready for review does not mean approved for DOCX: a separate
critic grants that permission.

## Meaning and justification

- Cover mandatory assignment items. Preserve decisions, results, meaningful numbers,
  correctness conditions and causal links. Do not invent data, sources, tests,
  technologies or requirements for a finished appearance.
- Check quantity labels against the assignment and data metadata. Currency, physical
  unit, scale and measure meaning cannot be inferred from dataset names or general
  knowledge of their origin. If unconfirmed, keep a neutral measure label and do not
  add a designation such as `BRL`.
- Distinguish accepted decisions, discussed alternatives and open questions. Do not
  treat a draft proposal as agreed or replace a user decision without discussion.
- Label user-selected educational values as design assumptions, not external facts.
  For a quality measure, give conditions, target and verification method when assigned;
  do not invent a numeric standard.
- Check participants, terms, boundaries and decisions against previous works. Explain
  justified changes briefly. Do not preserve an old error for formal consistency.
- Separate system responsibilities from external participants. Initiating a bank
  operation is different from executing it. Do not replace «планируется проверить»
  with «проверено» without an actual result.
- Preserve required verbatim educational blocks and quotations. Express other content
  in your own words without restating the assignment before every step.

## Internal logic

- Conclusions must follow from stated premises and calculations. Do not call a
  solution reliable, secure or sufficient without the boundaries where that holds.
- Compare related claims across sections. Assumptions, exceptions and failure scenarios
  must not silently invalidate an earlier result, invariant or requirement.
- Educational simplification without implementation detail is acceptable when explicit,
  not presented as proven fact and compatible with the assignment. Missing production
  detail is not inherently an academic defect.
- Do not demand new technologies, components or independent domain research. Prefer
  narrowing a conclusion accurately over expanding architecture when that closes
  a logical gap.

## Assignment-based structure

- Follow assigned section names, order and numbering. Map content to each item;
  do not replace assignment structure with a universal template.
- Before headings/captions, inspect the template or builder to establish which numbers
  and words («Рисунок», «Таблица», etc.) Word adds automatically. Keep only substantive
  text in those Markdown elements; do not type generated numbers/words manually.
  Without automatic numbering, or with assigned literal text, keep the required format.
  Do not impose a universal ban on numbers.
- Without assigned sections, group content meaningfully and use specific headings.
  Process descriptions might use «Участники», «Ход процесса», «Обработка ошибок»;
  these are examples, not required sections. Content determines their count.
- Default hierarchy: one practical uses `#`, its main sections `##`, and optional
  subsections `###`. In a combined document, practicals are top-level sections.
  For a requested fragment, preserve its place in the existing hierarchy.
- Each section develops a distinct thought. Do not create a heading per sentence
  or a section merely for symmetry.
- Include introduction, goal, tasks, conclusion, title page, contents or glossary
  only when required by the assignment, user or accepted structure. Do not add them
  automatically.

## Language and concision

Apply [humanize-ru-academic](../../humanize-ru-academic/SKILL.md) when writing or
substantively editing final prose. The writer uses it before handoff; the critic
checks concrete weaknesses by the same criteria. It adapts editing to Russian
academic language and supplements this core, not the assignment. If both files
were already read, do not follow their mutual links again.

- Use natural Russian in a moderately academic register. Prefer concrete
  «кто делает что и зачем». Do not inflate the text into a research article or turn
  it into informal conversation.
- «Шлюз передаёт запрос провайдеру» is appropriate. «Осуществляется реализация механизма обеспечения взаимодействия» is too heavy. «Шлюз кидает запрос, и всё норм» is too informal. Do not simulate humanity with typos.
- Remove empty preambles, bureaucracy and generic praise: «следует отметить»,
  «важно подчеркнуть», «в рамках данной работы», «играет ключевую роль»,
  «обеспечивает эффективность и надёжность». Meaningful logical connectors are allowed.
- Remove repetition, paraphrased headings/tables, explanations of obvious code,
  general advice and repeated caveats. Keep necessary explanations of nontrivial
  decisions or limits once, where relevant.
- User preference: cutting about 40% of inflated text at the cost of up to 5% of
  secondary detail is preferable. This is guidance, not a quota or measured share
  of meaning. Do not cut already dense prose or sacrifice mandatory meaning and
  justification to meet a percentage.
- Do not use em dashes `—` in authored prose. Restructure, use a colon or split the
  sentence. Before delivery, find every `—` and confirm it remains only in required
  quotations, code, formulas, official names or externally prescribed captions.
  Do not mechanically replace dashes with hyphens.
- Prefer «серверная часть» to `backend`; prefer «уведомление о смене статуса» or,
  at first mention, «вебхук-уведомление» to `webhook`. Keep useful terms and abbreviations
  API, C4, RPS, MFA; explain unfamiliar ones at first use.
- Use one term per object. Do not alternate «мерчант», «клиент», «арендатор» and
  «тенант» for the same role. Add terms to a glossary when the work includes one.

These rules do not identify AI authorship. An allowed exception or preference for
another correct word must not block finished work; explicit factual, numbering and
punctuation requirements are checked separately.

## Markdown for DOCX transfer

- Save UTF-8 `.md` using ordinary headings, paragraphs, lists, tables, links and code
  blocks. Do not emulate Word layout with spaces, HTML or manual page breaks.
- Before handoff, search possible manual numbers and em dashes, for example:
  `rg -n '—|^#{1,6} +[0-9]+[.)]|^(Рисунок|Таблица) +[0-9]+' <report.md>`.
  Assess each match in context and against numbering rules; do not autofix it.
- Use lists for sequences or parallel items and tables for shared-field comparisons.
  Explain what a list enumerates without adding a formal preamble for its own sake.
- Give a short reference before each table/figure. Put a figure reference immediately
  before it; align labels/captions with sections and accepted numbering.
- Preserve a diagram's semantic description before its separate PlantUML block or
  other assigned representation. Keep existing image links; do not claim an absent
  image has been inserted. Explicit placeholders require an agreed handoff format.
- Check relative image/material links when saving elsewhere. Tables must have clear
  column boundaries and code blocks must be closed.
- Word layout, fonts, styles and page breaks belong to DOCX generation. Final Markdown
  must not need substantive rewriting during transfer.

## Editorial decision example

Draft: «Следует отметить, что мы обсуждали два варианта. В итоге решили, что подпись проверяет шлюз. Если подпись неверная, статус менять нельзя. Это важно для надёжности системы».

Final: «Шлюз проверяет подпись уведомления. Уведомление с неверной подписью не меняет статус платежа».

The decision and correctness condition remain; discussion history and generic praise
are removed. If comparison is assigned, preserve its arguments in the relevant section.
