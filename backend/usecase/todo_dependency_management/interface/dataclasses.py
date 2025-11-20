# Standard library
from typing import Optional, List

# Third-party
# (none needed)

# Internal - from other modules
from lib.base_models import BaseRequest, BaseResponse

# Internal - from same interface module
# (none needed)


class SetDependencyRequest(BaseRequest):
    """Request DTO for setting a todo dependency."""
    todo_id: int
    dependency_type: str  # 'previous' or 'next'
    dependency_todo_id: int  # ID of the todo to link
    user_id: int  # For access control


class SetDependencyResponse(BaseResponse):
    """Response DTO for setting a dependency."""
    todo_id: int
    dependency_type: str
    dependency_todo_id: int
    success: bool


class RemoveDependencyRequest(BaseRequest):
    """Request DTO for removing a todo dependency."""
    todo_id: int
    dependency_type: str  # 'previous' or 'next'
    user_id: int  # For access control


class RemoveDependencyResponse(BaseResponse):
    """Response DTO for removing a dependency."""
    todo_id: int
    dependency_type: str
    success: bool


class ValidateDependencyRequest(BaseRequest):
    """Request DTO for validating a dependency chain."""
    todo_id: int
    user_id: int  # For access control


class ValidateDependencyResponse(BaseResponse):
    """Response DTO for validating dependencies."""
    todo_id: int
    is_valid: bool
    has_circular_dependency: bool
    chain_length: int
    message: str


class DependencyNode(BaseResponse):
    """DTO for a node in the dependency chain."""
    todo_id: int
    title: str
    status: str
    previous_todo_id: Optional[int] = None
    next_todo_id: Optional[int] = None


class GetDependencyChainRequest(BaseRequest):
    """Request DTO for getting a dependency chain."""
    todo_id: int
    user_id: int  # For access control
    direction: str = 'both'  # 'previous', 'next', or 'both'


class GetDependencyChainResponse(BaseResponse):
    """Response DTO for getting dependency chain."""
    todo_id: int
    chain: List[DependencyNode]
    total_todos: int

