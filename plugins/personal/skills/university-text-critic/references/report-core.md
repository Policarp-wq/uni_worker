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
- For each real design uncertainty (architecture style, database technology, protocol)
  give a short table of genuine alternatives with the criteria and the choice; one
  alternative in a table is not a comparison. Keep the problem, the decision and its
  check as separate statements, not one fused paragraph. Add a formula only where a
  calculation is performed, not as a decoration per item.
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
- A completeness claim about a model («тупиков нет», «каждый путь завершается»,
  «все случаи покрыты») must hold without an added assumption. If it only holds
  because an assumption rules a case out («сбой устраняется за 24 часа»), the model
  lacks an outcome for that case: add the outcome (state, end event, branch) or
  narrow the claim to the assumed conditions. Recording the assumption alone does
  not close the gap.
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
- User preference: losing up to 5% of secondary detail to remove about half of
  inflated text is preferable to keeping the detail. Mandatory meaning and
  justification are never cut. A wall of text is a defect in any section, not only
  in answers: when a paragraph carries several ideas, split or cut it instead of
  polishing sentences.
- Answer an assignment question directly in one to three sentences: the answer, then
  the key reason. Do not restate the question, add background or list every caveat.
- Justify a chosen option in one clause. Do not keep the unchosen fallback or a
  closing paragraph about general caveats, source-check dates or what was not analyzed
  unless the assignment asks for it; report such limits to the user in the handoff.
- Do not give entities code names such as `UC1`, `E2`, `Q3` or `H1` in prose, headings
  or tables unless the assignment prescribes them. Use a name, or a number with a word
  («прецедент 3», «Альтернатива 2»), and refer to earlier works by the name of the
  item or «вопрос 4 таблицы 1.5 ПР2».
- Do not mix two languages inside one phrase («целочисленную version»). Use the
  Russian term or restructure the sentence.
- Do not use em dashes `—` in authored prose. Restructure, use a colon or split the
  sentence. Before delivery, find every `—` and confirm it remains only in required
  quotations, code, formulas, official names or externally prescribed captions.
  Do not mechanically replace dashes with hyphens.
- Prefer «серверная часть» to `backend`; prefer «уведомление о смене статуса» or,
  at first mention, «вебхук-уведомление» to `webhook`. Keep useful terms and abbreviations
  API, C4, RPS, MFA; explain unfamiliar ones at first use.
- Use one term per object. Do not alternate «мерчант», «клиент», «арендатор» and
  «тенант» for the same role. Add terms to a glossary when the work includes one.

## Veil: text about the work instead of the work

The «пелена» is prose the reader does not need to understand the result. It hides
the decisions in surrounding narration. A hollow paragraph is deleted, not polished:
restructuring it only produces a clean hollow paragraph. Remove from final prose:

- Production history and provenance: which script, tool or session made an artifact,
  that models «не расходятся» because one generator builds them, links to source files
  (`.drawio`, `.archimate`, `.py`) unless the assignment requires them in the text.
  Keep tool facts the assignment asks for in one clause, and real verification limits
  once, in the limitations section.
- Non-decisions: what did not become a class, subtype, table or section and why,
  unless the assignment asks for it (for example a mapping table with empty cells).
  One mention in the place the assignment prescribes is enough.
- Retelling an adjacent figure or table in prose: «инварианты 1–9 перенесены…»,
  «связь показана ассоциацией…». Give the reference and only what the figure cannot show.
- Optional material beyond the assignment: an extra table, a second secondary
  deviation, background calculations. If an earlier work left questions, close them
  only when the current assignment asks.
- Uniform rows in reference tables: surrogate `id`, `created_at`, `updated_at` with the
  same constraint and source in every table are stated once in a sentence. Merge
  same-typed fields with identical constraints into one row.

Write counts and quantities as digits: «9 прецедентов», «3 записи», not «девять».
Keep words inside fixed expressions («в три приёма», «оба варианта»).

## Sentence discipline

Adapted from the structural rules of ASD-STE100 for Russian academic prose. They
apply to authored prose, not to tables, captions, code or verbatim blocks.

- One idea per sentence. Keep a sentence within 25 words. A longer sentence needs a
  reason (a single condition that cannot be split); over 40 words is always split.
- One topic per paragraph, at most 6 sentences.
- Use the verb, not its noun: «шлюз проверяет подпись», not «осуществляется проверка
  подписи шлюзом». Avoid «является», «производится», «путём выполнения».
- Do not stack more than 3 nouns in a genitive chain: «проверка допустимости связей
  объектов модели» → «проверка, какие связи допустимы между объектами».
- Do not join independent clauses with a semicolon in prose: split the sentence.
  A semicolon at the end of list items is allowed.
- Do not stack hedges («может потенциально способствовать»). State the claim or remove
  it. Keep the strength of every claim: «может завершиться ошибкой» does not become
  «завершается ошибкой».
- Never add a cause, number or mechanism while rewriting. A sentence that reads better
  because it states a new fact is no longer an edit.
- Stop cutting when the sentence is unambiguous. Shortest is not the goal.

## Mandatory compression pass

Every final report passes a measured compression round before critic review. Prose
words exclude tables, code, display formulas, images, headings and captions; the
critic gate counts them with `scripts/prose_gate.py`.

1. Record `baseline` on the first complete final version, not on the draft.
2. Cut at least 10% of prose words with the veil and sentence rules above: delete
   whole explanations, repeated conditions and narration first, retyping sentences last.
3. Run `compress`. It approves only with at least 10% reduction and no hard lint
   findings (stock phrases, em dashes in prose, sentences over 40 words).
4. Fixes after review may add at most 5% back. More growth requires a new round.

If 10% cannot be reached without losing mandatory meaning, stop and show the human
the measured result and the blocking passages. Only an explicit human decision may
be recorded with `compress --waive`; the author does not waive the round alone.

## Figures and diagrams

- Use the notation, tool and level of detail the assignment and its sample prescribe.
  A storage schema shown with numeric multiplicities in the sample (`1`, `0..1`,
  `0..*`) is not drawn in crow's foot notation, and vice versa.
- The image contains the diagram only. No legend, explanatory notes, footnotes or
  verification remarks inside it; meaning belongs in the text, the caption is added
  by the template. A title inside the image must not repeat or contradict the caption.
- Every class, table, relation and multiplicity in the image matches the text, tables
  and data dictionary: counts, names, keys and cardinalities agree.
- Use a readable sans-serif font and the same style across the figures of one work.

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
  Write list items as `- ` lines, not as a semicolon chain inside one paragraph.
- Write a display formula on its own line as `$$formula \tag{n}$$` (LaTeX subset) and
  symbols inside prose as `$...$`; do not type fractions, sums or indices as plain
  Unicode text. Number formulas consecutively and cite them as «по формуле n». Follow
  each display formula with a «где» paragraph listing symbols after a hyphen (`w_i - вес`),
  not a dash.
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
