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


class TodoDependencyManagementBadRequestException(BadRequestRootException):
    """Base exception for todo dependency management bad request errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


class TodoDependencyManagementNotFoundException(NotFoundRootException):
    """Base exception for todo dependency management not found errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


class TodoDependencyManagementForbiddenException(ForbiddenRootException):
    """Base exception for todo dependency management forbidden errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


class TodoDependencyManagementInternalServerErrorException(InternalServerErrorRootException):
    """Base exception for todo dependency management internal server errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


# Specific exceptions
class TodoNotFoundByIdException(TodoDependencyManagementNotFoundException):
    """Exception raised when todo is not found by ID."""
    
    def __init__(self, todo_id: int):
        message = f"Todo with id {todo_id} not found"
        super().__init__(message, code="TODO_NOT_FOUND_BY_ID")


class TodoAccessDeniedException(TodoDependencyManagementForbiddenException):
    """Exception raised when user doesn't have access to todo."""
    
    def __init__(self, todo_id: int, user_id: int):
        message = f"User {user_id} does not have access to todo {todo_id}"
        super().__init__(message, code="TODO_ACCESS_DENIED")


class CircularDependencyException(TodoDependencyManagementBadRequestException):
    """Exception raised when a circular dependency is detected."""
    
    def __init__(self, todo_id: int, dependency_todo_id: int):
        message = f"Circular dependency detected between todo {todo_id} and {dependency_todo_id}"
        super().__init__(message, code="CIRCULAR_DEPENDENCY")


class InvalidDependencyException(TodoDependencyManagementBadRequestException):
    """Exception raised when a dependency is invalid."""
    
    def __init__(self, message: str):
        super().__init__(message, code="INVALID_DEPENDENCY")

