# Exception Handling Architecture

[← Back to Architecture Index](./ARCHITECTURE.md)

---

## Exception Hierarchy

The application uses a hierarchical exception structure:

1. **Root Exceptions** (`lib/exceptions.py`) - Base exception classes
2. **Module Exceptions** (`module/interface/exceptions.py`) - Module-specific base exceptions
3. **Specific Exceptions** - Concrete exceptions with built-in messages

### Root Exceptions

Located in `lib/exceptions.py`, these are the base exception classes:
- `BaseRootException` - Base for all exceptions
- `BadRequestRootException` - 400 Bad Request
- `UnauthorizedRootException` - 401 Unauthorized
- `ForbiddenRootException` - 403 Forbidden
- `NotFoundRootException` - 404 Not Found
- `InternalServerErrorRootException` - 500 Internal Server Error

### Module Exceptions

Each module should have its own exception file: `module/interface/exceptions.py`

**Structure:**
```python
# repository/user/interface/exceptions.py
from lib.exceptions import BadRequestRootException, NotFoundRootException

class UserBadRequestException(BadRequestRootException):
    """Base exception for user-related bad request errors."""
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)

class UserNotFoundException(NotFoundRootException):
    """Base exception for user not found errors."""
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)
```

### Specific Exceptions

Specific exceptions inherit from module exceptions and have built-in messages:

```python
class UserEmailAlreadyExistsException(UserBadRequestException):
    """Exception raised when trying to create a user with an existing email."""
    
    def __init__(self, email: str):
        message = f"User with email {email} already exists"
        super().__init__(message, code="USER_EMAIL_EXISTS")

class UserNotFoundByIdException(UserNotFoundException):
    """Exception raised when a user is not found by ID."""
    
    def __init__(self, user_id: int):
        message = f"User with id {user_id} not found"
        super().__init__(message, code="USER_NOT_FOUND_BY_ID")
```

## Rules

1. **Never use root exceptions directly** - Always use module-specific exceptions
2. **Messages are built into exceptions** - Don't pass messages when raising, use specific exception classes
3. **Document exceptions in abstract classes** - All exceptions that can be raised must be documented in the abstract class/interface docstrings
4. **Export exceptions in interface/__init__.py** - Include `from .exceptions import *` in interface `__init__.py`

## Example Usage

### In Repository Service

```python
# repository/user/service.py
from . import interface

def create(self, user_data: interface.UserData) -> interface.UserDTO:
    try:
        # ... create user ...
    except IntegrityError:
        raise interface.UserEmailAlreadyExistsException(user_data.email)
```

### In UseCase Service

```python
# usecase/user_management/service.py
from . import interface

def register_user(self, request: interface.RegisterUserRequest):
    existing_user = self.user_repo.get_by_email(request.email)
    if existing_user:
        raise interface.UserRegistrationEmailExistsException(request.email)
```

### In Abstract Class Documentation

```python
# usecase/user_management/interface/abstraction.py
from .exceptions import UserRegistrationEmailExistsException

class AbstractUserManagementService(ABC):
    @abstractmethod
    def register_user(self, request: RegisterUserRequest) -> RegisterUserResponse:
        """
        Register a new user.
        
        Raises:
            UserRegistrationEmailExistsException: If email is already registered
        """
        pass
```

---

[← Back to Architecture Index](./ARCHITECTURE.md) | [Next: Timestamp Handling →](./ARCHITECTURE_TIMESTAMPS.md)

