# Key Principles & Best Practices

[← Back to Architecture Index](./ARCHITECTURE.md)

---

## Key Principles

### 1. Separation of Concerns
Each layer has a single, well-defined responsibility.

### 2. Dependency Inversion
High-level modules depend on abstractions, not concrete implementations.

### 3. Testability
Each component can be tested in isolation using mocks/stubs of interfaces.

### 4. Scalability
New features can be added as new modules without affecting existing code.

### 5. Maintainability
Clear boundaries make code easy to understand and modify.

### 6. Layer Responsibilities
- **Presentation**: Only request/response handling, no business logic
- **UseCase**: Contains business logic, processes, and workflows
- **Repository**: Only data access and simple state management, no business logic
- **CommonUseCase**: Reusable business logic shared across 2+ usecases

---

## Testing Strategy

### Unit Tests
- Test each service in isolation
- Mock all dependencies using interfaces
- Test business logic in CommonUseCase

### Integration Tests
- Test repository with test database
- Test external services with test doubles
- Test usecase with real repositories but mocked externals

### End-to-End Tests
- Test full request/response cycle
- Use test database and mocked externals

---

## Migration Path

When adding a new feature:

1. **Define Domain Model** (if needed) → `repository/{feature}/models.py`
2. **Create Repository** → `repository/{feature}/service.py` + interface
3. **Create UseCase** → `usecase/{feature}/service.py` + interface
4. **Create Presentation** → `presentation/rest/{feature}_views.py`
5. **Wire in Bootstrapper** → `runner/bootstrap.py`
6. **Add URL Routes** → `runner/urls.py`

---

## Best Practices

1. **Always use interfaces** - Never import concrete implementations across layers
2. **Declare dependencies with abstract types** - Always use abstract class types in constructor parameters (e.g., `IUserRepository`, not `UserRepositoryService`)
3. **Import organization** - Use `from interface.xxx` for same-module imports, full paths for other modules
4. **Keep services balanced** - Group related operations, but don't make services too large or too small
5. **Use Pydantic for all DTOs** - All inputs, outputs, and filter objects must be Pydantic models extending BaseFilter/BaseRequest/BaseResponse
6. **Manual logging is mandatory** - Every method must manually log input at start and output at end (no decorators)
7. **Docstrings in abstract classes** - All method documentation and explanations go in the abstract class/interface, not implementation
8. **Extend base exceptions** - All service exceptions extend from lib exceptions (e.g., `BadRequestRootException`)
9. **General get method with filters** - Provide `get_todos(filters: Filter)` as general filtering method
10. **Separate get_by_id if used frequently** - If `get_by_id` is used a lot, provide it as a separate method
11. **No cross-module ForeignKey** - Models in different modules store IDs/UUIDs, not ForeignKey relationships
12. **Single Responsibility** - Each service handles a cohesive set of related operations
13. **Fail Fast** - Validate inputs early, use type hints
14. **Document interfaces** - Clear contracts between layers
15. **Consistent naming** - Follow the established patterns
16. **Use lib for common components** - Base models, validators, exceptions come from lib directory

---

[← Back to Architecture Index](./ARCHITECTURE.md) | [Next: Code Standards →](./ARCHITECTURE_CODE_STANDARDS.md)

