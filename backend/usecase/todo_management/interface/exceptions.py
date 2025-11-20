# Standard library
# (none needed)

# Third-party
# (none needed)

# Internal - from other modules
from lib.exceptions import (
    BadRequestRootException,
    NotFoundRootException,
    ForbiddenRootException
)

# Internal - from same interface module
# (none needed)


class TodoManagementBadRequestException(BadRequestRootException):
    """Base exception for todo management bad request errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


class TodoManagementNotFoundException(NotFoundRootException):
    """Base exception for todo management not found errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


class TodoManagementForbiddenException(ForbiddenRootException):
    """Base exception for todo management forbidden errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


# Specific exceptions
class TodoNotFoundByIdException(TodoManagementNotFoundException):
    """Exception raised when todo is not found by ID."""
    
    def __init__(self, todo_id: int):
        message = f"Todo with id {todo_id} not found"
        super().__init__(message, code="TODO_NOT_FOUND_BY_ID")


class TodoTitleRequiredException(TodoManagementBadRequestException):
    """Exception raised when todo title is missing."""
    
    def __init__(self):
        message = "Todo title is required"
        super().__init__(message, code="TODO_TITLE_REQUIRED")


class TodoAccessDeniedException(TodoManagementForbiddenException):
    """Exception raised when user doesn't have access to todo."""
    
    def __init__(self, todo_id: int, user_id: int):
        message = f"User {user_id} does not have access to todo {todo_id}"
        super().__init__(message, code="TODO_ACCESS_DENIED")


