---
name: architecture-patterns
description: Use when designing or refactoring Java/Spring/Spring Boot/Spring AI backend architecture, especially Clean/Hexagonal/Onion Architecture, DDD bounded contexts, dependency cycles, transaction boundaries, Spring Boot testability, RAG/tool boundaries, or AI-agent runtime modules.
---

# Architecture Patterns

Design Java/Spring backend modules with explicit dependency direction, test
seams, and framework boundaries. Choose the smallest structure that protects
domain rules and makes behavior testable.

## Operating Rules

- Start from current code, tests, and project specs before proposing structure.
- Keep domain concepts framework-free where practical: no JPA, HTTP DTOs,
  Spring AI prompts, or provider clients inside domain objects.
- Put Spring at the edges: API, persistence, configuration, messaging, REST
  clients, AI adapters, and observability.
- Let application services own orchestration, transactions, policy gates, and
  calls to ports.
- Treat LLMs and RAG as infrastructure adapters, not domain authority or free
  tool selectors.

## Architecture Workflow

1. Identify the bounded context, module, or use case.
2. Draw dependency direction: `api -> application -> domain` and
   `infrastructure -> application/domain ports`.
3. Define ports only at volatility boundaries: persistence, external HTTP,
   brokers, clock/id generation, AI models, vector stores, tools, and policy.
4. Choose proof first: plain JUnit for domain, fake adapters for use cases,
   Spring slices for adapters, full context tests only for wiring.
5. Add the smallest boundary that works. Do not create Clean Architecture
   folders mechanically.

## Reference Routing

- For package structure, ports/adapters, Java records/value objects, REST/JPA
  adapters, and DDD examples:
  [`references/java-spring-architecture.md`](references/java-spring-architecture.md).
- For Spring Boot configuration, validation, transactions, testing,
  observability, security, and AOT/native-readiness:
  [`references/spring-boot-practices.md`](references/spring-boot-practices.md).
- For Spring AI ChatClient, structured output, tool calling, RAG, memory,
  prompt boundaries, and deterministic AI tests:
  [`references/spring-ai-practices.md`](references/spring-ai-practices.md).
- For review/debug scenarios, dependency-cycle smells, and acceptance checks:
  [`references/review-checklist.md`](references/review-checklist.md).

## Quick Decisions

| Situation | Prefer |
|---|---|
| Business invariant or calculation | Domain entity/value object/domain service |
| User-action orchestration | Application service/use case |
| HTTP mapping | Controller + DTO mapper |
| Database access | Repository port + Spring Data/JPA adapter |
| External service call | Port + `RestClient`/`WebClient` adapter |
| Model call or RAG query | AI/RAG port + Spring AI adapter |
| Cross-cutting policy | Explicit application-layer guard/service |
| Transaction boundary | Application service method |
| Domain-rule test | Plain JUnit, no Spring context |
| Controller test | `@WebMvcTest` or focused MVC test |
| Persistence test | `@DataJpaTest` or repository integration test |
| REST client test | `@RestClientTest` or mock server |
| AI test | Stubbed model/client plus golden and malformed-output cases |

## Common Mistakes

- Controllers, repositories, or prompt builders own business decisions.
- Ports exist for every class rather than unstable/external seams.
- `@Transactional` is private, self-invoked, or wraps slow external calls.
- Live models, vector stores, or real HTTP services are the only proof.
- Raw dialogue, PII, credentials, hidden prompts, or retrieved text leak into
  traces, logs, tool calls, or handoff summaries.
