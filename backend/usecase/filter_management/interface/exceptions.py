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


class FilterManagementBadRequestException(BadRequestRootException):
    """Base exception for filter management bad request errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


class FilterManagementNotFoundException(NotFoundRootException):
    """Base exception for filter management not found errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


class FilterManagementForbiddenException(ForbiddenRootException):
    """Base exception for filter management forbidden errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


class FilterManagementInternalServerErrorException(InternalServerErrorRootException):
    """Base exception for filter management internal server errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


# Specific exceptions
class SavedFilterNotFoundByIdException(FilterManagementNotFoundException):
    """Exception raised when saved filter is not found by ID."""
    
    def __init__(self, filter_id: int):
        message = f"Saved filter with id {filter_id} not found"
        super().__init__(message, code="SAVED_FILTER_NOT_FOUND_BY_ID")


class SavedFilterNameRequiredException(FilterManagementBadRequestException):
    """Exception raised when saved filter name is missing."""
    
    def __init__(self):
        message = "Saved filter name is required"
        super().__init__(message, code="SAVED_FILTER_NAME_REQUIRED")


class SavedFilterAccessDeniedException(FilterManagementForbiddenException):
    """Exception raised when user doesn't have access to saved filter."""
    
    def __init__(self, filter_id: int, user_id: int):
        message = f"User {user_id} does not have access to saved filter {filter_id}"
        super().__init__(message, code="SAVED_FILTER_ACCESS_DENIED")

