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


class SubtaskManagementBadRequestException(BadRequestRootException):
    """Base exception for subtask management bad request errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


class SubtaskManagementNotFoundException(NotFoundRootException):
    """Base exception for subtask management not found errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


class SubtaskManagementForbiddenException(ForbiddenRootException):
    """Base exception for subtask management forbidden errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


class SubtaskManagementInternalServerErrorException(InternalServerErrorRootException):
    """Base exception for subtask management internal server errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


# Specific exceptions
class SubtaskNotFoundByIdException(SubtaskManagementNotFoundException):
    """Exception raised when subtask is not found by ID."""
    
    def __init__(self, subtask_id: int):
        message = f"Subtask with id {subtask_id} not found"
        super().__init__(message, code="SUBTASK_NOT_FOUND_BY_ID")


class SubtaskTitleRequiredException(SubtaskManagementBadRequestException):
    """Exception raised when subtask title is missing."""
    
    def __init__(self):
        message = "Subtask title is required"
        super().__init__(message, code="SUBTASK_TITLE_REQUIRED")


class TodoNotFoundByIdException(SubtaskManagementNotFoundException):
    """Exception raised when todo is not found by ID."""
    
    def __init__(self, todo_id: int):
        message = f"Todo with id {todo_id} not found"
        super().__init__(message, code="TODO_NOT_FOUND_BY_ID")


class TodoAccessDeniedException(SubtaskManagementForbiddenException):
    """Exception raised when user doesn't have access to todo."""
    
    def __init__(self, todo_id: int, user_id: int):
        message = f"User {user_id} does not have access to todo {todo_id}"
        super().__init__(message, code="TODO_ACCESS_DENIED")

