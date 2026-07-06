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
mkdir -p /path/to/poc-gmmc-agent/docs/planning/subagent-handoff
cp qwen/poc-gmmc-agent/subagent-handoff/TEMPLATE.md \
  /path/to/poc-gmmc-agent/docs/planning/subagent-handoff/TEMPLATE.md
```

Qwen Code CLI can list and manage project-level subagents with `/agents` and
`/agents manage` after the files are copied into `.qwen/agents/`.

## Code Analysis MCP

Recommended MCP server configuration:

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
  prompt safety review, Langfuse diagnostics, and Java test guidance.
- `regulated-flow-reviewer`: Spring security, prompt safety review, RAG
  evidence boundaries, architecture review, and Langfuse diagnostics.
- `verification-release-owner`: Spring verification, Spring TDD, Java
  standards, security, RAG, prompt, and Langfuse evidence skills.
