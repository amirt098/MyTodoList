# Standard library
from typing import Optional

# Third-party
# (none needed)

# Internal - from other modules
from lib.base_models import BaseModel, BaseFilter

# Internal - from same interface module
# (none needed)


class KanbanColumnCreateRequest(BaseModel):
    """Request for creating a kanban column."""
    name: str
    status_value: Optional[str] = None
    color: Optional[str] = None
    project_id: Optional[int] = None
    user_id: Optional[int] = None
    order: int = 0
    is_default: bool = False
    is_active: bool = True
    created_at: int | None = None
    updated_at: int | None = None


class KanbanColumnUpdateRequest(BaseModel):
    """Request for updating a kanban column."""
    name: str | None = None
    status_value: str | None = None
    color: str | None = None
    order: int | None = None
    is_active: bool | None = None
    updated_at: int | None = None


class KanbanColumnDTO(BaseModel):
    """DTO for KanbanColumn responses."""
    column_id: int
    name: str
    status_value: str
    color: str
    project_id: Optional[int] = None
    user_id: Optional[int] = None
    order: int
    is_default: bool
    is_active: bool
    created_at: int
    updated_at: int
    
    @classmethod
    def from_model(cls, column) -> 'KanbanColumnDTO':
        """Create KanbanColumnDTO from Django KanbanColumn model."""
        return cls(
            column_id=column.id,
            name=column.name,
            status_value=column.status_value or "",
            color=column.color or "#6B7280",
            project_id=column.project_id,
            user_id=column.user_id,
            order=column.order,
            is_default=column.is_default,
            is_active=column.is_active,
            created_at=column.created_at,
            updated_at=column.updated_at
        )


class KanbanColumnFilter(BaseFilter):
    """Filter for querying kanban columns."""
    project_id: Optional[int] = None
    user_id: Optional[int] = None
    is_default: Optional[bool] = None
    is_active: Optional[bool] = None

