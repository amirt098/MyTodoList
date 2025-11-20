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


class SmartTodoManagementBadRequestException(BadRequestRootException):
    """Base exception for smart todo management bad request errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


class SmartTodoManagementInternalServerErrorException(InternalServerErrorRootException):
    """Base exception for smart todo management internal server errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


# Specific exceptions
class LLMServiceUnavailableException(SmartTodoManagementInternalServerErrorException):
    """Exception raised when LLM service is unavailable."""
    
    def __init__(self, reason: str):
        message = f"LLM service unavailable: {reason}"
        super().__init__(message, code="LLM_SERVICE_UNAVAILABLE")


class InvalidTextException(SmartTodoManagementBadRequestException):
    """Exception raised when text input is invalid."""
    
    def __init__(self, message: str = "Invalid text input"):
        super().__init__(message, code="INVALID_TEXT")

