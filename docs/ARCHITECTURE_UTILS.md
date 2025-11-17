# Utils Layer Architecture

[← Back to Architecture Index](./ARCHITECTURE.md)

---

## Utils Layer Overview

The Utils layer contains pure functions, stateless helpers, and utility services. Even utility services should follow the interface/abstraction pattern for consistency and testability.

## Utils Module Structure

Each utility module should follow the standard interface pattern:

```
utils/
├── date_utils/
│   ├── service.py              # Implementation
│   ├── interface/
│   │   ├── __init__.py         # Exports
│   │   └── abstraction.py     # Abstract class
│   └── __init__.py             # Module exports
├── common/
│   ├── service.py
│   ├── interface/
│   │   ├── __init__.py
│   │   └── abstraction.py
│   └── __init__.py
└── constants/
    └── __init__.py             # Constants don't need interface
```

## Interface Pattern for Utils

Even utility services should have abstract interfaces:

```python
# utils/date_utils/interface/abstraction.py
from abc import ABC, abstractmethod
from datetime import datetime

class AbstractDateTimeService(ABC):
    """Interface for datetime operations."""
    
    @abstractmethod
    def now(self) -> datetime:
        """Get current UTC datetime."""
        pass
    
    @abstractmethod
    def timestamp(self) -> float:
        """Get current Unix timestamp."""
        pass
    # ... other methods
```

```python
# utils/date_utils/service.py
from . import interface

class DateTimeService(interface.AbstractDateTimeService):
    """Service for datetime operations."""
    
    def now(self) -> datetime:
        return datetime.now(timezone.utc)
    
    def timestamp(self) -> float:
        return datetime.now(timezone.utc).timestamp()
    # ... implementations
```

## Usage in Other Layers

When using utility services, import the interface for type hints and the service instance for usage:

```python
# usecase/user_management/service.py
from utils.date_utils import interface as date_utils_interface
from utils.date_utils import datetime_service

class UserManagementService:
    def __init__(
        self,
        user_repo: user_repository_interface.AbstractUserRepository,
        date_service: date_utils_interface.AbstractDateTimeService = datetime_service
    ):
        self.user_repo = user_repo
        self.date_service = date_service
    
    def register_user(self, request):
        # Use the service
        now = self.date_service.now()
        # ...
```

## Benefits

1. **Testability**: Easy to mock utility services in tests
2. **Consistency**: All services follow the same pattern
3. **Flexibility**: Can swap implementations if needed
4. **Type Safety**: Abstract classes provide clear contracts

## Constants

Constants modules don't need interfaces - they're just static values:

```python
# utils/constants/__init__.py
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100
```

## Pure Functions

Pure functions (no state, no side effects) can be in service files without interfaces:

```python
# utils/common/service.py
def calculate_total(items: list[float]) -> float:
    """Pure function - no interface needed."""
    return sum(items)
```

However, if a utility has state or complex behavior, it should have an interface.

---

[← Back to Architecture Index](./ARCHITECTURE.md)

