# Qwen Code CLI Pack For `poc-gmmc-agent`

This pack contains project-specific Qwen Code CLI assets for running a compact
five-role subagent pipeline in `poc-gmmc-agent`.

Target checkout used by this pack:

```text
/Users/skyforger/Documents/poc-gmmc-agent
```

## Contents

- `QWEN.md` - project operating guide for Qwen Code CLI sessions.
- `agents/*.md` - project-level Qwen subagent definitions.
- `skills/answer-codebase-questions/` - focused, evidence-backed answers about
  current project code, logic, configuration, tests, and architecture.
- `skills/canary-token-prompt-guard/` - project-level Qwen skill for canary
  token placement in runtime prompt payloads.
- `subagent-handoff/TEMPLATE.md` - durable task handoff template.

## Prerequisites

- Qwen Code CLI project subagents enabled for the target checkout.
- UV available on the machine so Qwen/Codex can launch `code-index-mcp` through
  `uvx`.
- The target project's current `AGENTS.md`, specs, code, and tests available at
  the target checkout path.

Serena is not available for this project. Do not configure Qwen agents to depend
on Serena skills, Serena MCP tools, or `.serena/` project state.

## Install Into A Project Checkout

```bash
cp qwen/poc-gmmc-agent/QWEN.md /path/to/poc-gmmc-agent/QWEN.md
mkdir -p /path/to/poc-gmmc-agent/.qwen/agents
cp qwen/poc-gmmc-agent/agents/*.md /path/to/poc-gmmc-agent/.qwen/agents/
mkdir -p /path/to/poc-gmmc-agent/.qwen/skills
cp -R qwen/poc-gmmc-agent/skills/. /path/to/poc-gmmc-agent/.qwen/skills/
mkdir -p /path/to/poc-gmmc-agent/docs/planning/subagent-handoff
cp qwen/poc-gmmc-agent/subagent-handoff/TEMPLATE.md \
  /path/to/poc-gmmc-agent/docs/planning/subagent-handoff/TEMPLATE.md
```

Qwen Code CLI can list and manage project-level subagents with `/agents` and
`/agents manage` after the files are copied into `.qwen/agents/`.

Project-level skills are discovered from `.qwen/skills/<skill-name>/SKILL.md`.
`answer-codebase-questions` should be used for focused questions about current
code, behavior, configuration, tests, integrations, or architecture. It answers
from concrete source evidence and may save findings under
`docs/planning/investigations/` when explicitly requested.
`canary-token-prompt-guard` should be used for prompt cards, prompt renderers,
GigaChat/GigaChat Ultra prompt payloads, few-shot boundaries, and canary-token
placement reviews.

## Code Analysis MCP

Merge this project-scoped entry into `.qwen/settings.json`:

```json
{
  "mcpServers": {
    "code-index": {
      "command": "uvx",
      "args": [
        "code-index-mcp",
        "--project-path",
        "/Users/skyforger/Documents/poc-gmmc-agent"
      ]
    }
  }
}
```

Alternatively, run `qwen mcp add --scope project --transport stdio code-index
uvx code-index-mcp --project-path /Users/skyforger/Documents/poc-gmmc-agent`
from the target project root.

If the MCP server starts without a project path, call `set_project_path` with the
target checkout path before using indexed results.

Typical workflow:

1. Confirm the active project path with `get_settings_info`.
2. Use `find_files` and `search_code_advanced` for discovery.
3. Run `build_deep_index` before class/method-level analysis or reference
   tracing.
4. Use `get_file_summary` when file structure matters.
5. Run `refresh_index` after branch switches, broad edits, or stale results.

The index is a navigation aid. Qwen agents must still verify behavioral claims
against source files and the relevant Gradle or integration tests.

## Roles

- `principal-architect` - architecture, specs, trade-offs, and implementation briefs.
- `spring-runtime-implementer` - Java/Spring/LangGraph4j implementation.
- `rag-llm-prompt-specialist` - RAG, prompts, structured outputs, and golden tests.
- `regulated-flow-reviewer` - PII, compliance, handoff, final-action, and RAG evidence review.
- `verification-release-owner` - diff scope, tests, release readiness, and PR evidence.

## Skill Routing

The subagent descriptions reference the project skills they should apply:

- `principal-architect`: architecture, clean architecture, codebase discovery,
  RAG architecture, Spring engineering, and Spring security skills.
- `spring-runtime-implementer`: Spring TDD, Java standards, Spring patterns,
  clean architecture, JPA, security, and verification skills.
- `rag-llm-prompt-specialist`: RAG architecture, prompt-engineering patterns,
  prompt safety review, canary-token prompt guard, Langfuse diagnostics, and
  Java test guidance.
- `regulated-flow-reviewer`: Spring security, prompt safety review, RAG
  evidence boundaries, canary-token forbidden-zone review, architecture review,
  and Langfuse diagnostics.
- `verification-release-owner`: Spring verification, Spring TDD, Java
  standards, security, RAG, prompt, and Langfuse evidence skills.

Project-level Qwen skills:

- `answer-codebase-questions`: focused code, behavior, configuration, test, and
  architecture investigation with source evidence and optional durable notes.
- `canary-token-prompt-guard`: prompt canary-token placement, validation, and
  forbidden-zone review for runtime prompt payloads.
