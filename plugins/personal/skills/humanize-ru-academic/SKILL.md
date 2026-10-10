---
name: humanize-ru-academic
description: Write and edit Russian academic work in natural, moderately academic language without bureaucratic phrasing, empty praise or stock expressions. Apply to final practical/lab/coursework prose, notebook explanations and requests to remove AI-like or robotic style. Do not edit verbatim assignment blocks, quotations or working notes until they are being turned into final prose.
---

# Natural Russian academic prose

Example Russian requests: «убери нейросетевой стиль», «очеловечь текст»,
«слишком роботизированно».

An adaptation of the user-supplied English `humanize-writing` 2.0.0 for Russian
academic work. Aim for accurate text showing actual actions, reasons for decisions
and the limits of results. Do not imitate human authorship through errors, random
digressions or invented experience. These techniques improve editing; they do not
establish authorship or guarantee AI-detector results. Write the deliverable in
Russian. Keep the Russian examples below as language guidance, not facts to invent.

## Place in the workflow

Apply relevant techniques while writing; review existing prose when editing. The
eight passes below are aspects of review, not a requirement to rewrite eight times.

In the academic workflow, the writer applies this skill before saving final Markdown
and handing it to the independent critic. The critic uses the same criteria and
identifies concrete weaknesses, not presumed origins. This skill does not launch
review, grant approval or change the DOCX procedure.

Read the [shared writer/critic core](../university-text-critic/references/report-core.md).
It defines required content, structure, punctuation and Markdown; this skill provides
editing techniques. Do not duplicate shared rules. If already read for the current
task, do not reread it. Explicit user and assignment requirements take precedence.

Before editing, read the text and available grounds: assignment, agreed decisions,
calculations and results. Preserve numbers, units, formulas, references, names,
terms and strength of claims. Do not resolve substantive uncertainty by guessing.
Report a missing source separately from the final work; do not supply a plausible
but unverified reference.

## 1. Remove mechanical structure

Look for identical introductions and mini-conclusions in every section, repeating
a heading in the first sentence and equally sized lists padded for symmetry.
Combine repeated explanations; choose paragraphs, lists or tables for their content.

Do not change required sections or assignment order for variety. Matching structures
for comparable experiments help comparison and do not inherently need correction.
A required conclusion must answer the tasks and follow from results.

Before: «В данном разделе рассматривается обработка ошибок. Обработка ошибок является важной частью системы. Таким образом, обработка ошибок имеет большое значение».

After: «При ошибке проверки подписи шлюз отклоняет уведомление».

Use that replacement only if this behavior already exists in the materials.
Otherwise remove repetition without inventing a mechanism.

## 2. Replace exaggeration with concrete content

Check expressions such as «играет ключевую роль», «имеет огромное значение»,
«открывает новые горизонты», «революционный подход», «мощный инструмент» and
«обеспечивает высокую эффективность». Remove the judgment or describe a supported
action and result. Replacing «ключевой» with «важный» does not fix the problem.

Before: «Индекс играет ключевую роль в значительном повышении производительности».

After, with measurements: «После создания индекса время запроса сократилось с 420 до 35 мс».

The example numbers are fictional. Use only the work's own measurements. Without
measurements, do not claim achieved speedup; describe the index's purpose if known.

## 3. Remove Russian clichés and bureaucratic phrasing

Edit phrases in context rather than using a word blacklist. Common replacements:

| Heavy or empty wording | More direct wording |
| --- | --- |
| «В современном стремительно развивающемся мире…» | Start with the subject and specific problem |
| «Осуществляется проведение анализа данных» | «Данные анализируются», or name the actor |
| «Производится сохранение результата» | «Программа сохраняет результат» |
| «С целью обеспечения возможности…» | «Чтобы…» |
| «В силу того факта, что…» | «Поскольку…» |
| «Следует особо отметить, что…» | Remove the preamble and keep the statement |
| «Данный подход позволяет обеспечить…» | Name the approach and explain its action |

Words such as «комплексный», «эффективный», «инновационный», «оптимальный»,
«экосистема» and «парадигма» need a meaning check, not automatic removal.
«Экосистема Python» and «парадигма программирования» can be accurate terms.
Preserve justified efficiency comparisons and explicit optimality criteria.

## 4. Fix grammar that obscures meaning

- Unpack verbal-noun chains: «реализация механизма обеспечения проверки» usually
  means «проверка» or «модуль проверяет».
- Name the actor when known and relevant: «сервер проверяет токен». Impersonal
  «получено 120 записей» is appropriate when the result matters; do not invent an actor.
- Check tails such as «подчёркивая значимость», «демонстрируя потенциал» and
  «способствуя развитию». Remove empty judgments; preserve proven causal links.
  Correct adverbial participles referring to the wrong subject.
- Avoid repeated «не просто X, а Y» and «не только X, но и Y» constructions.
  State the property directly. Keep contrasts distinguishing real options or limits.
- Do not vary technical-object names for variety. «Запрос», «команда» and
  «сообщение» can refer to different entities.
- Remove a third item if it duplicates the first two. Do not remove three independent
  results merely because there are three.
- Check «от X до Y»: endpoints must define a clear range or sequence. Otherwise list
  the objects directly.

Russian does not require constant «является». «Сервис представляет собой компонент,
осуществляющий проверку» can often become «Сервис проверяет…». Preserve necessary
definitions and the object's actual role.

## 5. Make sentences readable

Split overloaded sentences, combine choppy fragments and remove repeated openings.
Sentence length follows the thought; do not impose short-sentence quotas. The text
should sound natural when explaining the work to a teacher while remaining written
academic prose.

Remove decorative emoji, bolding of every other term and lists such as
«**Надёжность:** надёжность повышается». Preserve useful explanations. Do not turn
an effective comparison into a continuous paragraph merely to eliminate lists.

Follow Russian heading capitalization and use «ёлочки» quotation marks. Correct
typography is not poor writing. Follow the shared core's em-dash rule for academic
work: restructure sentences instead of mechanically replacing dashes with hyphens.
Do not import English dash-frequency conventions into Russian.

## 6. Remove filler; retain justified caution

Remove «важно отметить», «как уже было сказано выше» and «в заключение хотелось бы
отметить» when they add nothing. Remove «вот исправленный вариант», «надеюсь, это
поможет», direct user addresses and assistant service messages from the final report.

Do not strengthen conclusions for a confident tone. Do not turn «Может снизить
задержку» into «снижает задержку» without verification. Preserve assumptions,
sampling limits, measurement errors, negative results and the distinction between
correlation and causation.

«Эксперты считают», «исследования показывают» and «общепринято» need a specific
source when supporting a conclusion. Use an already verified source; otherwise
notify the author that verification is needed. Do not invent publications, dates,
interviews or quotations, or silently remove required substantiation.

## 7. Restore actual connections between ideas

Check repetition of «кроме того», «более того», «таким образом» and «следовательно».
Keep a connector only when it accurately expresses addition, contrast, cause or
conclusion. Do not cycle substitutions of «таким образом» and «следовательно».

Before: «Более того, повторы удалены. Таким образом, построена диаграмма».

After: «После удаления повторов построена диаграмма».

Sequence does not prove causation. Explain the reason for removing duplicates from
the actual materials if that reason matters.

## 8. Show authorial thought through decisions

Academic independence appears through selection reasons, interpretation and honest
limits. Preserve why a method was chosen, what limits the conclusion and the actual
result. Do not add emotions, humor, slang, personal memories or deliberate sloppiness
for «живости».

First person is acceptable when allowed by the genre and formatting conventions;
do not force «я» or «мы». Do not attribute experience, observations or experiments
absent from the source materials.

Before: «Полученные результаты наглядно демонстрируют огромный потенциал выбранного подхода и открывают широкие перспективы дальнейших исследований».

After, only when supported: «Метод разделил выборку на два кластера. Их устойчивость к изменению параметров не проверялась».

## Final verification and delivery

Reread and compare with the source: preserve required results, conditions, arguments
and references; introduce no new facts or stronger claims. Check phrases that fit
any subject after replacing a few nouns. Make them specific using the materials or
remove them if they add nothing.

For rewriting requests, deliver the complete corrected passage or save the requested
file. Briefly report substantive edits and unresolved questions to the user. Do not
add a «Что изменено» section to the submitted report. A «Было / Стало / Причина»
table is for useful comparison, not a mandatory step after every edit.

For review-only requests, identify the actual passage, problem and possible
replacement. Combine overlapping comments on one phrase. Do not claim expression
frequencies without checking or treat a correct word as inherently wrong. Explain
the harm: repetition, imprecision, unsupported inference or difficult reading.
