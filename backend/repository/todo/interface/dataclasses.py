# Standard library
from typing import Optional, List

# Third-party
# (none needed)

# Internal - from other modules
from lib.base_models import BaseModel, BaseFilter

# Internal - from same interface module
# (none needed)


class TodoCreateRequest(BaseModel):
    """Request for creating a todo."""
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
    created_at: int | None = None
    updated_at: int | None = None
    completed_at_timestamp_ms: Optional[int] = None
    auto_repeat: str = 'None'


class TodoUpdateRequest(BaseModel):
    """Request for updating a todo."""
    title: str | None = None
    description: str | None = None
    deadline_timestamp_ms: int | None = None
    priority: str | None = None
    status: str | None = None
    category: str | None = None
    labels: List[str] | None = None
    project_id: int | None = None
    previous_todo_id: int | None = None
    next_todo_id: int | None = None
    order: int | None = None
    created_at: int | None = None
    updated_at: int | None = None
    completed_at_timestamp_ms: int | None = None
    auto_repeat: str | None = None


class TodoDTO(BaseModel):
    """DTO for Todo responses."""
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
    
    @classmethod
    def from_model(cls, todo) -> 'TodoDTO':
        """Create TodoDTO from Django Todo model."""
        return cls(
            todo_id=todo.id,
            title=todo.title,
            description=todo.description or "",
            deadline_timestamp_ms=todo.deadline,
            priority=todo.priority,
            status=todo.status,
            category=todo.category or "",
            labels=todo.labels if todo.labels else [],
            user_id=todo.user_id,
            project_id=todo.project_id,
            previous_todo_id=todo.previous_todo_id,
            next_todo_id=todo.next_todo_id,
            order=todo.order,
            created_at=todo.created_at,
            updated_at=todo.updated_at,
            completed_at_timestamp_ms=todo.completed_at,
            auto_repeat=todo.auto_repeat
        )


class TodoFilter(BaseFilter):
    """Filter for querying todos."""
    user_id: Optional[int] = None
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
