# Architecture Layers

[← Back to Architecture Index](./ARCHITECTURE.md)

---

## 1. Introduction

This document describes the full architecture of a Django-based Modular Monolith designed using:

- **Clean Architecture principles**
- **Dependency Inversion**
- **Modular, feature-based structure**
- **Interface-driven services**
- **UseCase-oriented application layer**
- **Modular design with clear layer responsibilities**

The goal is to create a scalable, testable, maintainable architecture where each module is independent and easy to evolve.

---

## 2. High-Level Architecture Overview

```
--------------------------------------------
     Presentation Layer (REST, GraphQL)
--------------------------------------------
     UseCase Layer (Application Services)
--------------------------------------------
     Common UseCase Layer (Shared Logic)
--------------------------------------------
     Repository Layer (Data + Domain Logic)
--------------------------------------------
     Externals / Clients / Infrastructure
--------------------------------------------
     Utils (Pure Functions)
--------------------------------------------
     Runner (Django + Bootstrapper)
--------------------------------------------
```

### Layer Descriptions

#### Presentation Layer
Handles requests, converts input → DTO → output.
- **No business logic**
- Only orchestration of incoming/outgoing data
- Supports REST, GraphQL, WebSocket interfaces

#### UseCase Layer
Represents application-level actions and contains business logic.
Each usecase lives in its own folder containing:
- `service.py` - Main usecase implementation with business logic
- `interface/abstraction.py` - Interface definitions
- `interface/dataclasses.py` - Pydantic DTOs (all inputs, outputs, and filters)
- `interface/externals.py` - External dependencies interface

**Business Logic Placement:**
- **Business logic belongs in UseCase** - UseCase contains business logic, processes, and workflows
- **CommonUseCase is for shared logic only** - Move logic to CommonUseCase only if it's repeated in 2 or more usecases
- **Repository handles data access** - Repository focuses on CRUD and data persistence, not business logic

**UseCase Service Size Guidelines:**
- **Not too small**: Don't create a separate service for each method (e.g., don't have CreateTodoService, UpdateTodoService, DeleteTodoService separately)
- **Not too big**: Don't put unrelated operations in one service
- **Balanced approach**: Group related operations together (e.g., `TodoManagementService` handles create, update, delete, get, list operations for todos)
- **Complex operations**: Keep complex, specialized operations separate if they have different dependencies or significant complexity (e.g., AI-related services)

**Example of Good Service Grouping:**
- `UserManagementService` - register, login, password_recovery, update_profile
- `TodoManagementService` - create, update, delete, get, list todos
- `ProjectManagementService` - create, update, delete, manage_members
- `SmartTodoService` - AI-powered todo creation (separate due to different dependencies)

UseCases orchestrate logic using:
- Repository (for data access)
- Externals (for external services)
- Common UseCase (for shared business logic used by multiple usecases)

**Logging Requirements:**
- Every method must manually log input at the start
- Every method must manually log output at the end
- Use structured logging with appropriate log levels
- No decorators - logging is done explicitly in each method

**Documentation Requirements:**
- All docstrings and method explanations are in the abstract class/interface
- Implementation classes should not duplicate docstrings
- Abstract classes define the contract and behavior

**Import Organization:**
- Same module (outside interface): Import interface module `from . import interface` and use qualified names like `interface.CreateTodoRequest`, `interface.AbstractTodoManagementService`
- Inside interface files: Use direct imports `from .dataclasses import CreateTodoRequest` (no `interface.` prefix needed)
- Other modules: Import with descriptive alias `from repository.user import interface as user_repository_interface` and use `user_repository_interface.AbstractUserRepository`
- Abstract classes use `Abstract` prefix: `AbstractTodoRepository`, `AbstractUserManagementService`

**Dependency Injection:**
- Always declare injected dependencies with abstract class types using qualified names
- Example: `def __init__(self, user_repo: user_repository_interface.AbstractUserRepository)` not `UserRepositoryService`

#### Common UseCase Layer
Application-level shared logic used across multiple usecases:
- **Purpose**: Contains business logic that is repeated in 2 or more usecases
- **policies** - Business rules and policies shared across usecases
- **workflows** - Multi-step business processes shared across usecases
- **shared validators** - Reusable validation logic
- **shared converters** - Data transformation utilities

**When to use CommonUseCase:**
- Logic is used in 2 or more different usecases
- Logic represents a reusable business rule or workflow
- Logic needs to be consistent across multiple usecases

**When NOT to use CommonUseCase:**
- Logic is specific to a single usecase (keep it in that usecase)
- Logic is simple data access (belongs in Repository)

#### Repository Layer
Contains Django models and a thin repository service per module:
- **CRUD operations**
- **State transitions**
- **Domain/business rules** tied to persisted data
- **Repository abstraction interface**

Each repository module contains:
- `models.py` - Django ORM models
- `service.py` - Repository implementation
- `interface/abstraction.py` - Repository interface
- `interface/dataclasses.py` - Data transfer objects
- `interface/externals.py` - External dependencies

**Important: Model Relationships Between Modules**
- **No direct ForeignKey relationships** between models in different modules/apps
- Models in different modules should store IDs/UUIDs as regular fields, not ForeignKey
- This maintains loose coupling and allows modules to evolve independently
- Relationships are resolved at the service layer, not at the database level
- Within the same module, ForeignKey relationships are allowed

#### Externals / Clients / Infrastructure
External services and system-level integrations:
- Payment gateway
- SMS services
- Email services
- Redis
- Kafka
- Database wrappers
- Cache layer

Each external module contains:
- `service.py` - Service implementation
- `interface/abstraction.py` - Service interface
- `interface/dataclasses.py` - DTOs
- `interface/externals.py` - Nested external dependencies

#### Utils Layer
Pure functions, stateless helpers, constants.
- No dependencies on other layers
- Reusable across all layers
- No side effects

#### Lib Layer (Shared Foundation)
Common, reusable components used across all layers:
- **Base Pydantic Models** - Base classes for all DTOs
- **Common Validation Types** - Reusable Pydantic validators and types
- **Base Exceptions** - Root exception classes (e.g., `BadRequestRootException`, `NotFoundRootException`, `UnauthorizedRootException`)
- **Common Utilities** - Shared helper functions
- **Base Interfaces** - Common interface patterns

All service-specific exceptions extend from base exceptions in lib.

#### Runner Layer
Django settings, URLs, and a central bootstrapper that wires dependencies.
- `settings.py` - Django configuration
- `urls.py` - URL routing
- `bootstrap.py` - Dependency injection container

---

[← Back to Architecture Index](./ARCHITECTURE.md) | [Next: Dependency Rules →](./ARCHITECTURE_DEPENDENCIES.md)

