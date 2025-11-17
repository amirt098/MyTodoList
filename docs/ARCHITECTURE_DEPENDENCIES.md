# Dependency Rules

[← Back to Architecture Index](./ARCHITECTURE.md)

---

## Dependency Flow

```
Presentation → UseCase
UseCase → Repository + CommonUseCase + Externals
CommonUseCase → Repository + Utils
Repository → Infrastructure + Utils
Externals → Clients + Utils
Utils → nothing
Runner → constructs all dependencies but is imported by no one
```

## Rules of Thumb

1. **All imports point downward** - Lower layers never import from higher layers
2. **Only abstractions are imported** - Never import concrete implementations
3. **Business logic belongs in UseCase** - UseCase contains business logic and processes. CommonUseCase is only for logic that is repeated in 2 or more usecases
4. **Repository owns state changes** - All database mutations go through repositories
5. **CommonUseCase holds reusable business workflows** - Shared application logic used across multiple usecases
6. **No circular imports** - Architecture enforces unidirectional dependencies
7. **No cross-module ForeignKey relationships** - Models in different modules store IDs/UUIDs, not ForeignKey relationships

## Dependency Violations

❌ **BAD:**
```python
# Repository importing from UseCase
from usecase.register_user.service import RegisterUserService
```

✅ **GOOD:**
```python
# UseCase importing Repository abstraction
from repository.user.interface.abstraction import IUserRepository
```

## Model Relationship Rules

❌ **BAD - Direct ForeignKey between modules:**
```python
# repository/todo/models.py
from repository.user.models import User  # ❌ Importing model from different module

class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ❌ Direct FK relationship
    title = models.CharField(max_length=200)
```

✅ **GOOD - Store ID/UUID instead:**
```python
# repository/todo/models.py
# No import from repository.user

class Todo(models.Model):
    user_id = models.IntegerField()  # ✅ Store ID as regular field
    # OR
    user_uuid = models.UUIDField()  # ✅ Store UUID if using UUIDs
    title = models.CharField(max_length=200)
    
    # Relationships resolved at service layer
    # def get_user(self):
    #     return UserRepositoryService().get_by_id(self.user_id)
```

✅ **GOOD - ForeignKey within same module:**
```python
# repository/todo/models.py
from repository.todo.models import Subtask  # ✅ Same module

class Todo(models.Model):
    title = models.CharField(max_length=200)

class Subtask(models.Model):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE)  # ✅ OK within same module
    title = models.CharField(max_length=200)
```

**Why this matters:**
- Maintains loose coupling between modules
- Allows modules to be developed/deployed independently
- Prevents circular dependencies at database level
- Makes it easier to split into microservices later
- Relationships are resolved through repository services, not ORM

---

[← Back to Architecture Index](./ARCHITECTURE.md) | [Next: Bootstrapper →](./ARCHITECTURE_BOOTSTRAPPER.md)

