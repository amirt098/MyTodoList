# Standard library
from typing import Optional, List, Dict, Any

# Third-party
# (none needed)

# Internal - from other modules
from lib.base_models import BaseRequest, BaseResponse

# Internal - from same interface module
# (none needed)


class SavedFilterDTO(BaseResponse):
    """Pydantic DTO for SavedFilter."""
    filter_id: int
    name: str
    description: str
    filter_criteria: Dict[str, Any]
    user_id: int
    is_default: bool
    created_at: int
    updated_at: int


class SaveFilterRequest(BaseRequest):
    """Request DTO for saving a filter."""
    name: str
    description: Optional[str] = None
    filter_criteria: Dict[str, Any]  # JSON object with filter parameters
    user_id: int
    is_default: bool = False


class SaveFilterResponse(BaseResponse):
    """Response DTO for saving a filter."""
    filter_id: int
    name: str
    description: str
    filter_criteria: Dict[str, Any]
    created_at: int


class GetSavedFiltersRequest(BaseRequest):
    """Request DTO for getting saved filters."""
    user_id: int
    is_default: Optional[bool] = None


class GetSavedFiltersResponse(BaseResponse):
    """Response DTO for getting saved filters."""
    filters: List[SavedFilterDTO]
    total: int


class DeleteSavedFilterRequest(BaseRequest):
    """Request DTO for deleting a saved filter."""
    filter_id: int
    user_id: int  # For access control


class DeleteSavedFilterResponse(BaseResponse):
    """Response DTO for deleting a saved filter."""
    success: bool
    message: str

