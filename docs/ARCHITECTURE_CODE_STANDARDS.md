# Code Standards & Code of Conduct

[← Back to Architecture Index](./ARCHITECTURE.md)

---

This section defines the coding standards and best practices that all developers must follow when contributing to the project.

## 1. Import Order

Follow a strict import order for better readability and to avoid circular dependencies:

1. **Standard library modules** (e.g., `os`, `sys`, `datetime`, `logging`)
2. **Third-party libraries** (e.g., `requests`, `pydantic`, `django`)
3. **Internal project modules** (from outer to inner):
   - `lib/` modules (if needed)
   - `utils/` modules first
   - `clients/` modules
   - `externals/` modules
   - `repository/` modules
   - `usecase/` modules
   - `presentation/` modules

**Rules:**
- Each group separated by a blank line
- Within each group, imports sorted alphabetically
- Use absolute imports, not relative imports

**Example:**
```python
# Standard library
import logging
from datetime import datetime
from typing import List, Optional

# Third-party
from pydantic import BaseModel
from django.db import models

# Internal - from outer to inner
from lib.exceptions import BadRequestRootException
from utils.date_utils import format_date
from clients.redis import interface as redis_interface
from repository.user import interface as user_repository_interface
from usecase.todo_management import interface

# Usage in code:
# - interface.CreateTodoRequest (same module)
# - user_repository_interface.AbstractUserRepository (other module)
# - redis_interface.AbstractRedisService (other module)
```

**Import Rules for Same Module:**
- When importing from the **same service/module** (outside interface directory), import the `interface` module itself
- Use qualified names with `interface.` prefix in code
- Example: `from . import interface` then use `interface.CreateTodoRequest`, `interface.AbstractTodoManagementService`
- **Inside interface files** (e.g., `interface/abstraction.py`, `interface/dataclasses.py`): Use direct imports without `interface.` prefix
- Example inside interface: `from .dataclasses import CreateTodoRequest` (no prefix needed)

**Import Rules for Other Modules:**
- When importing from **other modules**, import the interface module with a descriptive name
- Use qualified names with the interface module name prefix
- Example: `from repository.user import interface as user_repository_interface` then use `user_repository_interface.AbstractUserRepository`
- Example: `from externals.email import interface as email_interface` then use `email_interface.AbstractEmailService`
- Example: `from lib.exceptions import BadRequestRootException` (lib modules don't need interface prefix)

**Abstract Class Naming Convention:**
- Use `Abstract` prefix for all abstract classes
- Example: `AbstractTodoRepository`, `AbstractUserManagementService`, `AbstractEmailService`
- Alternative: `InterfaceTodoRepository` (but `Abstract` is preferred)

## 2. Single Responsibility Principle

- Each class or function should have only one clear responsibility
- If a function does multiple things, split it into smaller functions
- If a class handles multiple concerns, consider splitting it

## 3. Class Naming

- Use **CamelCase** with first letter capitalized
- Class name should describe its nature or purpose, ending with its type/role
- Examples: `UserService`, `TodoRepository`, `EmailClient`, `PaymentManager`
- Add a brief docstring explaining the class's responsibility

**Examples:**
```python
class UserManagementService:
    """Service for managing user operations."""
    pass

class TodoRepositoryService:
    """Repository service for todo data access."""
    pass
```

## 4. Function Naming

- Use **snake_case** for function names
- Function name should follow pattern: "verb + object + modifier (if needed)"
- Make names meaningful and descriptive
- Examples: `calculate_sum`, `send_email_to_user`, `get_todo_by_id`, `create_user_account`

**Examples:**
```python
def get_todo_by_id(todo_id: int) -> TodoDTO:
    """Get a todo by its ID."""
    pass

def send_verification_email_to_user(user_email: str) -> None:
    """Send verification email to user."""
    pass
```

## 5. Logging Input and Output

- **Log input at the start** of every function with `logger.info()` level
- **Log output at the end** of every function with `logger.info()` level
- Use `logging` module instead of `print()` statements
- Use structured logging with `extra` parameter for better parsing

**Example:**
```python
import logging

logger = logging.getLogger(__name__)

def create_todo(self, request: CreateTodoRequest) -> CreateTodoResponse:
    logger.info(
        f"Creating todo: {request.title}",
        extra={"input": request.model_dump()}
    )
    
    # ... function logic ...
    
    logger.info(
        f"Todo created successfully: {response.todo_id}",
        extra={"output": response.model_dump()}
    )
    return response
```

## 6. Logging Errors and Exceptions

- All errors in `try-except` blocks should be logged
- Use `logger.error()` for critical errors
- Use `logger.warning()` for non-critical issues
- Use `logging.exception()` to automatically include traceback
- Never use bare `except:` - always catch specific exceptions

**Example:**
```python
try:
    user = self.user_repo.get_by_id(user_id)
except NotFoundRootException as e:
    logger.error(
        f"User not found: {user_id}",
        extra={"user_id": user_id, "error": str(e)},
        exc_info=True
    )
    raise
except Exception as e:
    logger.exception(f"Unexpected error getting user: {user_id}")
    raise InternalServerErrorRootException("Failed to get user")
```

## 7. Type Hints

- **Always use type hints** for function parameters and return types
- Improves code readability and enables better IDE support
- Use `typing` module for complex types (List, Dict, Optional, Union)

**Example:**
```python
from typing import List, Optional

def get_todos(
    self,
    filters: TodoFilter,
    limit: Optional[int] = None
) -> List[TodoDTO]:
    """Get todos with filtering."""
    pass
```

## 8. Documentation (Docstrings)

- **Every function, class, and module must have docstrings**
- Docstrings should explain purpose, parameters, return values, and exceptions
- Use Google or NumPy style docstrings
- **Important**: Docstrings go in abstract classes/interfaces, not implementations

**Example:**
```python
# In interface/abstraction.py
class AbstractTodoManagementService(ABC):
    @abstractmethod
    def get_todo_by_id(self, todo_id: int) -> TodoDTO:
        """
        Get a single todo by ID.
        
        This method is provided separately as it's used frequently.
        
        Args:
            todo_id: Todo ID to fetch
            
        Returns:
            TodoDTO with todo information
            
        Raises:
            NotFoundRootException: If todo doesn't exist
        """
        pass
```

## 9. Resource Management (Context Managers)

- Use `with` statement for file operations and resource management
- Ensures proper cleanup even if exceptions occur
- Example: `with open("file.txt") as f:`

**Example:**
```python
with open(file_path, 'r') as f:
    content = f.read()

# Or for database connections
with transaction.atomic():
    # database operations
    pass
```

## 10. Input Validation

- **Validate inputs before processing**
- Use Pydantic models for automatic validation
- Provide clear, helpful error messages
- Fail fast - validate early

**Example:**
```python
def create_todo(self, request: CreateTodoRequest) -> CreateTodoResponse:
    # Pydantic automatically validates request
    if not request.title or len(request.title.strip()) == 0:
        raise BadRequestRootException("Title cannot be empty")
    
    # Continue with logic...
```

## 11. Virtual Environments

- Always use virtual environments (`venv` or `virtualenv`)
- Keeps dependencies isolated per project
- Document dependencies in `requirements.txt` or `pyproject.toml`

## 12. Exception Handling

- **Avoid catching generic exceptions** - catch specific exceptions
- Use custom exceptions from `lib.exceptions`
- Always re-raise or handle exceptions appropriately
- Never use bare `except:` clause

**Example:**
```python
# ❌ BAD
try:
    user = self.user_repo.get_by_id(user_id)
except:  # Too generic
    pass

# ✅ GOOD
try:
    user = self.user_repo.get_by_id(user_id)
except NotFoundRootException:
    logger.warning(f"User not found: {user_id}")
    raise
except Exception as e:
    logger.error(f"Unexpected error: {e}", exc_info=True)
    raise InternalServerErrorRootException("Failed to get user")
```

## 13. Dependency Injection Type Declarations

- **Always declare injected dependencies with abstract class types**
- Makes it clear what interface is expected
- Enables better IDE support and type checking
- Never use concrete implementations in constructor parameters

**Example:**
```python
# ✅ GOOD - Using abstract class types with qualified names
from . import interface
from repository.todo import interface as todo_repository_interface
from repository.user import interface as user_repository_interface
from externals.email import interface as email_interface

class TodoManagementService(interface.AbstractTodoManagementService):
    def __init__(
        self,
        todo_repo: todo_repository_interface.AbstractTodoRepository,  # ✅ Abstract class
        user_repo: user_repository_interface.AbstractUserRepository,   # ✅ Abstract class
        email_client: email_interface.AbstractEmailService   # ✅ Abstract class
    ):
        self.todo_repo = todo_repo
        self.user_repo = user_repo
        self.email_client = email_client

# ❌ BAD - Using concrete implementations
class TodoManagementService(interface.AbstractTodoManagementService):
    def __init__(
        self,
        todo_repo: TodoRepositoryService,  # ❌ Concrete class
        user_repo: UserRepositoryService,   # ❌ Concrete class
    ):
        pass
```

## 14. Import Organization Within Same Module

When importing from the same service/module:
- Use `from interface.xxx` for DTOs, exceptions, and abstractions
- Keeps imports clean and shows they're from the same module

**Example:**
```python
# usecase/todo_management/service.py

# Standard library
import logging

# Third-party
from typing import List

# Internal - from other modules
from lib.exceptions import NotFoundRootException, BadRequestRootException
from repository.todo import interface as todo_repository_interface
from repository.user import interface as user_repository_interface

# Internal - from same module
from . import interface

# Usage in code:
# - interface.AbstractTodoManagementService
# - interface.CreateTodoRequest
# - interface.CreateTodoResponse
# - todo_repository_interface.AbstractTodoRepository
# - user_repository_interface.AbstractUserRepository
```

## 15. Performance Optimization

- Optimize algorithms and data structures in critical paths
- Use database query optimization (select_related, prefetch_related)
- Consider caching for frequently accessed data
- Profile before optimizing - measure, don't guess

## Code Organization Summary

Following these standards ensures:
- ✅ High code readability
- ✅ Maintainable and extensible codebase
- ✅ Secure and robust applications
- ✅ Prevention of common errors
- ✅ Better team collaboration
- ✅ Improved product quality

---

[← Back to Architecture Index](./ARCHITECTURE.md) | [Next: Logging →](./ARCHITECTURE_LOGGING.md)

