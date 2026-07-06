# Qwen Code CLI Pack For `poc-gmmc-agent`

This pack contains project-specific Qwen Code CLI assets for running a compact
five-role subagent pipeline in `poc-gmmc-agent`.

## Contents

- `QWEN.md` - project operating guide for Qwen Code CLI sessions.
- `agents/*.md` - project-level Qwen subagent definitions.
- `subagent-handoff/TEMPLATE.md` - durable task handoff template.

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

## Roles

- `principal-architect` - architecture, specs, trade-offs, and implementation briefs.
- `spring-runtime-implementer` - Java/Spring/LangGraph4j implementation.
- `rag-llm-prompt-specialist` - RAG, prompts, structured outputs, and golden tests.
- `regulated-flow-reviewer` - PII, compliance, handoff, final-action, and RAG evidence review.
- `verification-release-owner` - diff scope, tests, release readiness, and PR evidence.
