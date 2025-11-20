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


class SubtaskBadRequestException(BadRequestRootException):
    """Base exception for subtask-related bad request errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


class SubtaskNotFoundException(NotFoundRootException):
    """Base exception for subtask not found errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


class SubtaskInternalServerErrorException(InternalServerErrorRootException):
    """Base exception for subtask-related internal server errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


# Specific exceptions
class SubtaskNotFoundByIdException(SubtaskNotFoundException):
    """Exception raised when subtask is not found by ID."""
    
    def __init__(self, subtask_id: int):
        message = f"Subtask with id {subtask_id} not found"
        super().__init__(message, code="SUBTASK_NOT_FOUND_BY_ID")


class SubtaskTitleRequiredException(SubtaskBadRequestException):
    """Exception raised when subtask title is missing."""
    
    def __init__(self):
        message = "Subtask title is required"
        super().__init__(message, code="SUBTASK_TITLE_REQUIRED")

