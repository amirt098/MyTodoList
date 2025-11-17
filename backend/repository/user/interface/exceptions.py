# Standard library
# (none needed)

# Third-party
# (none needed)

# Internal - from other modules
from lib.exceptions import (
    BadRequestRootException,
    NotFoundRootException,
    UnauthorizedRootException,
    ForbiddenRootException,
    InternalServerErrorRootException
)

# Internal - from same interface module
# (none needed)


class UserBadRequestException(BadRequestRootException):
    """Base exception for user-related bad request errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


class UserNotFoundException(NotFoundRootException):
    """Base exception for user not found errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


class UserUnauthorizedException(UnauthorizedRootException):
    """Base exception for user-related unauthorized errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


class UserForbiddenException(ForbiddenRootException):
    """Base exception for user-related forbidden errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


class UserInternalServerErrorException(InternalServerErrorRootException):
    """Base exception for user-related internal server errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


# Specific exceptions inheriting from module exceptions

class UserEmailAlreadyExistsException(UserBadRequestException):
    """Exception raised when trying to create a user with an existing email."""
    
    def __init__(self, email: str):
        message = f"User with email {email} already exists"
        super().__init__(message, code="USER_EMAIL_EXISTS")


class UserEmailConflictException(UserBadRequestException):
    """Exception raised when trying to update a user with an email that's already in use."""
    
    def __init__(self, email: str):
        message = f"Email {email} is already in use"
        super().__init__(message, code="USER_EMAIL_CONFLICT")


class UserNotFoundByIdException(UserNotFoundException):
    """Exception raised when a user is not found by ID."""
    
    def __init__(self, user_id: int):
        message = f"User with id {user_id} not found"
        super().__init__(message, code="USER_NOT_FOUND_BY_ID")


class UserNotFoundByEmailException(UserNotFoundException):
    """Exception raised when a user is not found by email."""
    
    def __init__(self, email: str):
        message = f"User with email {email} not found"
        super().__init__(message, code="USER_NOT_FOUND_BY_EMAIL")

