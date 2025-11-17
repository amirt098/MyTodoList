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


class UserManagementBadRequestException(BadRequestRootException):
    """Base exception for user management bad request errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


class UserManagementNotFoundException(NotFoundRootException):
    """Base exception for user management not found errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


class UserManagementUnauthorizedException(UnauthorizedRootException):
    """Base exception for user management unauthorized errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


class UserManagementForbiddenException(ForbiddenRootException):
    """Base exception for user management forbidden errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


class UserManagementInternalServerErrorException(InternalServerErrorRootException):
    """Base exception for user management internal server errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


# Specific exceptions inheriting from module exceptions

class UserRegistrationEmailExistsException(UserManagementBadRequestException):
    """Exception raised when trying to register a user with an existing email."""
    
    def __init__(self, email: str):
        message = f"User with email {email} already exists"
        super().__init__(message, code="REGISTRATION_EMAIL_EXISTS")


class UserLoginInvalidCredentialsException(UserManagementUnauthorizedException):
    """Exception raised when login credentials are invalid."""
    
    def __init__(self):
        message = "Invalid email or password"
        super().__init__(message, code="LOGIN_INVALID_CREDENTIALS")


class UserLoginInactiveAccountException(UserManagementUnauthorizedException):
    """Exception raised when trying to login with an inactive account."""
    
    def __init__(self):
        message = "User account is inactive"
        super().__init__(message, code="LOGIN_INACTIVE_ACCOUNT")


class UserProfileNotFoundException(UserManagementNotFoundException):
    """Exception raised when trying to update a profile for a non-existent user."""
    
    def __init__(self, user_id: int):
        message = f"User with id {user_id} not found"
        super().__init__(message, code="PROFILE_NOT_FOUND")

