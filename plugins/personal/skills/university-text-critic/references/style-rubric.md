# Applying shared criteria and analyzing examples

## What to check

Normative criteria are in the shared `report-core.md` linked by SKILL.md. Do not
create a separate critic standard. Write comments in Russian, in plain complete
sentences; identify the specific violated assignment/core requirement.

Review final work only. Do not treat a source draft's verbosity as a final-text
defect. If supplied for comparison, verify preservation of substantive decisions,
not rejected alternatives or conversation history.

Check whether assigned sections are preserved; without prescribed sections, assess
logical grouping. Do not demand your preferred structure when the author may choose.

Identify lost meaning, unmet requirements and contradictions first, then language
and Markdown issues. Separate mandatory fixes from cosmetic suggestions. Confident
wording is not evidence. SKILL.md defines inputs, review format and approval.

Unconfirmed currency/units alter meaning and require correction: `SUM(price)` without
currency metadata cannot be labeled `BRL`. If Word styles or the builder generate
caption words/numbers, manually written «Рисунок 1» or «1. Заголовок» also needs a fix
to prevent duplication. Correct em dashes `—` in authored prose under the explicit
core rule; preserve required quotations, code and externally assigned captions.

Check logic within the presented model. Select key conclusions and mentally test
whether they hold under directly relevant conditions and failures. Do not produce
a universal production checklist or suggest technologies. An honestly recorded
assumption/open question allowed by the assignment deserves at most an optional
suggestion, or no comment.

Example: the text claims «инфраструктура надёжна», then places the application and
only database on one node. Database failure stops the system but is not automatically
an academic error. If an agreed calculation meets assigned availability, the single
point of failure is explicit and conclusions are limited to the educational scenario,
the simplification is acceptable. Promised uninterrupted operation after database
failure or unqualified "proven reliability" is a contradiction: request a corrected
conclusion, not a particular technology.

## Analysis of supplied materials

Names and groups below are explicitly fictional examples. Never substitute local
personal profile values into them.

Original materials were in `university/examples`; they are not bundled or mandatory
resources. Two PDFs in `good` were accepted but rated about 6/10. They illustrate
minimum acceptability, not an ideal standard. This analysis supports applying the
criteria without original examples. For recalibration, ask the caller for actual
paths to readable copies.

**Практическая_1_Иванов_И_И_ИКБО-00-00**, sections «Суть работы» and «Выбранные показатели»:

- Useful: a short description of PortfolioPro's behavior, with criticism tied to
  pages and specific gaps. «Стек перечислен, но нет сравнения вариантов» is more
  useful than a generic architecture judgment.
- Do not copy: cumbersome measure names, the typo «провеёл», unfinished
  «нагрузочное тестирование с помощью». The claim «ни одна из них не предоставляет»
  requires evidence even in an accepted work.

**Практическая_2_Иванов_И_И_ИКБО-00-00**, payment-gateway EventStorming work:

- Useful: «Система мерчанта создаёт поручение, получает платёжную ссылку…»; explicit
  gateway/provider responsibility separation; tables of commands, events, invariants
  and unresolved questions; comparison with earlier work.
- Preserve important prohibitions and conditions: a successful payment cannot return
  to processing, and recovery requires a security check. Removing these changes the model.
- Improve carefully: repeated long names and identical table preambles. Preserve
  needed figure/table references. Dashes in mandatory captions are not grounds to
  reject the document.

**bad/pr1_firesru_chicago.ipynb**, Markdown cells only:

- Undesirable: each plot is explained using «показывает»; assignment requirements
  repeat; generic advice about what EDA should be closes the text. «в этой итерации…
  выводы будут добавляться» remains beside completed conclusions.
- Preserve numeric results, reasons for handling missing values, arrest-count versus
  arrest-probability distinctions and limits on conclusions. Do not call everything
  in `bad` bad or remove essential caveats.
- Analysis limit: the user did not separately explain placement in `bad`; these are
  editorial observations. Without the assignment, its mandatory quotations or
  educational blocks cannot be declared unnecessary.

PDFs were converted to Markdown before analysis. Some tables collapsed into lines
and columns during extraction: this is an extraction flaw, not evidence of poor
original formatting. This textual analysis did not check diagrams.

## Veil and figure example

Fictional storage-design report for a payment gateway, first version approved with
«текст плотный, сокращение не требуется». The author then cut about 20% of prose by
hand. These cuts are what the critic should have demanded:

- «Схемы, словарь, объёмы и индексы строит один скрипт, поэтому они не расходятся»,
  «допустимость связей проверена скриптом», «исходник: storage.drawio»: production
  history. Delete; the unverified-tool limit stays once in «Допущения и ограничения».
- «Классы выведены из двух агрегатов…», «основной и резервный провайдеры подтипами
  не стали…», «инварианты 1–9 перенесены из ПР2…»: non-decisions and retelling of
  the adjacent figure. Delete; the mapping table already records them.
- A whole table closing questions of an earlier work that the current assignment did
  not ask for, and a second secondary deviation from 3NF: optional material. Delete.
- Data-dictionary rows `id`, `created_at`, `updated_at` repeated in every table:
  replace with one sentence and merge same-typed fields.
- «девять прецедентов» → «9 прецедентов».

Figures in the same report: the sample in the assignment draws the storage schema
with numeric multiplicities, the report used crow's foot notation with an in-image
«Обозначения» legend; the other two figures carried explanatory footnotes inside
the image. Each is a `[диаграмма]` mandatory fix: redraw in the sample's notation and
move notes into text or delete them.

Do not overcorrect: the invariant table, normalization check and index rationale are
required by the assignment and stay even when long.

## Editing and decision examples

**Shorten:** «Следует отметить, что в рамках данной практической работы осуществляется рассмотрение процесса взаимодействия системы мерчанта с платёжным провайдером» → «Работа описывает взаимодействие системы мерчанта с платёжным провайдером».

**Preserve meaning:** «Сначала фиксируются типы полей, затем число заполненных и пропущенных значений» → «Проверены типы полей и пропуски». Changing tense is allowed only when the checks actually happened.

**Do not overedit:** «Уведомление с неверной подписью не меняет статус платежа» is already concise and precise. `APPROVE` if other requirements are satisfied; no shortening is needed.

**Reject:** «Шлюз списывает деньги» when the provider actually debits. `REVISE`: «Провайдер проводит платёж, шлюз получает результат». This is a substantive error, not cosmetic.
