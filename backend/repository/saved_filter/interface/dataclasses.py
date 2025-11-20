# Standard library
from typing import Optional, Dict, Any

# Third-party
# (none needed)

# Internal - from other modules
from lib.base_models import BaseModel, BaseFilter

# Internal - from same interface module
# (none needed)


class SavedFilterCreateRequest(BaseModel):
    """Request for creating a saved filter."""
    name: str
    description: Optional[str] = None
    filter_criteria: Dict[str, Any]  # JSON object with filter parameters
    user_id: int
    is_default: bool = False
    created_at: int | None = None
    updated_at: int | None = None


class SavedFilterUpdateRequest(BaseModel):
    """Request for updating a saved filter."""
    name: str | None = None
    description: str | None = None
    filter_criteria: Dict[str, Any] | None = None
    is_default: bool | None = None
    updated_at: int | None = None


class SavedFilterDTO(BaseModel):
    """DTO for SavedFilter responses."""
    filter_id: int
    name: str
    description: str
    filter_criteria: Dict[str, Any]
    user_id: int
    is_default: bool
    created_at: int
    updated_at: int
    
    @classmethod
    def from_model(cls, saved_filter) -> 'SavedFilterDTO':
        """Create SavedFilterDTO from Django SavedFilter model."""
        return cls(
            filter_id=saved_filter.id,
            name=saved_filter.name,
            description=saved_filter.description or "",
            filter_criteria=saved_filter.filter_criteria or {},
            user_id=saved_filter.user_id,
            is_default=saved_filter.is_default,
            created_at=saved_filter.created_at,
            updated_at=saved_filter.updated_at
        )


class SavedFilterFilter(BaseFilter):
    """Filter for querying saved filters."""
    user_id: Optional[int] = None
    is_default: Optional[bool] = None

