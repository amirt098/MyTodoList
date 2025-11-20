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


class LLMBadRequestException(BadRequestRootException):
    """Base exception for LLM-related bad request errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


class LLMInternalServerErrorException(InternalServerErrorRootException):
    """Base exception for LLM-related internal server errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


# Specific exceptions
class LLMServiceUnavailableException(LLMInternalServerErrorException):
    """Exception raised when LLM service is unavailable."""
    
    def __init__(self, reason: str):
        message = f"LLM service unavailable: {reason}"
        super().__init__(message, code="LLM_SERVICE_UNAVAILABLE")

