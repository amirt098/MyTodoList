# Standard library
# (none needed)

# Third-party
# (none needed)

# Internal - from other modules
from lib.exceptions import (
    BadRequestRootException,
    NotFoundRootException,
    ForbiddenRootException,
    InternalServerErrorRootException
)

# Internal - from same interface module
# (none needed)


class BulkOperationsBadRequestException(BadRequestRootException):
    """Base exception for bulk operations bad request errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


class BulkOperationsNotFoundException(NotFoundRootException):
    """Base exception for bulk operations not found errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


class BulkOperationsForbiddenException(ForbiddenRootException):
    """Base exception for bulk operations forbidden errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


class BulkOperationsInternalServerErrorException(InternalServerErrorRootException):
    """Base exception for bulk operations internal server errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


# Specific exceptions
class TodoNotFoundByIdException(BulkOperationsNotFoundException):
    """Exception raised when todo is not found by ID."""
    
    def __init__(self, todo_id: int):
        message = f"Todo with id {todo_id} not found"
        super().__init__(message, code="TODO_NOT_FOUND_BY_ID")


class TodoAccessDeniedException(BulkOperationsForbiddenException):
    """Exception raised when user doesn't have access to todo."""
    
    def __init__(self, todo_id: int, user_id: int):
        message = f"User {user_id} does not have access to todo {todo_id}"
        super().__init__(message, code="TODO_ACCESS_DENIED")


class EmptyTodoListException(BulkOperationsBadRequestException):
    """Exception raised when todo_ids list is empty."""
    
    def __init__(self):
        message = "Todo IDs list cannot be empty"
        super().__init__(message, code="EMPTY_TODO_LIST")

