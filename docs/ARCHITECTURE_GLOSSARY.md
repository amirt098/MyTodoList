# Glossary

[← Back to Architecture Index](./ARCHITECTURE.md)

---

## Architecture Terms

- **DTO**: Data Transfer Object - Pydantic models for data exchange (all inputs, outputs, filters)
- **UseCase**: Application-level action or operation (grouped logically, not one per method)
- **Repository**: Data access layer with domain logic
- **Abstraction**: Interface or Protocol defining a contract
- **Bootstrapper**: Dependency injection container
- **CommonUseCase**: Shared application logic across usecases (only for logic repeated in 2+ usecases)
- **Lib**: Shared foundation components (base models, exceptions, validators)

## Layer Terms

- **Presentation Layer**: Handles requests, converts input → DTO → output. No business logic.
- **UseCase Layer**: Contains business logic, processes, and workflows
- **Repository Layer**: Data access and simple state management, no business logic
- **CommonUseCase Layer**: Reusable business logic shared across 2+ usecases
- **Externals Layer**: External services and system-level integrations
- **Utils Layer**: Pure functions, stateless helpers, constants
- **Lib Layer**: Shared foundation components used across all layers
- **Runner Layer**: Django settings, URLs, and bootstrapper

## Design Patterns

- **Dependency Inversion**: High-level modules depend on abstractions, not concrete implementations
- **Single Responsibility**: Each class or function has one clear responsibility
- **Interface Segregation**: Clients should not depend on interfaces they don't use
- **Clean Architecture**: Separation of concerns with clear layer boundaries

---

[← Back to Architecture Index](./ARCHITECTURE.md)

