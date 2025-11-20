# Quick Reference Guide - Architecture Notes
## Quick Reference for Architecture Guidelines

> This file contains key architecture guidelines that must be followed in every task.

---

## 📋 Layer Structure

```
Presentation → UseCase → Repository + CommonUseCase + Externals
```

### Responsibilities:
- **Presentation**: Only request/response handling, no business logic
- **UseCase**: Business logic and processes
- **Repository**: Only CRUD and data access, no business logic
- **CommonUseCase**: Shared logic used in 2+ usecases

---

## 🔄 Dependency Rules

1. ✅ All imports point downward (lower layers never import from higher layers)
2. ✅ Only abstractions are imported (never concrete implementations)
3. ✅ No ForeignKey between different modules (only ID/UUID stored)
4. ✅ ForeignKey only allowed within the same module

---

## 🎯 SOLID Principles

### Single Responsibility Principle (SRP)
- Each class/function should have **one clear responsibility**
- Split functions that do multiple things
- Split classes that handle multiple concerns

**Example:**
```python
# ✅ GOOD - Single responsibility
class UserRepositoryService:
    """Only handles user data access."""
    pass

# ❌ BAD - Multiple responsibilities
class UserService:
    """Handles data access, validation, and email sending."""
    pass
```

### Open/Closed Principle (OCP)
- Classes should be **open for extension, closed for modification**
- Use interfaces/abstract classes for extensibility
- Add new features by extending, not modifying existing code

**Example:**
```python
# ✅ GOOD - Extensible via interface
class AbstractEmailService(ABC):
    @abstractmethod
    def send(self, email: str): pass

class SMTPEmailService(AbstractEmailService):
    def send(self, email: str): ...

class SendGridEmailService(AbstractEmailService):
    def send(self, email: str): ...
```

### Liskov Substitution Principle (LSP)
- Subtypes must be **substitutable for their base types**
- Derived classes should not break base class contracts
- All implementations of an interface must fulfill the contract

**Example:**
```python
# ✅ GOOD - All implementations follow the contract
class AbstractRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: int) -> DTO | None: pass

class UserRepository(AbstractRepository):
    def get_by_id(self, id: int) -> UserDTO | None: ...  # ✅ Follows contract

class TodoRepository(AbstractRepository):
    def get_by_id(self, id: int) -> TodoDTO | None: ...  # ✅ Follows contract
```

### Interface Segregation Principle (ISP)
- Clients should not be forced to depend on interfaces they don't use
- Create **specific interfaces** instead of general-purpose ones
- Split large interfaces into smaller, focused ones

**Example:**
```python
# ❌ BAD - Large interface
class AbstractUserService(ABC):
    @abstractmethod
    def create(self): pass
    @abstractmethod
    def update(self): pass
    @abstractmethod
    def delete(self): pass
    @abstractmethod
    def send_email(self): pass  # Not all clients need this

# ✅ GOOD - Segregated interfaces
class AbstractUserRepository(ABC):
    @abstractmethod
    def create(self): pass
    @abstractmethod
    def update(self): pass
    @abstractmethod
    def delete(self): pass

class AbstractEmailService(ABC):
    @abstractmethod
    def send_email(self): pass
```

### Dependency Inversion Principle (DIP)
- High-level modules should not depend on low-level modules
- Both should depend on **abstractions**
- Always depend on interfaces, not concrete implementations

**Example:**
```python
# ✅ GOOD - Depends on abstraction
class UserManagementService:
    def __init__(self, user_repo: AbstractUserRepository):  # ✅ Interface
        self.user_repo = user_repo

# ❌ BAD - Depends on concrete implementation
class UserManagementService:
    def __init__(self, user_repo: UserRepositoryService):  # ❌ Concrete
        self.user_repo = user_repo
```

**Key Points:**
- Always use abstract class types in constructor parameters
- Never import concrete implementations across layers
- Use dependency injection with interfaces

---

## 📁 Interface Structure

Each module must have this structure:

```
module/
├── service.py
└── interface/
    ├── __init__.py      # Exports everything
    ├── abstraction.py   # Abstract classes (with Abstract prefix)
    ├── dataclasses.py   # Pydantic DTOs (BaseModel/BaseRequest/BaseResponse)
    ├── exceptions.py    # Module exceptions (extends lib exceptions)
    └── externals.py    # External dependencies (optional)
```

---

## 📥 Import Patterns

### Same Module (outside interface):
```python
from . import interface
# Usage: interface.CreateTodoRequest, interface.AbstractTodoService
```

### Other Modules:
```python
from repository.user import interface as user_repository_interface
# Usage: user_repository_interface.AbstractUserRepository
```

### Inside Interface Files:
```python
from .dataclasses import CreateTodoRequest  # No prefix
from .exceptions import UserNotFoundException  # No prefix
```

### Import Order:
1. Standard library
2. Third-party
3. Internal (from outer to inner): lib → utils → clients → externals → repository → usecase → presentation

---

## ⏰ Timestamps

- ✅ **Timestamps are calculated in UseCase** (not in Repository)
- ✅ Use `DateTimeService` from `utils.date_utils`
- ✅ Timestamps are stored as **integer (BigIntegerField)**
- ✅ Repository only stores timestamps (no calculation)
- ✅ In models: `created_at = models.BigIntegerField()` (not DateTimeField)

---

## 🚨 Exception Handling

### Hierarchy:
1. **Root Exceptions** (`lib/exceptions.py`): `BadRequestRootException`, `NotFoundRootException`, etc.
2. **Module Exceptions** (`module/interface/exceptions.py`): `UserBadRequestException`
3. **Specific Exceptions**: `UserEmailAlreadyExistsException`

### Rules:
- Never use root exceptions directly
- Messages are built into exception classes
- All exceptions must be documented in abstract class docstrings

---

## 📝 Logging

- ✅ Every method must **log input at the start** (`logger.info`)
- ✅ Every method must **log output at the end** (`logger.info`)
- ✅ Use structured logging with `extra` parameter
- ❌ No decorators - logging is done manually

```python
logger.info(f"Creating todo: {request.title}", extra={"input": request.model_dump()})
# ... logic ...
logger.info(f"Todo created: {response.todo_id}", extra={"output": response.model_dump()})
```

---

## 📚 Documentation

- ✅ All docstrings in **abstract classes** (not in implementations)
- ✅ Abstract classes define the contract and behavior
- ✅ Include: Args, Returns, Raises

---

## 💉 Dependency Injection

- ✅ Always declare with **abstract class types**:
```python
def __init__(self, user_repo: user_repository_interface.AbstractUserRepository)
```
- ❌ Never use concrete implementations in constructor parameters

---

## 🔧 Bootstrapper (Dependency Wiring)

### Location: `runner/bootstrap.py`

The bootstrapper is where **all dependencies are wired together**. When creating new services, you must update the bootstrap.

### Steps to Update Bootstrap:

1. **Import concrete service classes**:
```python
from repository.new_module.service import NewRepositoryService
from usecase.new_management.service import NewManagementService
from externals.new_service.service import NewExternalService
```

2. **Create instances in `__init__`**:
```python
def __init__(self):
    # Repositories (concrete implementations)
    self.new_repo = NewRepositoryService()
    
    # Externals (concrete implementations)
    self.new_external = NewExternalService()
    
    # UseCases (injecting abstract types, but using concrete instances)
    self.new_management_service = NewManagementService(
        new_repo=self.new_repo,           # AbstractNewRepository type expected
        new_external=self.new_external,    # AbstractNewExternalService type expected
        date_time_service=DateTimeService()  # If needed
    )
```

3. **Add getter method**:
```python
def get_new_management_service(self) -> NewManagementService:
    return self.new_management_service
```

### Important Notes:

- ✅ **Bootstrap is the ONLY place** where concrete implementations are imported
- ✅ All services are instantiated here
- ✅ Dependencies are injected here (but types are abstract)
- ✅ When adding a new service, **always update bootstrap**
- ✅ When adding new dependencies to existing services, **update bootstrap**
- ✅ Check existing service instantiations when dependencies change

### When to Update Bootstrap:

1. **Creating a new Repository** → Add import and instance
2. **Creating a new UseCase** → Add import, instance, and getter method
3. **Creating a new External service** → Add import and instance
4. **Adding dependency to existing UseCase** → Update service instantiation
5. **Adding Utils service** → Add import, instance, and inject to services that need it

### Complete Example: Adding DateTimeService

If a UseCase needs `DateTimeService`:

```python
# In bootstrap.py
from utils.date_utils.service import DateTimeService

class Bootstrapper:
    def __init__(self):
        # Repositories
        self.user_repo = UserRepositoryService()
        self.todo_repo = TodoRepositoryService()
        
        # Utils (shared services)
        self.date_time_service = DateTimeService()
        
        # UseCases (inject dependencies)
        self.user_management_service = UserManagementService(
            user_repo=self.user_repo,
            date_time_service=self.date_time_service  # ✅ Injected
        )
        
        self.todo_management_service = TodoManagementService(
            todo_repo=self.todo_repo,
            date_time_service=self.date_time_service  # ✅ Injected
        )
```

### Checklist for Bootstrap Updates:

- [ ] Import statement added for new service?
- [ ] Service instance created in `__init__`?
- [ ] Dependencies injected correctly?
- [ ] Getter method added (for UseCases)?
- [ ] All existing services checked for new dependencies?
- [ ] Utils services created once and shared?

---

## 🎯 Service Size Guidelines

- ✅ **Balanced**: Group related operations together
- ❌ Not too small: Don't create a separate service for each method
- ❌ Not too big: Don't put unrelated operations in one service

**Good Examples:**
- `UserManagementService`: register, login, password_recovery, update_profile
- `TodoManagementService`: create, update, delete, get, list todos

---

## 🗄️ Model Relationships

- ✅ Between different modules: only **ID/UUID** (no ForeignKey)
- ✅ Within same module: ForeignKey is allowed
- ✅ Relationships are resolved in service layer

```python
# ✅ GOOD
class Todo(models.Model):
    user_id = models.IntegerField()  # Not ForeignKey

# ❌ BAD
class Todo(models.Model):
    user = models.ForeignKey(User, ...)  # If User is in different module
```

---

## 🔧 Repository Pattern

### Dataclasses:
- `CreateRequest` and `UpdateRequest` (BaseModel)
- `DTO` with `from_model()` classmethod
- `Filter` extends BaseFilter

### Service:
- Use `CreateRequest` and `UpdateRequest` (not old Data classes)
- Use `DTO.from_model()` for conversion
- Timestamps stored directly as integer

---

## 🎨 Naming Conventions

- **Classes**: CamelCase with `Abstract` prefix for abstract classes
  - `AbstractTodoRepository`, `AbstractUserManagementService`
- **Functions**: snake_case
  - `create_todo`, `get_todo_by_id`
- **Files**: snake_case
  - `todo_views.py`, `user_management.py`

---

## ✅ Best Practices Checklist

Before committing code, check these items:

- [ ] All imports point downward?
- [ ] Only abstractions are imported?
- [ ] Timestamps calculated in UseCase?
- [ ] Timestamps stored as integer?
- [ ] Logging for input and output done?
- [ ] Docstrings in abstract classes?
- [ ] Dependency injection with abstract types?
- [ ] Exceptions extend from lib exceptions?
- [ ] Model relationships without ForeignKey between modules?
- [ ] Import order followed?
- [ ] Type hints for all functions?
- [ ] Pydantic for all DTOs?
- [ ] SOLID principles followed?
- [ ] Single Responsibility per class/function?
- [ ] Dependencies on abstractions, not concretions?
- [ ] Bootstrap updated with new services?
- [ ] All dependencies wired in bootstrap?

---

## 🔍 Quick Examples

### Repository Create:
```python
def create(self, todo_data: interface.TodoCreateRequest) -> interface.TodoDTO:
    logger.info(f"Creating todo: {todo_data.title}", extra={"input": todo_data.model_dump()})
    
    todo = Todo()
    todo.title = todo_data.title
    todo.created_at = todo_data.created_at  # integer
    todo.updated_at = todo_data.updated_at  # integer
    todo.save()
    
    result = interface.TodoDTO.from_model(todo)
    logger.info(f"Todo created: {result.todo_id}", extra={"output": result.model_dump()})
    return result
```

### UseCase Create:
```python
def create_todo(self, request: interface.CreateTodoRequest) -> interface.CreateTodoResponse:
    logger.info(f"Creating todo: {request.title}", extra={"input": request.model_dump()})
    
    # Calculate timestamps in UseCase
    now_dto = self.date_time_service.now()
    
    # Create repository request
    todo_create_request = todo_repository_interface.TodoCreateRequest(
        title=request.title,
        created_at=now_dto.timestamp_ms,  # integer
        updated_at=now_dto.timestamp_ms,  # integer
        # ... other fields
    )
    
    todo_dto = self.todo_repo.create(todo_create_request)
    
    response = interface.CreateTodoResponse(...)
    logger.info(f"Todo created: {response.todo_id}", extra={"output": response.model_dump()})
    return response
```

---

## 📌 Additional Important Notes

1. **Business Logic**: Always in UseCase, not in Repository
2. **CommonUseCase**: Only for shared logic (2+ usecases)
3. **Type Hints**: Always use them
4. **Fail Fast**: Validate early
5. **Single Responsibility**: Each class has one responsibility
6. **No Circular Imports**: Architecture enforces unidirectional dependencies
7. **SOLID Principles**: Follow all five principles in every design decision
8. **Interface Segregation**: Create focused interfaces, not large general ones
9. **Dependency Inversion**: Always depend on abstractions
10. **Bootstrap Updates**: Always update `runner/bootstrap.py` when creating new services or adding dependencies

---

**Version**: 1.0  
**Last Updated**: 2024


