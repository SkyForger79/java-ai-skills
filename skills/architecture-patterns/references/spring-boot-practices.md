# Spring Boot Practices Reference

Use this reference when architecture choices touch Spring Boot configuration,
transactions, validation, tests, observability, security, or runtime packaging.

## Dependency Injection and Configuration

- Prefer constructor injection. Fields should be `final` where possible.
- Prefer `@ConfigurationProperties` with validation over scattered `@Value`.
- Use kebab-case property names; Spring Boot relaxed binding maps environment
  variables and property sources to Java fields.
- Use profiles/profile groups for environment-specific beans and configuration;
  avoid hard-coded `dev`/`prod` branches in services.
- Keep auto-configuration customizations in configuration packages, not inside
  domain or application services.
- Debug auto-configuration with the condition evaluation report, Actuator
  `conditions`, and `configprops` before guessing.

```java
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Positive;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.validation.annotation.Validated;

@Validated
@ConfigurationProperties(prefix = "orders.client")
public record OrdersClientProperties(
        @NotBlank String baseUrl,
        @Positive int connectTimeoutMillis,
        @Positive int readTimeoutMillis) {
}
```

Register properties via `@ConfigurationPropertiesScan` or
`@EnableConfigurationProperties` depending on local project style.

## Transactions

Put transaction boundaries around application use cases, not controllers,
repositories, or domain objects.

Checklist:

- `@Transactional` method is public and invoked through a Spring-managed bean.
- Query methods use `readOnly = true` when appropriate.
- External HTTP, broker, file, or model calls are outside long database
  transactions.
- Side effects that must survive retries use an outbox/idempotency boundary.
- Tests cover rollback, duplicate request, and side-effect replay cases when the
  workflow is stateful.

## Validation and API Errors

- Validate transport DTOs with `jakarta.validation`.
- Validate domain invariants inside constructors/factory methods even if the DTO
  already has annotations.
- Convert boundary exceptions to stable API errors using `@ControllerAdvice`.
- Use Spring Framework `ProblemDetail` when the service has an RFC 9457-style
  error contract.

## HTTP Clients

- Use `RestClient` for modern blocking MVC applications.
- Treat `RestTemplate` as legacy for new code; prefer `RestClient` unless the
  existing codebase standardizes on `RestTemplate`.
- Use `WebClient` when the service is reactive, needs streaming, or already
  operates on reactive types.
- Use Spring HTTP interfaces such as `@HttpExchange` when a typed declarative
  client improves adapter clarity and the project already accepts generated
  proxy clients.
- Hide clients behind ports for business workflows; do not scatter HTTP calls
  through use cases.
- Configure timeouts, authentication, base URLs, retry/circuit policy, and
  observability centrally.

## Testing Strategy

Choose the smallest Spring test that proves the behavior.

| Behavior | Harness |
|---|---|
| Entity/value-object invariants | Plain JUnit |
| Use case orchestration | Plain JUnit with fake ports |
| MVC mapping, validation, error advice | `@WebMvcTest` |
| JSON serialization only | Jackson tester or focused mapper test |
| Repository query/mapping | `@DataJpaTest` |
| REST client adapter | `@RestClientTest` + mock server |
| Configuration properties binding | `ApplicationContextRunner` or focused context |
| Security rules | MVC/security slice plus negative cases |
| Container-backed integration | Testcontainers with Boot `@ServiceConnection` |
| Full wiring | `@SpringBootTest`, reserved for integration confidence |

Good Spring Boot architecture keeps most tests outside `@SpringBootTest`.

## Observability and Operations

- Add Actuator for health/readiness/liveness where the deployment needs probes.
- Use Micrometer/Observation for important external calls and workflow spans.
- Keep metric tags low-cardinality; never tag raw user input, session text, PII,
  credentials, prompts, or retrieved document text.
- Make logs structured enough to debug request/session correlation without
  leaking regulated content.

## Security Boundaries

- Authenticate at API edges and pass caller identity as a typed application
  context, not as arbitrary strings pulled from static holders.
- Authorize in application services for business actions; endpoint checks alone
  are not enough for reusable workflows.
- For HTTP APIs, prefer explicit `SecurityFilterChain` beans with ordered
  `authorizeHttpRequests` rules and a final deny-all rule. The first matching
  rule wins, so put specific rules before broad ones.
- For bearer-token APIs, use OAuth2 Resource Server JWT or opaque-token support
  instead of custom token parsing unless project specs require otherwise.
- Keep secrets in external configuration and secret stores; never expose them in
  configuration properties endpoints, logs, traces, prompt context, or tool
  schemas.
- Include negative tests for forbidden caller, wrong tenant/session owner,
  malformed input, replay/idempotency conflict, and rate limits when relevant.

## AOT and Native Readiness

For applications that may use Spring AOT/native images:

- Prefer constructor injection and explicit configuration over reflection-heavy
  dynamic wiring.
- Keep serialization DTOs explicit and covered by tests.
- Avoid runtime classpath scanning tricks in domain/application logic.
- Check native hints for libraries that use reflection, proxies, resources, or
  dynamic clients; add a `RuntimeHintsRegistrar` or library-native hint when an
  adapter needs explicit reflection/resource/proxy registration.
- Use `@NestedConfigurationProperty` when nested configuration properties are
  not inner classes and need metadata/native reflection support.
- Remember that AOT/native processing assumes a fixed classpath and build-time
  profile choices; do not rely on runtime profile switching for native images.
- Treat AOT warnings as architecture feedback, not only packaging issues.
