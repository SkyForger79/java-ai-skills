---
name: answer-codebase-questions
description: Use when developers, analysts, DevOps engineers, or architects ask how poc-gmmc-agent code, runtime logic, configuration, integrations, tests, or architecture currently work, including requests to locate an implementation, trace a flow, explain a decision, or compare code with current specs.
---

# Answer Codebase Questions

Answer focused questions about `poc-gmmc-agent` with the smallest evidence set
that supports the conclusion.

## Boundaries

- Use for code, behavior, configuration, integration, test, and architecture questions.
- Use `acquire-codebase-knowledge` instead for full repository mapping,
  onboarding, or `docs/codebase/` generation.
- Do not edit implementation code while answering a question.
- Explain the current state; recommend changes only when explicitly asked.
- Save an investigation under `docs/` only when explicitly requested.

## Evidence Order

1. Current source, configuration, deployment files, and executable tests.
2. Current `docs/specs/` for intended logic or architecture contracts.
3. `README.md`, `AGENTS.md`, and `QWEN.md` for project operating context.
4. `docs/architecture/` and `docs/brief/` as background.
5. Archived material only when a current source points to it or the user asks.

Code and tests define actual behavior; current specs define intended behavior.
Report disagreement as a finding.

## Fast Investigation

1. Scope the literal question as a code path, business rule,
   runtime/configuration path, or architecture boundary. Ask only when ambiguity
   would materially change the answer.
2. Confirm the active checkout and `code-index-mcp` project path. Start with
   `find_files` and `search_code_advanced`; use `rg` for docs, YAML, deployment,
   and exact text. If the index is unavailable, continue with `rg` and targeted
   reads; never substitute Serena in this Qwen project. Run `build_deep_index`
   for class/method/reference analysis, or architecture questions that depend on
   symbol relationships. Use `refresh_index` only for stale data.
3. Read the smallest relevant source slices and nearest tests. Trace entry point,
   decisions, adapters, and outcome. For framework behavior, verify runtime
   configuration, conditions, wiring, and proxies, not only annotations. For
   logic or architecture, inspect the relevant current spec.
4. Verify each important claim at a concrete `path:line`. Treat index results as
   navigation, not proof. Support negative claims with targeted repository
   searches and label them as inferences. Run existing focused tests when useful;
   do not create a temporary harness in read-only mode. Report coverage gaps.

## Answer Contract

Start with the direct answer. Add only the sections the question needs:

- **How it works** - the execution, dependency, state, or configuration path.
- **Evidence** - concrete source and test references in `path:line` form.
- **Gaps or findings** - missing proof, conflicting sources, or code/spec drift.

When certainty differs, distinguish facts, evidence-backed inferences, and
unknowns. For drift requiring an architecture decision, return and stop at:

```markdown
**Architecture Finding**
- Conflict: ...
- Evidence: ...
- Decision needed: ...
- Owner: `principal-architect`
```

Do not dispatch the role or edit specs/docs until the user asks to continue.

## Saving An Investigation

On explicit request, write:

```text
docs/planning/investigations/<YYYY-MM-DD-topic>.md
```

Include the question, answer, traced flow, evidence, findings/unknowns, and test
status. Keep the note descriptive and implementation-free.
