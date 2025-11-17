# Standard library
# (none needed)

# Third-party
# (none needed)

# Internal
# (none needed)


class BaseRootException(Exception):
    """Base exception for all application exceptions."""
    
    def __init__(self, message: str, code: str | None = None):
        self.message = message
        self.code = code
        super().__init__(self.message)


class BadRequestRootException(BaseRootException):
    """400 Bad Request - Client error."""
    pass


class UnauthorizedRootException(BaseRootException):
    """401 Unauthorized - Authentication required."""
    pass


class ForbiddenRootException(BaseRootException):
    """403 Forbidden - Access denied."""
    pass


class NotFoundRootException(BaseRootException):
    """404 Not Found - Resource not found."""
    pass


class InternalServerErrorRootException(BaseRootException):
    """500 Internal Server Error - Server error."""
    pass

