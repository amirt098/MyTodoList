# Standard library
from abc import ABC, abstractmethod

# Internal - from same interface module (direct import, no interface. prefix needed)
from .dataclasses import (
    AnalyzeFreeTextRequest, AnalyzeFreeTextResponse,
    CreateSmartTodoRequest, CreateSmartTodoResponse,
    AutoCategorizeRequest, AutoCategorizeResponse,
    SuggestSubtasksRequest, SuggestSubtasksResponse,
    SuggestNextActionRequest, SuggestNextActionResponse,
    ConversationalQueryRequest, ConversationalQueryResponse
)


class AbstractSmartTodoManagementService(ABC):
    """Interface for smart todo management operations."""
    
    @abstractmethod
    def analyze_free_text(self, request: AnalyzeFreeTextRequest) -> AnalyzeFreeTextResponse:
        """
        Analyze free text and return structured suggestions.
        
        Args:
            request: AnalyzeFreeTextRequest with text and user_id
            
        Returns:
            AnalyzeFreeTextResponse with suggested todos and detected intent
            
        Raises:
            InvalidTextException: If text is invalid
            LLMServiceUnavailableException: If LLM service is unavailable
        """
        pass
    
    @abstractmethod
    def create_smart_todo(self, request: CreateSmartTodoRequest) -> CreateSmartTodoResponse:
        """
        Create a todo using AI suggestions.
        
        Args:
            request: CreateSmartTodoRequest with suggestion and user_id
            
        Returns:
            CreateSmartTodoResponse with created todo information
        """
        pass
    
    @abstractmethod
    def auto_categorize(self, request: AutoCategorizeRequest) -> AutoCategorizeResponse:
        """
        Auto-categorize a todo based on title and description.
        
        Args:
            request: AutoCategorizeRequest with title, description, and user_id
            
        Returns:
            AutoCategorizeResponse with suggested category, labels, and priority
        """
        pass
    
    @abstractmethod
    def suggest_subtasks(self, request: SuggestSubtasksRequest) -> SuggestSubtasksResponse:
        """
        Suggest subtasks for a todo.
        
        Args:
            request: SuggestSubtasksRequest with todo information and user_id
            
        Returns:
            SuggestSubtasksResponse with suggested subtasks
        """
        pass
    
    @abstractmethod
    def suggest_next_action(self, request: SuggestNextActionRequest) -> SuggestNextActionResponse:
        """
        Suggest next action for a user.
        
        Args:
            request: SuggestNextActionRequest with user_id and optional context
            
        Returns:
            SuggestNextActionResponse with suggested actions
        """
        pass
    
    @abstractmethod
    def conversational_query(self, request: ConversationalQueryRequest) -> ConversationalQueryResponse:
        """
        Handle conversational queries ("What should I do today?").
        
        Args:
            request: ConversationalQueryRequest with query and user_id
            
        Returns:
            ConversationalQueryResponse with response and suggestions
        """
        pass

