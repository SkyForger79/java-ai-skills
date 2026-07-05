# Architecture Review Checklist

Use this reference for reviews, refactors, dependency-cycle fixes, and safety
checks after applying the skill.

## Boundary Questions

- What bounded context or use case owns this behavior?
- Which layer owns each decision: API mapping, orchestration, domain invariant,
  persistence, external service, AI/RAG, policy, or observability?
- Can the core behavior run in a plain unit test without Spring, a database, a
  network, or a live model?
- Are ports created only for real volatility or external boundaries?
- Are package names aligned with business capabilities rather than generic
  technical buckets only?
- If module boundaries matter, is there an enforceable check such as Spring
  Modulith `ApplicationModules.verify()`, ArchUnit, or build/import rules?

## Dependency Smells

| Smell | Fix |
|---|---|
| Domain imports Spring, JPA, HTTP, or Spring AI | Move annotation/client detail to adapter |
| Use case imports concrete repository/client | Introduce application port |
| Controller contains branching business rules | Extract use case or policy service |
| Repository publishes events or calls APIs | Move orchestration to application layer |
| JPA entity doubles as rich aggregate by accident | Split entity/domain or document the tradeoff |
| `@Transactional` private/self-invoked method | Move boundary to public Spring bean method |
| Live model/vector store needed for unit tests | Stub AI/RAG port and add focused adapter tests |
| Tool callback bypasses authorization/policy | Route through application service guard |
| Cross-module import reaches another module's internals | Add an architecture test or expose a named/public interface |

## Spring Boot Checks

- Configuration is bound through validated `@ConfigurationProperties`.
- Controllers use DTO validation and stable error mapping.
- REST clients have timeouts, base URL, authentication, error mapping, and tests.
- HTTP security rules are ordered from specific to broad and end deny-by-default.
- Database transactions are short and do not wrap slow external calls.
- Container-backed integration tests use Testcontainers/`@ServiceConnection` when
  real infrastructure behavior matters.
- Actuator/Micrometer/Observation data avoids high-cardinality or sensitive tags.
- Security has negative tests, not just happy-path authentication.
- `@SpringBootTest` is justified; otherwise use a smaller test slice.

## Spring AI Checks

- `ChatClient`, prompt templates, vector stores, and provider options live in
  AI/RAG adapters or configuration.
- Tool callbacks are narrow, validated, authorized, and idempotent when needed.
- Structured model output is validated before state changes.
- RAG evidence is source-scoped; no-answer is explicit.
- Memory is scoped and not used as factual authority.
- Tests cover malformed model output, prompt-injection attempts, denied tools,
  no retrieval result, and provider failure.
- Logs/traces never expose hidden prompts, raw dialogue, PII, secrets, or
  retrieved sensitive text.

## Acceptance Cases

Positive case:

- A use case can be tested with fake ports and no Spring context.
- Adapter tests prove mapping/wiring for persistence, HTTP, security, or AI.
- The package dependency direction is understandable from imports alone.

Negative/safety case:

- Invalid input is rejected before domain state changes.
- Unauthorized or wrong-tenant actions do not call downstream tools/services.
- Retrieval no-answer or malformed model output does not produce unsupported
  claims or side effects.

## Refactor Guardrails

- Do not move code only to satisfy a diagram.
- Do not introduce new frameworks because a pattern example mentions them.
- Do not split a small cohesive module into many empty layers.
- Do not hide business decisions in annotations, listeners, advisors, or
  generic utility classes.
- Keep migration steps small enough that tests can prove each boundary change.
