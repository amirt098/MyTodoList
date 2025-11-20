# Standard library
# (none needed)

# Third-party
# (none needed)

# Internal - from other modules
from lib.exceptions import (
    BadRequestRootException,
    NotFoundRootException,
    InternalServerErrorRootException
)

# Internal - from same interface module
# (none needed)


class TodoBadRequestException(BadRequestRootException):
    """Base exception for todo-related bad request errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


class TodoNotFoundException(NotFoundRootException):
    """Base exception for todo not found errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


class TodoInternalServerErrorException(InternalServerErrorRootException):
    """Base exception for todo-related internal server errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


# Specific exceptions
class TodoNotFoundByIdException(TodoNotFoundException):
    """Exception raised when todo is not found by ID."""
    
    def __init__(self, todo_id: int):
        message = f"Todo with id {todo_id} not found"
        super().__init__(message, code="TODO_NOT_FOUND_BY_ID")


class TodoTitleRequiredException(TodoBadRequestException):
    """Exception raised when todo title is missing."""
    
    def __init__(self):
        message = "Todo title is required"
        super().__init__(message, code="TODO_TITLE_REQUIRED")


