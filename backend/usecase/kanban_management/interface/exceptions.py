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


class KanbanManagementBadRequestException(BadRequestRootException):
    """Base exception for kanban management bad request errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


class KanbanManagementNotFoundException(NotFoundRootException):
    """Base exception for kanban management not found errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


class KanbanManagementInternalServerErrorException(InternalServerErrorRootException):
    """Base exception for kanban management internal server errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


# Specific exceptions
class KanbanColumnNotFoundByIdException(KanbanManagementNotFoundException):
    """Exception raised when kanban column is not found by ID."""
    
    def __init__(self, column_id: int):
        message = f"Kanban column with id {column_id} not found"
        super().__init__(message, code="KANBAN_COLUMN_NOT_FOUND_BY_ID")


class KanbanColumnNameRequiredException(KanbanManagementBadRequestException):
    """Exception raised when kanban column name is missing."""
    
    def __init__(self):
        message = "Kanban column name is required"
        super().__init__(message, code="KANBAN_COLUMN_NAME_REQUIRED")


class TodoNotFoundByIdException(KanbanManagementNotFoundException):
    """Exception raised when todo is not found by ID."""
    
    def __init__(self, todo_id: int):
        message = f"Todo with id {todo_id} not found"
        super().__init__(message, code="TODO_NOT_FOUND_BY_ID")

