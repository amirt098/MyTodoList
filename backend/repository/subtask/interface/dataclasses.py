# Standard library
from typing import Optional

# Third-party
# (none needed)

# Internal - from other modules
from lib.base_models import BaseModel, BaseFilter

# Internal - from same interface module
# (none needed)


class SubtaskCreateRequest(BaseModel):
    """Request for creating a subtask."""
    title: str
    status: str = 'ToDo'
    todo_id: int
    order: int = 0
    created_at: int | None = None
    updated_at: int | None = None
    completed_at_timestamp_ms: Optional[int] = None


class SubtaskUpdateRequest(BaseModel):
    """Request for updating a subtask."""
    title: str | None = None
    status: str | None = None
    order: int | None = None
    updated_at: int | None = None
    completed_at_timestamp_ms: Optional[int] = None


class SubtaskDTO(BaseModel):
    """DTO for Subtask responses."""
    subtask_id: int
    title: str
    status: str
    todo_id: int
    order: int
    created_at: int
    updated_at: int
    completed_at_timestamp_ms: Optional[int] = None
    
    @classmethod
    def from_model(cls, subtask) -> 'SubtaskDTO':
        """Create SubtaskDTO from Django Subtask model."""
        return cls(
            subtask_id=subtask.id,
            title=subtask.title,
            status=subtask.status,
            todo_id=subtask.todo_id,
            order=subtask.order,
            created_at=subtask.created_at,
            updated_at=subtask.updated_at,
            completed_at_timestamp_ms=subtask.completed_at
        )


class SubtaskFilter(BaseFilter):
    """Filter for querying subtasks."""
    todo_id: Optional[int] = None
    status: Optional[str] = None

