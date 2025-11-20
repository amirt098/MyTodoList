# Standard library
# (none needed)

# Third-party
# (none needed)

# Internal - from other modules
from lib.exceptions import (
    BadRequestRootException,
    InternalServerErrorRootException
)

# Internal - from same interface module
# (none needed)


class SMSBadRequestException(BadRequestRootException):
    """Base exception for SMS-related bad request errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


class SMSInternalServerErrorException(InternalServerErrorRootException):
    """Base exception for SMS-related internal server errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


# Specific exceptions
class SMSSendFailedException(SMSInternalServerErrorException):
    """Exception raised when SMS sending fails."""
    
    def __init__(self, reason: str):
        message = f"Failed to send SMS: {reason}"
        super().__init__(message, code="SMS_SEND_FAILED")

