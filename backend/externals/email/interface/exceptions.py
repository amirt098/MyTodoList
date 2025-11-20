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


class EmailBadRequestException(BadRequestRootException):
    """Base exception for email-related bad request errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


class EmailInternalServerErrorException(InternalServerErrorRootException):
    """Base exception for email-related internal server errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


# Specific exceptions
class EmailSendFailedException(EmailInternalServerErrorException):
    """Exception raised when email sending fails."""
    
    def __init__(self, reason: str):
        message = f"Failed to send email: {reason}"
        super().__init__(message, code="EMAIL_SEND_FAILED")

