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


class ReminderBadRequestException(BadRequestRootException):
    """Base exception for reminder-related bad request errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


class ReminderNotFoundException(NotFoundRootException):
    """Base exception for reminder not found errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


class ReminderInternalServerErrorException(InternalServerErrorRootException):
    """Base exception for reminder-related internal server errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


# Specific exceptions
class ReminderNotFoundByIdException(ReminderNotFoundException):
    """Exception raised when reminder is not found by ID."""
    
    def __init__(self, reminder_id: int):
        message = f"Reminder with id {reminder_id} not found"
        super().__init__(message, code="REMINDER_NOT_FOUND_BY_ID")


class ReminderTitleRequiredException(ReminderBadRequestException):
    """Exception raised when reminder title is missing."""
    
    def __init__(self):
        message = "Reminder title is required"
        super().__init__(message, code="REMINDER_TITLE_REQUIRED")

