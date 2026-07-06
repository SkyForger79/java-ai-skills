# Spring AI Architecture Reference

Use this reference when a Java/Spring architecture includes model calls, prompt
contracts, tool calling, memory, RAG, vector stores, or AI observability.

## Placement

Spring AI belongs at the infrastructure/application edge.

```text
api -> application -> ai ports -> spring-ai adapter -> model/vector provider
domain -> no ChatClient, no PromptTemplate, no provider DTOs
```

Application code may depend on an explicit port:

```java
package support.application.ports;

public interface AnswerGenerator {
    GeneratedAnswer answer(AnswerRequest request);
}
```

The adapter owns Spring AI details:

```java
package support.infrastructure.ai;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.stereotype.Component;
import support.application.ports.AnswerGenerator;

@Component
class SpringAiAnswerGenerator implements AnswerGenerator {

    private final ChatClient chatClient;

    SpringAiAnswerGenerator(ChatClient.Builder builder) {
        this.chatClient = builder
                .defaultSystem("Answer only from supplied evidence.")
                .build();
    }

    @Override
    public GeneratedAnswer answer(AnswerRequest request) {
        return chatClient.prompt()
                .user(user -> user.text(request.prompt())
                        .param("evidence", request.evidence()))
                .call()
                .entity(GeneratedAnswer.class);
    }
}
```

## Prompt and Structured Output Contracts

- Keep prompts versioned and close to tests, usually under resources or a prompt
  package.
- Prefer structured outputs for routing, extraction, policy decisions, and
  final-action preparation.
- Validate model output with Java code before it changes state or calls tools.
- Add malformed-output fallback tests; do not rely on the model obeying schema
  instructions as the only safety layer.
- Keep hidden prompts and internal policies out of user-visible errors and logs.

## Tool Calling

Spring AI can expose tools/function callbacks to models. In regulated or
side-effectful systems, keep tool availability narrow and Java-owned.

Checklist:

- Expose only tools needed for the current use case.
- Use small input records with validation.
- Make read-only tools the default; require explicit confirmation or HITL for
  side effects.
- Enforce authorization, tenant/session ownership, idempotency, and policy in
  Java before executing the tool.
- Sanitize tool input/output before traces and model context.
- Test denied tools, malformed tool arguments, duplicate calls, and provider
  no-tool fallback.

Tool adapters should call application ports; they should not bypass domain or
policy services.

Spring AI `@Tool` methods are acceptable for narrow read-only capabilities when
their input records are validated and the method delegates to an application
service. For large toolsets, use `ToolSearchToolCallingAdvisor` or equivalent
on-demand discovery only after the same authorization, tenancy, idempotency, and
policy gates are enforced.

## RAG and Evidence Boundaries

Retrieval-Augmented Generation is an adapter boundary, not a source of policy.

- Keep corpus ingestion, splitting, embedding, and vector-store configuration in
  infrastructure.
- Use metadata filters for tenant, product domain, document class, locale, and
  freshness where the product requires isolation.
- Pass retrieved snippets as evidence with source metadata; do not treat
  retrieval no-answer as pseudo-evidence.
- Defend against prompt injection in retrieved documents by separating
  instructions from evidence and by telling the model that evidence is data.
- Return "no answer from approved sources" when retrieval confidence or source
  coverage is insufficient.
- Test cross-domain retrieval denial, no-answer, stale document filtering, and
  citation/source propagation.

## Memory

- Scope chat memory by tenant, user, session, and product domain as appropriate.
- Store summaries or structured facts when raw dialogue would leak PII or exceed
  retention policy.
- Do not use conversation memory as factual authority for recommendations,
  suitability, policy, pricing, or execution.
- Separate continuity context from approved evidence.

## Advisors and Cross-Cutting Concerns

Use Spring AI advisors for repeatable cross-cutting behavior such as memory,
RAG, guardrails, or logging, but keep business policy explicit in application
services. Advisors should not hide state transitions, approvals, or tool
eligibility decisions that tests need to assert.

Common advisor choices:

- `QuestionAnswerAdvisor` for straightforward vector-store-backed Q&A.
- `RetrievalAugmentationAdvisor` when query transformation, retrieval,
  post-processing, and generation need explicit control.
- Chat memory advisors only when conversation continuity is allowed by the
  product's retention and privacy rules.
- `ToolSearchToolCallingAdvisor` or other tool-discovery advisors only when the
  toolset is large and every discovered tool still passes Java authorization and
  policy gates.

## Vector Stores and ETL

- Use Spring AI document readers, transformers/splitters, embedding models, and
  `VectorStore` implementations as infrastructure.
- Keep `SimpleVectorStore` or fake retrievers for tests; use production vector
  stores only in integration or runtime smoke tests.
- Version ingestion jobs and metadata schemas so retrieval behavior is
  reproducible.

## Testing

AI tests should be deterministic by default.

| Behavior | Test approach |
|---|---|
| Prompt assembly | Golden prompt/resource test with sanitized fixtures |
| Structured parser | Valid, malformed, partial, and adversarial JSON cases |
| Application policy | Stub `AnswerGenerator`/AI port |
| Tool execution | Fake tool inputs plus authorization/idempotency checks |
| RAG no-answer | Fake retriever/vector store with empty result |
| Provider adapter wiring | Focused Spring context test with model disabled/stubbed |
| Live model smoke | Optional deploy/runtime check, not the only proof |

## Observability and Safety

- Record model/provider/operation metadata, latency, token counts, and error
  class when available.
- Redact prompts, raw dialogue, retrieved text, PII, credentials, and internal
  policies before logs or traces.
- Keep model configuration externalized.
- Fail closed on policy, schema, tool, retrieval, or provider errors when the
  workflow is regulated or side-effectful.
