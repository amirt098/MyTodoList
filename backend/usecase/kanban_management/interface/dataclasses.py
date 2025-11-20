# Standard library
from typing import Optional, List

# Third-party
# (none needed)

# Internal - from other modules
from lib.base_models import BaseRequest, BaseResponse

# Internal - from same interface module
# (none needed)


class KanbanColumnDTO(BaseResponse):
    """Pydantic DTO for KanbanColumn."""
    column_id: int
    name: str
    status_value: str
    color: str
    project_id: Optional[int] = None
    user_id: Optional[int] = None
    order: int
    is_default: bool
    is_active: bool


class KanbanCardDTO(BaseResponse):
    """Pydantic DTO for Todo as Kanban Card."""
    todo_id: int
    title: str
    description: str
    priority: str
    status: str
    labels: List[str]
    deadline_timestamp_ms: Optional[int] = None
    project_id: Optional[int] = None
    order: int
    progress: float = 0.0  # Progress percentage (0-100)


class GetKanbanBoardRequest(BaseRequest):
    """Request DTO for getting kanban board."""
    project_id: Optional[int] = None  # None = personal board
    user_id: int


class GetKanbanBoardResponse(BaseResponse):
    """Response DTO for kanban board."""
    columns: List[KanbanColumnDTO]
    cards: List[KanbanCardDTO]  # All cards, organized by column in frontend
    project_id: Optional[int] = None


class MoveTodoRequest(BaseRequest):
    """Request DTO for moving todo between columns."""
    todo_id: int
    new_status: str  # New status value (maps to column)
    user_id: int  # For access control
    new_order: Optional[int] = None  # Optional new order within column


class MoveTodoResponse(BaseResponse):
    """Response DTO for moving todo."""
    todo_id: int
    old_status: str
    new_status: str
    success: bool


class CreateColumnRequest(BaseRequest):
    """Request DTO for creating a kanban column."""
    name: str
    status_value: Optional[str] = None
    color: Optional[str] = None
    project_id: Optional[int] = None
    user_id: int
    order: Optional[int] = None


class CreateColumnResponse(BaseResponse):
    """Response DTO for creating a column."""
    column_id: int
    name: str
    status_value: str
    color: str
    order: int


class DeleteColumnRequest(BaseRequest):
    """Request DTO for deleting a kanban column."""
    column_id: int
    user_id: int  # For access control


class DeleteColumnResponse(BaseResponse):
    """Response DTO for deleting a column."""
    success: bool
    message: str


class ReorderColumnsRequest(BaseRequest):
    """Request DTO for reordering columns."""
    column_orders: List[dict]  # [{"column_id": 1, "order": 0}, ...]
    project_id: Optional[int] = None
    user_id: int


class ReorderColumnsResponse(BaseResponse):
    """Response DTO for reordering columns."""
    success: bool
    message: str

