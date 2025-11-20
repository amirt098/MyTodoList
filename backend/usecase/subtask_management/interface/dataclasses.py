# Standard library
from typing import Optional, List

# Third-party
# (none needed)

# Internal - from other modules
from lib.base_models import BaseRequest, BaseResponse

# Internal - from same interface module
# (none needed)


class SubtaskDTO(BaseResponse):
    """Pydantic DTO for Subtask."""
    subtask_id: int
    title: str
    status: str
    todo_id: int
    order: int
    created_at: int
    updated_at: int
    completed_at_timestamp_ms: Optional[int] = None


class AddSubtaskRequest(BaseRequest):
    """Request DTO for adding a subtask to a todo."""
    todo_id: int
    title: str
    user_id: int  # For access control
    order: Optional[int] = None


class AddSubtaskResponse(BaseResponse):
    """Response DTO for adding a subtask."""
    subtask_id: int
    title: str
    status: str
    todo_id: int
    order: int
    created_at: int


class UpdateSubtaskRequest(BaseRequest):
    """Request DTO for updating a subtask."""
    subtask_id: int
    todo_id: int
    user_id: int  # For access control
    title: Optional[str] = None
    status: Optional[str] = None
    order: Optional[int] = None


class UpdateSubtaskResponse(BaseResponse):
    """Response DTO for updating a subtask."""
    subtask_id: int
    title: str
    status: str
    todo_id: int
    order: int
    updated_at: int


class DeleteSubtaskRequest(BaseRequest):
    """Request DTO for deleting a subtask."""
    subtask_id: int
    todo_id: int
    user_id: int  # For access control


class DeleteSubtaskResponse(BaseResponse):
    """Response DTO for deleting a subtask."""
    success: bool
    message: str


class MarkSubtaskDoneRequest(BaseRequest):
    """Request DTO for marking a subtask as done."""
    subtask_id: int
    todo_id: int
    user_id: int  # For access control
    done: bool = True  # True to mark done, False to mark undone


class MarkSubtaskDoneResponse(BaseResponse):
    """Response DTO for marking a subtask as done."""
    subtask_id: int
    status: str
    completed_at_timestamp_ms: Optional[int] = None


class GetSubtasksRequest(BaseRequest):
    """Request DTO for getting subtasks."""
    todo_id: int
    user_id: int  # For access control
    status: Optional[str] = None


class GetSubtasksResponse(BaseResponse):
    """Response DTO for getting subtasks."""
    subtasks: List[SubtaskDTO]
    total: int
    progress: float  # Progress percentage (0-100) based on completed subtasks

