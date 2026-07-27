# Qwen Codebase Question Skill Design

## Goal

Add a project-specific Qwen Code CLI skill that helps developers, analysts,
DevOps engineers, and architects quickly answer questions about
`poc-gmmc-agent` code, behavior, and architecture.

## Scope

The skill uses question-driven investigation instead of building a complete
repository map. It starts with the smallest relevant context, uses
`code-index-mcp` and targeted source reads, and verifies behavioral claims
against source code and tests. For logic and architecture questions, it also
checks the relevant current specs and reports code/spec divergence.

If `code-index-mcp` is unavailable, the Qwen workflow falls back to `rg` and
targeted reads, never Serena. A divergence requiring an architecture decision
is returned as an `Architecture Finding`; the workflow stops without dispatching
`principal-architect` or editing specs/docs until the user asks to continue.

The skill does not edit implementation code. It explains the current state and
provides recommendations only when explicitly requested. On request, it may
save findings under:

```text
docs/planning/investigations/<YYYY-MM-DD-topic>.md
```

## Answer Contract

Default answers contain:

1. A direct answer.
2. A concise explanation of the execution or dependency path.
3. Evidence using concrete `path:line` references and relevant tests.
4. Gaps, uncertainty, or spec/code divergence when found.

Facts, evidence-backed inferences, and unverified assumptions remain visibly
separate. Recommendations are omitted unless requested.

## Integration

The skill lives at:

```text
qwen/poc-gmmc-agent/skills/answer-codebase-questions/SKILL.md
```

The root README, Qwen pack README, and `qwen/poc-gmmc-agent/QWEN.md` describe
its triggers, installation, evidence rules, and optional saved-artifact path.
It remains distinct from `acquire-codebase-knowledge`, which is intended for
full repository onboarding and durable codebase documentation.

## Verification

Verify skill discovery and behavior with focused scenarios covering a code-flow
question, an architecture question with a possible spec mismatch, and a request
to save findings without changing implementation files. Run structural checks,
frontmatter validation, link/path checks, and `git diff --check`.
