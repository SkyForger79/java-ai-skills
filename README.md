# Java AI Skills

Reusable Codex skills for Java, Spring Boot, RAG, and AI-agent engineering.

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
