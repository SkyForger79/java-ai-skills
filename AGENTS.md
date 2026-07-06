# AGENTS.md

This file is the operating guide for agents working in this repository. Keep it
focused on the harness assets stored here; detailed runtime decisions for
`poc-gmmc-agent` belong in the target project's specs, code, tests, and
`AGENTS.md`.

## Project Frame

`java-ai-skills` packages reusable agent assets for Java/Spring/RAG/regulated AI
engineering:

- Codex-style skills under `skills/`;
- Qwen Code CLI project assets under `qwen/poc-gmmc-agent/`;
- a compact Qwen subagent team for continuing development of `poc-gmmc-agent`.

The primary local target checkout is:

```text
/Users/skyforger/Documents/poc-gmmc-agent
```

Treat that checkout as the runtime source of truth when a harness change depends
on current application behavior. This repository is the distribution and
authoring surface for skills and Qwen assets; it is not the runtime application.

## Source Of Truth

For this repository:

1. Current files in this repository.
2. `README.md`.
3. Skill instructions in `skills/*/SKILL.md` and their referenced files.
4. Qwen pack instructions in `qwen/poc-gmmc-agent/QWEN.md`,
   `qwen/poc-gmmc-agent/agents/*.md`, and
   `qwen/poc-gmmc-agent/subagent-handoff/TEMPLATE.md`.

For `poc-gmmc-agent` behavior:

1. Current code and executable tests in `/Users/skyforger/Documents/poc-gmmc-agent`.
2. Target project specs, especially `docs/specs/README.md`,
   `docs/specs/sdd-flow.md`, and relevant spec deltas.
3. Target project `README.md`, `AGENTS.md`, and installed `QWEN.md`.
4. Target project architecture, brief, and planning docs as background.

If this repository's harness guidance conflicts with the target project's
current code, tests, specs, or `AGENTS.md`, treat it as a finding and update the
harness to match the accepted target-project contract.

## Repository Layout

```text
skills/
  <skill-name>/SKILL.md
  <skill-name>/references/
  <skill-name>/scripts/

qwen/poc-gmmc-agent/
  QWEN.md
  README.md
  agents/
  subagent-handoff/TEMPLATE.md
```

Do not commit local operating artifacts such as `.serena/`, `.worktree/`, or
`.DS_Store`.

Prompt-engineering skills are part of the project skill set because the
`rag-llm-prompt-specialist` role owns prompt templates, structured outputs,
golden tests, malformed-output fallbacks, and prompt safety review.

## Code Analysis Tooling

For Qwen workflow guidance that depends on source-code navigation, use
`code-index-mcp` launched through UV:

```toml
[mcp_servers.code-index]
type = "stdio"
command = "uvx"
args = [
  "code-index-mcp",
  "--project-path",
  "/Users/skyforger/Documents/poc-gmmc-agent"
]
```

Serena is unavailable for `poc-gmmc-agent`. Do not author new Qwen instructions
that require Serena skills, Serena MCP tools, or `.serena/` project state. If an
imported skill still contains Serena-specific navigation references, keep Qwen
assets explicit that `code-index-mcp`, `rg`, source reads, and executable tests
are the supported path.

Expected code-index usage in Qwen assets:

- confirm or set the active project path before relying on indexed data;
- use `find_files` and `search_code_advanced` for targeted discovery;
- run `build_deep_index` before class, method, or reference analysis;
- use `get_file_summary` for structure after deep indexing;
- run `refresh_index` after branch switches, large edits, or stale results.

## Context Bootstrap

Start each non-trivial task with:

```bash
git status --short --branch
```

Then use the smallest context that can answer the task:

- read `README.md` before changing install or repository-level guidance;
- read the relevant `skills/<name>/SKILL.md` before changing a skill;
- read only directly referenced files under `references/` or `scripts/` that the
  selected skill needs;
- read `qwen/poc-gmmc-agent/QWEN.md`, the affected subagent definition, and the
  handoff template before changing Qwen assets;
- inspect `/Users/skyforger/Documents/poc-gmmc-agent/AGENTS.md` and relevant
  target specs before changing rules that affect runtime development.

Prefer `rg` and `rg --files` for discovery. Use broad whole-file reads only for
small docs or selected instruction files where full context matters.

## Skill Authoring Rules

Each skill must keep a valid `SKILL.md` with YAML frontmatter containing at least
`name` and `description`. The description should say when to use the skill, not
just what the skill is.

Keep skills pragmatic and project-compatible:

- use Java/Spring examples that fit the target project's Gradle/Spring Boot
  stack unless a skill is intentionally generic;
- keep optional technologies explicit rather than implied defaults;
- put long reference material under `references/` and link it from `SKILL.md`;
- put reusable automation under `scripts/` instead of embedding large scripts in
  prose;
- avoid duplicating target-project specs inside a skill. Link or summarize the
  boundary, then defer to the current target spec.

When changing imported or adapted skills, preserve the local intent: these assets
exist to support regulated Java agent development in `poc-gmmc-agent`, not to
provide a generic Spring cookbook.

For common prompt-engineering skills, keep their generic reusable guidance, but
make project-level usage constraints explicit in Qwen assets: prompt examples
must be translated to Spring AI/GigaChat and the target project's prompt pack
before implementation.

## Qwen Code CLI Harness

The Qwen pack is project-specific to `poc-gmmc-agent`.

`qwen/poc-gmmc-agent/QWEN.md` is the shared operating guide for Qwen Code CLI
sessions in the target project. It should complement, not replace, the target
project's `AGENTS.md`.

Project-level subagents live in `qwen/poc-gmmc-agent/agents/` and are installed
to the target checkout as `.qwen/agents/*.md`. Keep the team compact:

- `principal-architect` owns architecture briefs, specs, and decisions;
- `spring-runtime-implementer` owns focused Java/Spring implementation after a
  brief exists;
- `rag-llm-prompt-specialist` owns RAG, prompts, structured outputs, and golden
  tests;
- `regulated-flow-reviewer` owns regulated-flow, PII, HITL, handoff, final
  action, and RAG-evidence review;
- `verification-release-owner` owns verification evidence and PR readiness.

Do not weaken these target-project invariants in Qwen assets:

- Java routing and policy own graph branches, tools, final actions, and handoff
  boundaries;
- the model must not freely choose product domains, tools, RAG sources, HITL
  outcomes, or final actions;
- Router handoff is summary-only;
- raw dialogue, PII, credentials, hidden prompts, request hashes, and internal
  policy must not leak to Router, CRM, traces, logs, or public responses;
- RAG no-answer is metadata, not evidence;
- live LLM/RAG behavior is not sufficient proof without deterministic tests.

## Syncing Assets To The Target Checkout

Use this repository as the authoring source. Before copying assets into the
target checkout, check for local target changes:

```bash
TARGET=/Users/skyforger/Documents/poc-gmmc-agent
git -C "$TARGET" status --short --branch
```

Install or refresh the Qwen pack with:

```bash
TARGET=/Users/skyforger/Documents/poc-gmmc-agent

cp qwen/poc-gmmc-agent/QWEN.md "$TARGET/QWEN.md"
mkdir -p "$TARGET/.qwen/agents"
cp qwen/poc-gmmc-agent/agents/*.md "$TARGET/.qwen/agents/"
mkdir -p "$TARGET/docs/planning/subagent-handoff"
cp qwen/poc-gmmc-agent/subagent-handoff/TEMPLATE.md \
  "$TARGET/docs/planning/subagent-handoff/TEMPLATE.md"
```

Install or refresh project-local skills only when explicitly requested, and do
not overwrite target-local edits blindly. Compare first:

```bash
TARGET=/Users/skyforger/Documents/poc-gmmc-agent
diff -ru skills "$TARGET/.agents/skills" || true
```

If a task requires changing the target project itself, follow the target
project's `AGENTS.md`: use a dedicated branch/worktree, update specs before
runtime contract changes, run the relevant Gradle tests, and deliver through a
scoped PR.

## Verification

For repository-only changes, run focused structural checks:

```bash
git status --short --branch
find skills -name SKILL.md | sort
find qwen/poc-gmmc-agent -type f | sort
```

For skill changes, verify each changed `SKILL.md` has frontmatter and that every
referenced local file exists.

For Qwen pack changes, verify the target install shape:

```bash
test -f qwen/poc-gmmc-agent/QWEN.md
test -f qwen/poc-gmmc-agent/subagent-handoff/TEMPLATE.md
find qwen/poc-gmmc-agent/agents -name '*.md' | sort
```

For documentation changes that describe code-index behavior, verify the Qwen
pack still contains the required tool references:

```bash
rg "code-index-mcp|uvx|build_deep_index|search_code_advanced|refresh_index" \
  README.md AGENTS.md qwen/poc-gmmc-agent
```

When changes are copied into `/Users/skyforger/Documents/poc-gmmc-agent`, run
the target project's relevant verification there and report both source-repo and
target-checkout status.

## Git Discipline

Keep commits scoped by asset type when practical:

- skills-only changes;
- Qwen pack changes;
- repository documentation or install guidance.

Do not stage `.serena/`, `.worktree/`, `.DS_Store`, generated caches, or target
project files unless the task explicitly asks to modify them. If the target
checkout has unrelated local changes, leave them alone and report only the files
you touched.
