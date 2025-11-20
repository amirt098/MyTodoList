# Standard library
from abc import ABC, abstractmethod

# Internal - from same interface module (direct import, no interface. prefix needed)
from .dataclasses import AnalyzeTextRequest, AnalyzeTextResponse, GenerateSuggestionsRequest, GenerateSuggestionsResponse


class AbstractLLMService(ABC):
    """Interface for LLM service operations."""
    
    @abstractmethod
    def analyze_text(self, request: AnalyzeTextRequest) -> AnalyzeTextResponse:
        """
        Analyze free text and extract todo information.
        
        Args:
            request: AnalyzeTextRequest with text and optional context
            
        Returns:
            AnalyzeTextResponse with suggested todos and detected intent
            
        Raises:
            LLMServiceUnavailableException: If LLM service is unavailable
        """
        pass
    
    @abstractmethod
    def generate_suggestions(self, request: GenerateSuggestionsRequest) -> GenerateSuggestionsResponse:
        """
        Generate suggestions based on a prompt.
        
        Args:
            request: GenerateSuggestionsRequest with prompt and context
            
        Returns:
            GenerateSuggestionsResponse with suggestions
            
        Raises:
            LLMServiceUnavailableException: If LLM service is unavailable
        """
        pass

