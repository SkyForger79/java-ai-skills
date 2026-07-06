# QWEN.md

This file is the operating guide for Qwen Code CLI sessions in this repository.
It complements `AGENTS.md`; when the two differ, follow the stricter project
boundary and use current code, executable tests, and durable specs as the source
of truth.

## Project Frame

`poc-gmmc-agent` is a PoC for regulated financial product assistants. The
runtime is a bounded workflow agent, not an autonomous sales agent:

- an upstream Router selects one product-domain agent at session start;
- the selected product agent owns the session until completion, domain switch,
  HITL/policy boundary, or failure;
- Java routing and policies choose graph branches, tools, RAG mode, final
  action, compliance, and handoff behavior;
- the model must not freely choose tools, product domains, RAG sources, final
  actions, HITL outcomes, or Router handoff behavior;
- Router handoff is summary-only; raw dialogue stays in persistence/audit paths.

Developer-facing entry points are English. Product and architecture documents
are mostly Russian, with code identifiers preserved in English.

## Source-Of-Truth Order

1. Current code and executable tests.
2. Current durable specs: `docs/specs/README.md`, `docs/specs/sdd-flow.md`,
   `docs/specs/three-agent-template-solution-spec.md`,
   `docs/specs/agent-runtime-trace-fix-spec.md`,
   `docs/specs/llm-prompt-pack.md`, and relevant spec deltas.
3. `README.md`, `AGENTS.md`, and this file.
4. `docs/architecture/` and `docs/brief/` as background.
5. `docs/planning/subagent-handoff/*.md` as durable task history, not as a
   substitute for specs.
6. Historical raw notes, research, and archived plans under
   `docs/background-archive/`, only when explicitly needed.

If specs and code diverge, treat it as a finding. Either align code to the
accepted spec or update/create a spec delta before implementation continues.

## Bootstrap For Non-Trivial Tasks

Start with a narrow context pass:

1. Run `git status --short --branch`.
2. Read `README.md`, then use `docs/planning/context-index.md` and
   `docs/specs/README.md` as the docs map.
3. Read `docs/specs/sdd-flow.md` and the smallest relevant spec section.
4. Inspect nearest tests before editing implementation.
5. Do not use removed historical `docs/superpowers/` specs or plans as current
   requirements.

For Java code navigation, prefer targeted symbol/file reads over broad whole-file
reads. Behavioral claims still require the relevant Gradle or integration test
harness.

## Branch And Worktree Discipline

Do not edit `develop`, `master`, or `main` directly for new work. Use a dedicated
task branch and worktree under `.worktree/<task>` unless the user explicitly asks
for a different workflow.

Before editing in a task worktree, record and use its absolute root:

```bash
pwd
git rev-parse --show-toplevel
git status --short --branch
```

After the first patch, check both the task worktree and the main checkout:

```bash
git -C <task-worktree> status --short
git -C <main-checkout> status --short
```

All completed changes should go through a scoped PR. Stage only files touched for
the task. Do not push directly to `master`/`main`.

## Qwen Subagent Pipeline

Use one shared durable handoff artifact for each non-trivial Qwen pipeline task:

```text
docs/planning/subagent-handoff/<YYYY-MM-DD-task-slug>.md
```

Create it from `docs/planning/subagent-handoff/TEMPLATE.md`. The artifact stays
in the repository after PR merge as durable task history. It records execution
evidence, decisions, findings, reviews, and verification, but it does not replace
`docs/specs/` as the source of runtime contracts.

The main Qwen session owner remains the integration owner: it chooses scope,
creates the branch/worktree, assigns subagents, integrates findings, resolves
conflicts, runs fresh verification, stages scoped files, commits, pushes, and
opens/updates the PR.

## Subagent Team

Use a compact five-role team. Prefer the narrowest role that matches the task.

### `principal-architect`

Deep project architecture, SDD/spec decisions, trade-offs, and implementation
briefs. May edit specs/docs, but not implementation code.

May edit:

- `docs/specs/`
- `docs/architecture/`
- `docs/planning/`
- `QWEN.md`
- the current handoff artifact

Must not edit:

- `src/`
- `deploy/`
- Gradle/build/runtime configuration
- tests or runtime resources

Owns the Architecture Brief and resolves Architecture Findings.

### `spring-runtime-implementer`

Java/Spring Boot/LangGraph4j implementation after an Architecture Brief exists.

May edit only implementation files explicitly allowed by the brief, usually
`src/main/java/`, `src/test/java/`, and focused resources under
`src/main/resources/`.

Must not edit specs or architecture docs. If implementation requires a new or
changed contract, stop and raise an Architecture Finding for
`principal-architect`.

### `rag-llm-prompt-specialist`

RAG, FinTools KB, fake RAG tests, Spring AI `ChatClient`, prompts, structured
output, golden tests, malformed-output fallbacks, and no-answer behavior.

Must not move route/tool/final-action decisions from Java into the model, create
cross-product RAG calls, or treat RAG no-answer as pseudo-evidence. If prompt or
RAG work requires a contract change, stop and raise an Architecture Finding.

### `regulated-flow-reviewer`

Safety/compliance reviewer for PII, raw dialogue, HITL, Router/CRM handoff,
tracking/audit, final actions, recommendations/suitability, and RAG evidence
boundaries.

May edit only review notes, docs/checklists/PR notes, and the Regulated Flow
Review section of the handoff artifact. Must not edit implementation code.

### `verification-release-owner`

Verification and release-readiness reviewer. Checks diff scope, test evidence,
PR notes, skipped checks, and residual risks.

May edit only verification notes, docs/checklists/PR notes, and the Verification
Evidence section of the handoff artifact. Must not edit implementation code.

## Pipeline States

Use these states in the handoff artifact:

- `planning`
- `implementing`
- `blocked`
- `architecture-review`
- `regulated-review`
- `verifying`
- `ready-for-pr`
- `merged`

Normal flow:

1. `principal-architect` writes the Architecture Brief.
2. `spring-runtime-implementer` or `rag-llm-prompt-specialist` implements within
   the allowed scope.
3. Implementers stop and raise Architecture Findings when they discover missing
   contracts or spec/code mismatches.
4. `principal-architect` resolves findings and updates specs/docs or the brief.
5. `regulated-flow-reviewer` reviews regulated-flow boundaries.
6. `verification-release-owner` records verification evidence and PR readiness.
7. The main Qwen session owner performs final integration, commit, push, and PR.

## Runtime Boundaries

Preserve these constraints unless a new approved spec changes them:

- no binding quotes, execution, personalized recommendations, or suitability
  claims;
- no hidden prompt, raw context, credentials, internal policy, idempotency keys,
  bearer tokens, request hashes, or PII disclosure;
- no cross-product RAG calls from a product agent;
- `DOMAIN_SWITCH` returns control to Router instead of answering for another
  product domain;
- `ASSISTANT_CAPABILITIES`, clarification, and handoff branches do not call RAG;
- inbound upstream-assistant dialogue is continuity context only, never factual
  authority for recommendations or suitability claims;
- RAG no-answer is metadata, not evidence;
- traces and tracking use sanitized state snapshots, not raw dialogue or PII.

## Verification

Choose the proof before changing code. Use the smallest harness that can catch
the regression, then widen when the change crosses module boundaries.

Common commands:

```bash
./gradlew test
./gradlew test --tests "com.gemstone.gmmc.agent.runtime.nodes.*"
./gradlew test --tests "com.gemstone.gmmc.agent.it.*"
./gradlew test --tests "com.gemstone.gmmc.agent.it.postgres.*"
```

Java tests normally run with memory persistence, fake RAG, and disabled or
stubbed LLMs. Live LLM/RAG variability is not sufficient proof.
