# Java/Spring Architecture Reference

Use this reference when translating Clean, Hexagonal, Onion, or DDD patterns
into a Java/Spring codebase.

## Structure Options

Prefer package names that match the business capability. A practical module can
look like this:

```text
orders/
  api/
    OrderController.java
    CreateOrderRequest.java
    OrderResponse.java
  application/
    CreateOrderUseCase.java
    OrderResult.java
    ports/
      OrderRepository.java
      CatalogClient.java
      PaymentGateway.java
  domain/
    Order.java
    OrderLine.java
    Money.java
    OrderStatus.java
    events/
      OrderSubmitted.java
  infrastructure/
    persistence/
      JpaOrderEntity.java
      SpringDataOrderRepository.java
      JpaOrderRepositoryAdapter.java
    http/
      CatalogRestClient.java
    payment/
      PaymentGatewayAdapter.java
    config/
      OrdersProperties.java
```

Dependency rule:

```text
api -> application -> domain
infrastructure -> application ports + domain
domain -> only Java/domain types
```

For larger Spring systems, consider a Spring Modulith-style package contract
when the project already uses it or adding it is in scope:

```text
com.acme.orders
  order
    OrderService.java          # public module API
    OrderPlaced.java           # public event
    internal/
      PlaceOrderUseCase.java
      Order.java
      JpaOrderRepositoryAdapter.java
  payment
    PaymentService.java
    internal/
      PaymentGatewayAdapter.java
```

Spring Modulith can verify package-level cycles and accidental dependencies on
another module's `internal` packages:

```java
import org.junit.jupiter.api.Test;
import org.springframework.modulith.core.ApplicationModules;

class ArchitectureVerificationTests {

    @Test
    void modulesRespectDeclaredBoundaries() {
        ApplicationModules.of(OrderManagementApplication.class).verify();
    }
}
```

If Spring Modulith is not present and should not be added, use the same idea with
existing import checks, ArchUnit, build rules, or focused review checklist items.

## Domain Model

Use records for immutable value objects and classes for aggregates with behavior.
Validate invariants at construction time.

```java
package orders.domain;

import java.math.BigDecimal;
import java.util.Currency;
import java.util.Objects;

public record Money(BigDecimal amount, Currency currency) {

    public Money {
        Objects.requireNonNull(amount, "amount");
        Objects.requireNonNull(currency, "currency");
        if (amount.signum() < 0) {
            throw new IllegalArgumentException("amount must be non-negative");
        }
    }

    public Money add(Money other) {
        if (!currency.equals(other.currency())) {
            throw new IllegalArgumentException("currency mismatch");
        }
        return new Money(amount.add(other.amount()), currency);
    }
}
```

```java
package orders.domain;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

public final class Order {

    private final UUID id;
    private final List<OrderLine> lines = new ArrayList<>();
    private OrderStatus status = OrderStatus.DRAFT;

    public Order(UUID id) {
        this.id = id;
    }

    public void addLine(String sku, int quantity, Money unitPrice) {
        if (status != OrderStatus.DRAFT) {
            throw new IllegalStateException("submitted orders cannot change");
        }
        if (quantity <= 0) {
            throw new IllegalArgumentException("quantity must be positive");
        }
        lines.add(new OrderLine(sku, quantity, unitPrice));
    }

    public void submit() {
        if (lines.isEmpty()) {
            throw new IllegalStateException("empty order cannot be submitted");
        }
        status = OrderStatus.SUBMITTED;
    }

    public UUID id() {
        return id;
    }
}
```

## Application Ports and Use Cases

Define ports from the application's point of view. Keep names business-oriented,
not technology-oriented.

```java
package orders.application.ports;

import java.util.Optional;
import java.util.UUID;
import orders.domain.Order;

public interface OrderRepository {
    Optional<Order> findById(UUID id);
    Order save(Order order);
}
```

```java
package orders.application;

import java.util.UUID;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import orders.application.ports.OrderRepository;
import orders.domain.Order;

@Service
public class CreateOrderUseCase {

    private final OrderRepository orders;

    public CreateOrderUseCase(OrderRepository orders) {
        this.orders = orders;
    }

    @Transactional
    public CreateOrderResult handle(CreateOrderCommand command) {
        Order order = new Order(UUID.randomUUID());
        command.lines().forEach(line ->
                order.addLine(line.sku(), line.quantity(), line.unitPrice()));
        order.submit();
        return CreateOrderResult.from(orders.save(order));
    }
}
```

Guidelines:

- Put `@Transactional` on public application-service methods reached through the
  Spring proxy.
- Avoid external HTTP, broker, and LLM calls inside database transactions unless
  the transaction is explicitly short and safe.
- Keep command/result records in application or API packages, not in domain when
  they represent transport/use-case shape rather than core concepts.

## API Adapter

Controllers parse requests, validate DTOs, call one use case, and map results.
They do not enforce business workflows.

```java
package orders.api;

import jakarta.validation.Valid;
import java.net.URI;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import orders.application.CreateOrderCommand;
import orders.application.CreateOrderUseCase;

@RestController
@RequestMapping("/orders")
class OrderController {

    private final CreateOrderUseCase createOrder;

    OrderController(CreateOrderUseCase createOrder) {
        this.createOrder = createOrder;
    }

    @PostMapping
    ResponseEntity<OrderResponse> create(@Valid @RequestBody CreateOrderRequest request) {
        var result = createOrder.handle(request.toCommand());
        return ResponseEntity
                .created(URI.create("/orders/" + result.id()))
                .body(OrderResponse.from(result));
    }
}
```

Use `ProblemDetail`/`@ControllerAdvice` for API error mapping when error shape is
part of the contract.

## Persistence Adapter

Keep JPA annotations in persistence types. Map to/from domain explicitly unless
the domain model is intentionally anemic and documented as such.

```java
package orders.infrastructure.persistence;

import java.util.Optional;
import java.util.UUID;
import org.springframework.stereotype.Repository;
import orders.application.ports.OrderRepository;
import orders.domain.Order;

@Repository
class JpaOrderRepositoryAdapter implements OrderRepository {

    private final SpringDataOrderRepository repository;
    private final OrderMapper mapper;

    JpaOrderRepositoryAdapter(SpringDataOrderRepository repository, OrderMapper mapper) {
        this.repository = repository;
        this.mapper = mapper;
    }

    @Override
    public Optional<Order> findById(UUID id) {
        return repository.findById(id).map(mapper::toDomain);
    }

    @Override
    public Order save(Order order) {
        return mapper.toDomain(repository.save(mapper.toEntity(order)));
    }
}
```

## Bounded Contexts

Use an Anti-Corruption Layer when another bounded context has a different model.
For example, `orders` should use its own `CustomerId` or `ProductSnapshot`
instead of importing `identity.User` or `catalog.Product`.

Use a Shared Kernel only for small, stable types that have explicit ownership and
versioning. If ownership is unclear, prefer duplication plus translation.

When a module must expose more than its root API, make the public surface
intentional. In Spring Modulith this can be a named interface; without it, use
package conventions and architecture tests to keep internal types private.

## Events and Side Effects

Use domain events for facts that happened inside the domain, but keep publishing
in the application/infrastructure layer. For reliable cross-process delivery,
prefer a transactional outbox over publishing directly from an aggregate.

Do not use events to hide synchronous validation requirements. If a use case
must know the result before returning, call an explicit port and handle failure.
