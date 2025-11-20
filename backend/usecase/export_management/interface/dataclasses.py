# Standard library
from typing import Optional

# Third-party
# (none needed)

# Internal - from other modules
from lib.base_models import BaseRequest, BaseResponse

# Internal - from same interface module
# (none needed)


class ExportTodosRequest(BaseRequest):
    """Request DTO for exporting todos."""
    user_id: int
    format: str = 'json'  # 'json' or 'csv'
    # Filter criteria (same as TodoFilter)
    project_id: Optional[int] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    category: Optional[str] = None
    label: Optional[str] = None


class ExportTodosResponse(BaseResponse):
    """Response DTO for exporting todos."""
    format: str
    content: str  # JSON string or CSV string
    total_todos: int
    filename: str  # Suggested filename

