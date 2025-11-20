# Standard library
from typing import Optional, List

# Third-party
# (none needed)

# Internal - from other modules
from lib.base_models import BaseRequest, BaseResponse

# Internal - from same interface module
# (none needed)


class BulkUpdateRequest(BaseRequest):
    """Request DTO for bulk updating todos."""
    todo_ids: List[int]  # List of todo IDs to update
    user_id: int  # For access control
    # Update fields (optional - only provided fields will be updated)
    status: Optional[str] = None
    priority: Optional[str] = None
    category: Optional[str] = None
    labels: Optional[List[str]] = None
    project_id: Optional[int] = None


class BulkUpdateResponse(BaseResponse):
    """Response DTO for bulk updating todos."""
    updated_count: int
    failed_count: int
    failed_todo_ids: List[int]
    success: bool
    message: str


class BulkDeleteRequest(BaseRequest):
    """Request DTO for bulk deleting todos."""
    todo_ids: List[int]  # List of todo IDs to delete
    user_id: int  # For access control


class BulkDeleteResponse(BaseResponse):
    """Response DTO for bulk deleting todos."""
    deleted_count: int
    failed_count: int
    failed_todo_ids: List[int]
    success: bool
    message: str

