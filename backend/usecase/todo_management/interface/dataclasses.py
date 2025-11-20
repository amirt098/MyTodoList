# Standard library
from typing import Optional, List

# Third-party
# (none needed)

# Internal - from other modules
from lib.base_models import BaseRequest, BaseResponse, BaseFilter

# Internal - from same interface module
# (none needed)


class CreateTodoRequest(BaseRequest):
    """Request DTO for creating a todo."""
    title: str
    description: Optional[str] = None
    deadline_timestamp_ms: Optional[int] = None
    priority: str = 'Medium'
    status: str = 'ToDo'
    category: Optional[str] = None
    labels: Optional[List[str]] = None
    user_id: int
    project_id: Optional[int] = None
    previous_todo_id: Optional[int] = None
    next_todo_id: Optional[int] = None
    order: int = 0
    auto_repeat: str = 'None'


class CreateTodoResponse(BaseResponse):
    """Response DTO for creating a todo."""
    todo_id: int
    title: str
    status: str
    user_id: int
    created_at: int


class GetTodoRequest(BaseRequest):
    """Request DTO for getting a todo."""
    todo_id: int
    user_id: int  # For access control


class TodoDTO(BaseResponse):
    """Pydantic DTO for Todo (used in get responses)."""
    todo_id: int
    title: str
    description: str
    deadline_timestamp_ms: Optional[int] = None
    priority: str
    status: str
    category: str
    labels: List[str]
    user_id: int
    project_id: Optional[int] = None
    previous_todo_id: Optional[int] = None
    next_todo_id: Optional[int] = None
    order: int
    created_at: int
    updated_at: int
    completed_at_timestamp_ms: Optional[int] = None
    auto_repeat: str
    progress: float = 0.0  # Progress percentage (0-100) based on subtasks


class TodoFilter(BaseFilter):
    """Filter for querying todos (extends BaseFilter)."""
    user_id: int
    project_id: Optional[int] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    category: Optional[str] = None
    label: Optional[str] = None
    deadline_after__gte: int | None = None
    deadline_after__lte: int | None = None
    deadline_before__gte: int | None = None
    deadline_before__lte: int | None = None
    created_after__gte: int | None = None
    created_after__lte: int | None = None
    created_before__gte: int | None = None
    created_before__lte: int | None = None
    search: Optional[str] = None


class TodoListResponse(BaseResponse):
    """Response DTO for getting todos list."""
    todos: List[TodoDTO]
    total: int


class GetAllMyTodosRequest(BaseRequest):
    """Request DTO for getting all my todos (unified view)."""
    user_id: int
    # Optional filters
    status: Optional[str] = None
    priority: Optional[str] = None
    category: Optional[str] = None
    label: Optional[str] = None
    deadline_after__gte: Optional[int] = None
    deadline_after__lte: Optional[int] = None
    search: Optional[str] = None
    order_by: str = '-created_at'
    limit: Optional[int] = None
    offset: Optional[int] = None


class UpdateTodoRequest(BaseRequest):
    """Request DTO for updating a todo."""
    todo_id: int
    user_id: int
    title: Optional[str] = None
    description: Optional[str] = None
    deadline_timestamp_ms: Optional[int] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    category: Optional[str] = None
    labels: Optional[List[str]] = None
    project_id: Optional[int] = None
    previous_todo_id: Optional[int] = None
    next_todo_id: Optional[int] = None
    order: Optional[int] = None
    auto_repeat: Optional[str] = None
    completed_at_timestamp_ms: Optional[int] = None


class UpdateTodoResponse(BaseResponse):
    """Response DTO for updating a todo."""
    todo_id: int
    title: str
    description: str
    deadline_timestamp_ms: Optional[int] = None
    priority: str
    status: str
    category: str
    labels: List[str]
    user_id: int
    project_id: Optional[int] = None
    updated_at: int


class DeleteTodoRequest(BaseRequest):
    """Request DTO for deleting a todo."""
    todo_id: int
    user_id: int  # For access control


class DeleteTodoResponse(BaseResponse):
    """Response DTO for deleting a todo."""
    success: bool
    message: str
