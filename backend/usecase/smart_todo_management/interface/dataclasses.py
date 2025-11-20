# Standard library
from typing import Optional, List

# Third-party
# (none needed)

# Internal - from other modules
from lib.base_models import BaseRequest, BaseResponse

# Internal - from same interface module
# (none needed)


class TodoSuggestion(BaseResponse):
    """DTO for a suggested todo from AI analysis."""
    title: str
    description: Optional[str] = None
    priority: str = 'Medium'
    category: Optional[str] = None
    labels: List[str] = []
    suggested_deadline: Optional[int] = None
    suggested_project_id: Optional[int] = None
    suggested_subtasks: List[str] = []
    confidence: float = 0.0


class AnalyzeFreeTextRequest(BaseRequest):
    """Request DTO for analyzing free text."""
    text: str
    user_id: int
    context: Optional[dict] = None  # Additional context


class AnalyzeFreeTextResponse(BaseResponse):
    """Response DTO for analyzing free text."""
    suggestions: List[TodoSuggestion]
    detected_intent: str
    confidence: float


class CreateSmartTodoRequest(BaseRequest):
    """Request DTO for creating a todo using AI suggestions."""
    suggestion: TodoSuggestion
    user_id: int
    accept_suggestion: bool = True  # If False, user will edit before creating


class CreateSmartTodoResponse(BaseResponse):
    """Response DTO for creating a smart todo."""
    todo_id: int
    title: str
    created_at: int


class AutoCategorizeRequest(BaseRequest):
    """Request DTO for auto-categorizing a todo."""
    title: str
    description: Optional[str] = None
    user_id: int


class AutoCategorizeResponse(BaseResponse):
    """Response DTO for auto-categorizing."""
    category: Optional[str] = None
    labels: List[str] = []
    priority: str = 'Medium'
    confidence: float = 0.0


class SuggestSubtasksRequest(BaseRequest):
    """Request DTO for suggesting subtasks."""
    todo_title: str
    todo_description: Optional[str] = None
    user_id: int
    max_subtasks: int = 5


class SuggestSubtasksResponse(BaseResponse):
    """Response DTO for suggesting subtasks."""
    subtasks: List[str]
    confidence: float


class SuggestNextActionRequest(BaseRequest):
    """Request DTO for suggesting next action."""
    user_id: int
    context: Optional[dict] = None  # Current todos, projects, etc.


class SuggestNextActionResponse(BaseResponse):
    """Response DTO for suggesting next action."""
    suggestions: List[str]
    confidence: float


class ConversationalQueryRequest(BaseRequest):
    """Request DTO for conversational query."""
    query: str
    user_id: int
    context: Optional[dict] = None


class ConversationalQueryResponse(BaseResponse):
    """Response DTO for conversational query."""
    response: str
    suggestions: List[TodoSuggestion] = []
    detected_intent: str
    confidence: float

