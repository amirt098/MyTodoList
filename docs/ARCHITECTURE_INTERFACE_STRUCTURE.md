# Interface Structure & Import Pattern

[← Back to Architecture Index](./ARCHITECTURE.md)

---

## Interface Directory Structure

Each module's `interface/` directory contains separate files for different concerns, but exports everything through `__init__.py`:

```
module_name/
└── interface/
    ├── __init__.py         # Exports everything from submodules
    ├── abstraction.py      # Abstract class definitions
    ├── dataclasses.py      # Pydantic DTOs
    ├── exceptions.py       # Module-specific exceptions (optional)
    └── externals.py        # External dependencies interface (optional)
```

## Interface `__init__.py` Pattern

The `interface/__init__.py` file exports everything from submodules:

```python
# interface/__init__.py
from .abstraction import *
from .dataclasses import *
from .exceptions import *  # if exists
from .externals import *   # if exists
```

This allows importing the interface module and using qualified names:

```python
# ✅ GOOD - Import interface module and use qualified names
from . import interface

# Usage in code:
# - interface.AbstractTodoRepository
# - interface.CreateTodoRequest
# - interface.CreateTodoResponse
# - interface.TodoDTO
# - interface.TodoFilter
```

## Abstract Class Naming

- **Use `Abstract` prefix** for all abstract classes
- Examples: `AbstractTodoRepository`, `AbstractUserManagementService`, `AbstractEmailService`
- Alternative: `InterfaceTodoRepository` (but `Abstract` is preferred)

## Import Patterns

### Same Module Imports

When importing from the same service/module:

```python
# ✅ GOOD - Import interface module and use qualified names
from . import interface

# Usage in code:
# - interface.AbstractTodoManagementService
# - interface.CreateTodoRequest
# - interface.CreateTodoResponse
# - interface.TodoDTO
# - interface.TodoFilter
```

### Other Module Imports

When importing from other modules:

```python
# ✅ GOOD - Import interface with descriptive alias and use qualified names
from repository.user import interface as user_repository_interface
from externals.email import interface as email_interface
from lib.exceptions import BadRequestRootException

# Usage in code:
# - user_repository_interface.AbstractUserRepository
# - email_interface.AbstractEmailService
# - BadRequestRootException (lib modules don't need interface prefix)
```

## Example: Complete Interface Structure

### `usecase/todo_management/interface/abstraction.py`

```python
# Standard library
from abc import ABC, abstractmethod

# Internal - from same interface module (direct import, no interface. prefix needed)
from .dataclasses import (
    CreateTodoRequest, CreateTodoResponse,
    UpdateTodoRequest, UpdateTodoResponse,
    TodoFilter, TodoDTO
)

class AbstractTodoManagementService(ABC):
    """Interface for todo management operations."""
    
    @abstractmethod
    def create_todo(self, request: CreateTodoRequest) -> CreateTodoResponse:
        """Create a new todo."""
        pass
    
    @abstractmethod
    def get_todo_by_id(self, todo_id: int) -> TodoDTO:
        """Get a single todo by ID."""
        pass
    
    # ... other methods
```

### `usecase/todo_management/interface/dataclasses.py`

```python
# Standard library
from datetime import datetime

# Third-party
from pydantic import BaseModel, Field

# Internal - from other modules
from lib.base_models import BaseRequest, BaseResponse, BaseFilter

class CreateTodoRequest(BaseRequest):
    title: str
    description: str | None = None
    user_id: int

class CreateTodoResponse(BaseResponse):
    todo_id: int
    title: str
    created_at: datetime

class TodoDTO(BaseResponse):
    todo_id: int
    title: str
    user_id: int
    created_at: datetime

class TodoFilter(BaseFilter):
    user_id: int | None = None
    status: str | None = None
```

### `usecase/todo_management/interface/__init__.py`

```python
# Export everything from submodules
from .abstraction import AbstractTodoManagementService
from .dataclasses import (
    CreateTodoRequest,
    CreateTodoResponse,
    UpdateTodoRequest,
    UpdateTodoResponse,
    TodoDTO,
    TodoFilter
)
```

### Usage in Service

```python
# usecase/todo_management/service.py

# Standard library
import logging

# Third-party
# (none)

# Internal - from other modules
from lib.exceptions import NotFoundRootException
from repository.todo import interface as todo_repository_interface

# Internal - from same module
from . import interface

logger = logging.getLogger(__name__)

class TodoManagementService(interface.AbstractTodoManagementService):
    def __init__(self, todo_repo: todo_repository_interface.AbstractTodoRepository):
        self.todo_repo = todo_repo
    
    def create_todo(self, request: interface.CreateTodoRequest) -> interface.CreateTodoResponse:
        logger.info(f"Creating todo: {request.title}", extra={"input": request.model_dump()})
        # ... implementation
        logger.info(f"Todo created: {response.todo_id}", extra={"output": response.model_dump()})
        return response
```

---

[← Back to Architecture Index](./ARCHITECTURE.md)

