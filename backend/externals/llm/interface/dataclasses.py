# Standard library
from typing import Optional, List, Dict, Any

# Third-party
# (none needed)

# Internal - from other modules
from lib.base_models import BaseRequest, BaseResponse

# Internal - from same interface module
# (none needed)


class AnalyzeTextRequest(BaseRequest):
    """Request DTO for analyzing free text."""
    text: str
    context: Optional[Dict[str, Any]] = None  # Additional context (user_id, existing todos, etc.)


class TodoSuggestion(BaseResponse):
    """DTO for a suggested todo from AI analysis."""
    title: str
    description: Optional[str] = None
    priority: str = 'Medium'
    category: Optional[str] = None
    labels: List[str] = []
    suggested_deadline: Optional[int] = None  # Timestamp in ms
    suggested_project_id: Optional[int] = None
    suggested_subtasks: List[str] = []
    confidence: float = 0.0  # 0.0 to 1.0


class AnalyzeTextResponse(BaseResponse):
    """Response DTO for analyzing free text."""
    suggestions: List[TodoSuggestion]
    detected_intent: str  # 'create_todo', 'query', 'update', etc.
    confidence: float
    raw_response: Optional[str] = None  # Raw LLM response for debugging


class GenerateSuggestionsRequest(BaseRequest):
    """Request DTO for generating suggestions."""
    prompt: str
    context: Optional[Dict[str, Any]] = None
    max_suggestions: int = 5


class GenerateSuggestionsResponse(BaseResponse):
    """Response DTO for generating suggestions."""
    suggestions: List[str]
    confidence: float

