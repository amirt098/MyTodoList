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


class ExportManagementBadRequestException(BadRequestRootException):
    """Base exception for export management bad request errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


class ExportManagementNotFoundException(NotFoundRootException):
    """Base exception for export management not found errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


class ExportManagementInternalServerErrorException(InternalServerErrorRootException):
    """Base exception for export management internal server errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


# Specific exceptions
class InvalidExportFormatException(ExportManagementBadRequestException):
    """Exception raised when export format is invalid."""
    
    def __init__(self, format: str):
        message = f"Invalid export format: {format}. Supported formats: json, csv"
        super().__init__(message, code="INVALID_EXPORT_FORMAT")

