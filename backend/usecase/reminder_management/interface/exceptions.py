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


class ReminderManagementBadRequestException(BadRequestRootException):
    """Base exception for reminder management bad request errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


class ReminderManagementNotFoundException(NotFoundRootException):
    """Base exception for reminder management not found errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


class ReminderManagementForbiddenException(ForbiddenRootException):
    """Base exception for reminder management forbidden errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


class ReminderManagementInternalServerErrorException(InternalServerErrorRootException):
    """Base exception for reminder management internal server errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


# Specific exceptions
class ReminderNotFoundByIdException(ReminderManagementNotFoundException):
    """Exception raised when reminder is not found by ID."""
    
    def __init__(self, reminder_id: int):
        message = f"Reminder with id {reminder_id} not found"
        super().__init__(message, code="REMINDER_NOT_FOUND_BY_ID")


class ReminderTitleRequiredException(ReminderManagementBadRequestException):
    """Exception raised when reminder title is missing."""
    
    def __init__(self):
        message = "Reminder title is required"
        super().__init__(message, code="REMINDER_TITLE_REQUIRED")


class ReminderAccessDeniedException(ReminderManagementForbiddenException):
    """Exception raised when user doesn't have access to reminder."""
    
    def __init__(self, reminder_id: int, user_id: int):
        message = f"User {user_id} does not have access to reminder {reminder_id}"
        super().__init__(message, code="REMINDER_ACCESS_DENIED")

