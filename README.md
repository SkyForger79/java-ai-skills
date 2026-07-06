# Java AI Skills And Qwen Agents

Reusable Codex skills and Qwen Code CLI subagent assets for Java, Spring Boot,
RAG, LLM, and regulated AI-agent engineering.

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
