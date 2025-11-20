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


class SavedFilterBadRequestException(BadRequestRootException):
    """Base exception for saved filter-related bad request errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


class SavedFilterNotFoundException(NotFoundRootException):
    """Base exception for saved filter not found errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


class SavedFilterInternalServerErrorException(InternalServerErrorRootException):
    """Base exception for saved filter-related internal server errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


# Specific exceptions
class SavedFilterNotFoundByIdException(SavedFilterNotFoundException):
    """Exception raised when saved filter is not found by ID."""
    
    def __init__(self, filter_id: int):
        message = f"Saved filter with id {filter_id} not found"
        super().__init__(message, code="SAVED_FILTER_NOT_FOUND_BY_ID")


class SavedFilterNameRequiredException(SavedFilterBadRequestException):
    """Exception raised when saved filter name is missing."""
    
    def __init__(self):
        message = "Saved filter name is required"
        super().__init__(message, code="SAVED_FILTER_NAME_REQUIRED")

