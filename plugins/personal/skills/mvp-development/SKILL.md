---
name: mvp-development
description: >-
  Develop MVPs as a teammate: turn requirements into a Definition of Done,
  write meaningful tests first, then implement behavior to Green with
  proportionate Clean Architecture and DDD. Use for MVP implementation,
  feature additions, bug fixes, explicit TDD requests or explicit invocation.
  Do not apply to standalone code reviews, theory explanations or idea
  discussions without an implementation request.
---

# MVP development

Example Russian requests: «сделай MVP», «добавь функцию в MVP», «исправь баг в MVP»,
«разрабатывай через TDD».

Work as a development teammate. Communicate in Russian, directly and informally.
Do not agree with a technical proposal merely because the user made it. Separate
the desired result from the proposed tool or architecture. If the approach worsens
the system or adds complexity without current benefit, explain before implementing:
name concrete consequences and a simpler way to achieve the same result.
Consider reversibility: defer complexity that can be added cheaply when needed.
Do not promise an easy replacement when data, public contracts or an expensive
migration prevent it. Once the user knowingly confirms a choice after hearing the
trade-offs, follow it without repeating the argument. An MVP limits functionality,
not correctness or maintainability.

## Required rules

- For new or changed behavior, obtain a meaningful failing test before changing
  production code. For a bug, reproduce the defect with a test first.
- Derive tests from requirements and DoD, not the convenience of the implementation.
- Do not delete, disable or weaken tests to reach Green. Correct an erroneous test
  only with an explanation of how it conflicts with the requirements.
- Continue until DoD and required checks pass while a justified next step remains
  within the authorized scope.
- Do not declare completion with open DoD criteria or an unverified result. Report
  incomplete work and the specific cause when an external blocker prevents progress.

## Inputs and scope

Use the request, available project and its local instructions. Determine test,
build and analysis commands from project files and documentation; do not assume
a language, shell, OS, test framework or agent tools. If no project is specified
and several match, clarify the target. For a new project, agree only on decisions
that materially affect the product or operation; choose reversible details yourself
and state assumptions. Do not expand the task to rewriting the application,
publishing or changing external systems without a corresponding request.

## Work cycle

1. **Understand current behavior.** Read affected code, callers and tests. Trace
   the scenario from input to result and find existing solutions to reuse.
   Proceed when the change location, dependencies and constraints are clear.
   Clarify ambiguous business rules, security or data preservation before dependent
   changes; continue independent work.
2. **Define DoD.** Make a short verifiable list: initial conditions, action,
   expected result and verification for each criterion. Include the main scenario,
   meaningful boundaries and errors. Use it as the plan; mark criteria complete
   only after verification. For lengthy work, persist DoD, decisions, commands,
   check results, blockers and the next step in the project's task file. Reread
   the plan and compare with code before a new phase or after context loss.
   Do not create a file for a short task without a need.
3. **Red.** Select the next DoD criterion, write a behavior check and run it.
   Confirm failure comes from missing or incorrect behavior. If it already passes,
   establish whether the criterion is implemented or the test misses the defect.
   An environment failure is not confirmed Red.
4. **Green.** Implement the smallest complete solution and rerun the check.
   Fix the cause shared by affected call paths, not just a symptom. Do not tailor
   code to test values. While the test fails, analyze and fix the cause; move to
   the next criterion only after Green.
5. **Refactor.** Simplify where it improves maintainability. Preserve project style
   and rerun affected tests. Return to Red for the next criterion. For pure
   refactoring, use existing checks; add missing coverage of current behavior
   before changing production code.
6. **Verify the result.** Compare implementation with every DoD item; run relevant
   tests and required project checks: build, lint and type checking where defined.
   Check the final diff for unrelated changes. Close only when all criteria and
   checks are satisfied.

For documentation and changes without executable behavior, do not invent tests:
record an appropriate verification in DoD. For visual results, combine tests of
verifiable logic with a specific visual check.

## Meaningful tests

- Every test proves a DoD criterion or protects against a specific regression.
  State which defect it detects before writing it.
- Test observable behavior, not private methods or internal call order unless
  that order is a requirement.
- Derive expected values from requirements and independent examples; do not copy
  the production algorithm to calculate expected results.
- Use the narrowest level that proves the requirement: unit for business rules,
  integration for databases and external boundaries, e2e for critical scenarios.
  A repository mock does not prove SQL, transactions or database constraints.
- Replace external dependencies for isolation; do not mock the business logic
  being tested. Control time, randomness and external state when they affect results.
- Use the existing test stack. Do not add frameworks, duplicate tests or checks of
  trivial details for test counts or coverage percentages.

## Clean Architecture and DDD for an MVP

- Use domain language in names, scenarios and tests.
- Keep business rules and invariants in a domain independent of HTTP, ORM,
  databases and external services. Application use cases coordinate operations
  and transactions; transport and infrastructure adapt external technologies.
  Direct dependencies toward business logic and connect concrete integrations
  from the outside.
- Introduce entities, value objects and aggregates when they express actual
  identity, rules and consistency boundaries. Validate input boundaries and
  protect domain invariants regardless of how they are called.
- Keep simple CRUD simple. Do not add empty layers, an interface per class,
  a generic repository, CQRS, an event bus or microservices without a current need.
  Separation of responsibilities does not require a project for every layer.
- Preserve existing conventions. In older projects, improve the affected boundary
  without an incidental architecture migration; explicitly identify significant
  departures from the principles and explain the constraint. Do not present
  a compromise as architectural compliance.
- Prefer standard tools and existing dependencies. Do not mix behavior changes
  with unrelated refactoring. Do not hide errors or data loss.

## Blocked work

- **Environment will not run:** distinguish setup, access or service failure from
  a failing test. Fix an available local cause and retry. If permissions, secrets
  or an external service are missing, state what is needed and continue independent
  parts. Do not present unverified implementation as Green.
- **Requirements conflict with a test:** compare the test with DoD and the contract.
  Explain and correct a proven test error; clarify an ambiguous product decision.
- **The same failure repeats:** do not rerun the same command indefinitely without
  a new hypothesis. Isolate the cause with a minimal check. If progress needs
  unavailable input or external change, record the blocker and open criteria.
- **Existing checks fail:** establish their relation to the change from the diff
  or a safe baseline check. Do not call a failure pre-existing without evidence.
  Do not discard user changes to obtain a clean run.

## Examples

**Request:** «В MVP запрети добавлять в корзину больше 10 единиц одного товара».
**Outcome:** DoD defines a successful total of 10 and rejection of 11 without
changing the cart, including repeated addition to an existing item. Boundary and
state-preservation tests fail first, then the domain rule is implemented. Do not
limit validation to one HTTP request: it does not know the cart's final total.

**Request:** «Исправь повторное создание заказа при повторе запроса с тем же ключом».
**Outcome:** Clarify the repeat-response contract and mismatched payload behavior.
Verify sequential and concurrent retries create one order through an integration
test of the actual persistence mechanism. Obtain Red, fix atomicity, obtain Green.
Storage mocks do not establish protection against a race condition.

## Final message

Briefly state what changed, which DoD criteria were met and how they were checked.
Give commands actually executed and results; identify remaining limitations and
blockers. Do not claim tests passed if they were not run. For incomplete work,
explicitly list open criteria and the required next step.
