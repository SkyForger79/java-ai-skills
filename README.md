# Java AI Skills And Qwen Agents

Reusable Codex skills and Qwen Code CLI subagent assets for Java, Spring Boot,
RAG, LLM, and regulated AI-agent engineering.

## Repository Role

This repository is the authoring and distribution surface for reusable agent
assets. It is not the runtime application.

Primary target project:

```text
/Users/skyforger/Documents/poc-gmmc-agent
```

Use this repository to maintain:

- Codex-compatible skills under `skills/`;
- the Qwen Code CLI operating guide under `qwen/poc-gmmc-agent/QWEN.md`;
- project-level Qwen subagents under `qwen/poc-gmmc-agent/agents/`;
- the durable Qwen handoff template under
  `qwen/poc-gmmc-agent/subagent-handoff/TEMPLATE.md`.

Runtime behavior, contracts, and test evidence belong to the target project.
When guidance here conflicts with current target code, specs, or tests, update
the harness guidance or the target specs before continuing implementation.

## Skills

| Skill | Source | Use |
|---|---|---|
| `springboot-tdd` | `poc-gmmc-agent` `master` | Test-driven Spring Boot feature work, bug fixes, and refactors. |
| `springboot-verification` | `poc-gmmc-agent` `master` | Spring Boot build, test, security, and release verification loops. |
| `java-coding-standards` | `poc-gmmc-agent` `master` | Java coding conventions for Spring Boot and related services. |
| `springboot-patterns` | `poc-gmmc-agent` `master` | Routine Spring Boot REST, service, config, and data-access patterns. |
| `spring-boot-engineer` | `poc-gmmc-agent` `master` | Deeper Spring Boot engineering for cross-layer backend work. |
| `clean-architecture` | `poc-gmmc-agent` `master` | Clean/Hexagonal Architecture and DDD boundaries in Java/Spring. |
| `jpa-patterns` | `poc-gmmc-agent` `master` | JPA/Hibernate entities, queries, transactions, indexes, and auditing. |
| `springboot-security` | `poc-gmmc-agent` `master` | Spring Security, validation, secrets, headers, rate limits, and dependency security. |
| `rag-architect` | `poc-gmmc-agent` `master` | RAG architecture, retrieval quality, vector stores, chunking, and evals. |
| `langfuse` | `poc-gmmc-agent` `master` | Langfuse trace, session, prompt, dataset, and eval debugging. |
| `prompt-engineering-patterns` | local common skill | Production prompt design, structured outputs, few-shot patterns, prompt optimization, and template systems. |
| `ai-prompt-engineering-safety-review` | local common skill | Safety, bias, privacy, prompt-injection, and effectiveness review for prompt changes. |
| `acquire-codebase-knowledge` | local `poc-gmmc-agent` checkout | Codebase discovery and onboarding documentation workflow. |
| `architecture-patterns` | local `poc-gmmc-agent` checkout | Pragmatic Java/Spring/Spring AI architecture boundary guidance. |

## Install

Install a skill from this repository by passing its path to the Codex skill installer.

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo SkyForger79/java-ai-skills \
  --path skills/springboot-tdd
```

Multiple skills can be installed in one command by repeating `--path`.

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo SkyForger79/java-ai-skills \
  --path skills/springboot-tdd \
  --path skills/springboot-verification \
  --path skills/java-coding-standards
```

Install the full project skill set with:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo SkyForger79/java-ai-skills \
  --path skills/springboot-tdd \
  --path skills/springboot-verification \
  --path skills/java-coding-standards \
  --path skills/springboot-patterns \
  --path skills/spring-boot-engineer \
  --path skills/clean-architecture \
  --path skills/jpa-patterns \
  --path skills/springboot-security \
  --path skills/rag-architect \
  --path skills/langfuse \
  --path skills/prompt-engineering-patterns \
  --path skills/ai-prompt-engineering-safety-review \
  --path skills/acquire-codebase-knowledge \
  --path skills/architecture-patterns
```

## Qwen Code CLI Assets

This repository also includes a project-specific Qwen Code CLI subagent pack for
`poc-gmmc-agent`:

```text
qwen/poc-gmmc-agent/
├── QWEN.md
├── agents/
│   ├── principal-architect.md
│   ├── spring-runtime-implementer.md
│   ├── rag-llm-prompt-specialist.md
│   ├── regulated-flow-reviewer.md
│   └── verification-release-owner.md
└── subagent-handoff/
    └── TEMPLATE.md
```

Use the pack by copying files into a `poc-gmmc-agent` checkout:

```bash
cp qwen/poc-gmmc-agent/QWEN.md /path/to/poc-gmmc-agent/QWEN.md
mkdir -p /path/to/poc-gmmc-agent/.qwen/agents
cp qwen/poc-gmmc-agent/agents/*.md /path/to/poc-gmmc-agent/.qwen/agents/
mkdir -p /path/to/poc-gmmc-agent/docs/planning/subagent-handoff
cp qwen/poc-gmmc-agent/subagent-handoff/TEMPLATE.md \
  /path/to/poc-gmmc-agent/docs/planning/subagent-handoff/TEMPLATE.md
```

Qwen Code discovers project-level subagents from `.qwen/agents/`. The included
`QWEN.md` defines the shared project operating guide, and the handoff template is
used for durable per-task pipeline records.

## Code Analysis MCP

Qwen agents for `poc-gmmc-agent` should use `code-index-mcp`, launched through
UV, for code discovery and symbol navigation. Serena is unavailable for this
project and must not be used in Qwen workflow instructions.

Recommended Qwen/Codex MCP configuration:

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

Use `find_files` and `search_code_advanced` for targeted discovery,
`build_deep_index` for class/method-level analysis, `get_file_summary` for file
structure after deep indexing, and `refresh_index` after branch switches or
large edits. Indexed results are navigation evidence; behavioral claims still
need source reads and executable tests in the target checkout.

## Maintenance Checks

Before committing repository-only changes, run focused structural checks:

```bash
git status --short --branch
find skills -name SKILL.md | sort
find qwen/poc-gmmc-agent -type f | sort
git diff --check
```

For changed skills, validate each updated skill directory with the Codex skill
validator:

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  skills/<skill-name>
```
