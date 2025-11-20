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


class ProjectBadRequestException(BadRequestRootException):
    """Base exception for project-related bad request errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


class ProjectNotFoundException(NotFoundRootException):
    """Base exception for project not found errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


class ProjectInternalServerErrorException(InternalServerErrorRootException):
    """Base exception for project-related internal server errors."""
    
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message, code)


# Specific exceptions
class ProjectNotFoundByIdException(ProjectNotFoundException):
    """Exception raised when project is not found by ID."""
    
    def __init__(self, project_id: int):
        message = f"Project with id {project_id} not found"
        super().__init__(message, code="PROJECT_NOT_FOUND_BY_ID")


class ProjectNameRequiredException(ProjectBadRequestException):
    """Exception raised when project name is missing."""
    
    def __init__(self):
        message = "Project name is required"
        super().__init__(message, code="PROJECT_NAME_REQUIRED")


class ProjectMemberNotFoundException(ProjectNotFoundException):
    """Exception raised when project member is not found."""
    
    def __init__(self, project_id: int, user_id: int):
        message = f"Project member not found for project {project_id} and user {user_id}"
        super().__init__(message, code="PROJECT_MEMBER_NOT_FOUND")


class ProjectMemberAlreadyExistsException(ProjectBadRequestException):
    """Exception raised when project member already exists."""
    
    def __init__(self, project_id: int, user_id: int):
        message = f"Project member already exists for project {project_id} and user {user_id}"
        super().__init__(message, code="PROJECT_MEMBER_ALREADY_EXISTS")

