# Standard library
from abc import ABC, abstractmethod

# Internal - from same interface module (direct import, no interface. prefix needed)
from .dataclasses import (
    SaveFilterRequest, SaveFilterResponse,
    GetSavedFiltersRequest, GetSavedFiltersResponse,
    DeleteSavedFilterRequest, DeleteSavedFilterResponse
)


class AbstractFilterManagementService(ABC):
    """Interface for filter management operations."""
    
    @abstractmethod
    def save_filter(self, request: SaveFilterRequest) -> SaveFilterResponse:
        """
        Save a filter for reuse.
        
        Args:
            request: SaveFilterRequest with filter name, description, criteria, and user_id
            
        Returns:
            SaveFilterResponse with saved filter information
            
        Raises:
            SavedFilterNameRequiredException: If name is missing
        """
        pass
    
    @abstractmethod
    def get_saved_filters(self, request: GetSavedFiltersRequest) -> GetSavedFiltersResponse:
        """
        Get user's saved filters.
        
        Args:
            request: GetSavedFiltersRequest with user_id and optional is_default filter
            
        Returns:
            GetSavedFiltersResponse with list of saved filters
        """
        pass
    
    @abstractmethod
    def delete_saved_filter(self, request: DeleteSavedFilterRequest) -> DeleteSavedFilterResponse:
        """
        Delete a saved filter.
        
        Args:
            request: DeleteSavedFilterRequest with filter_id and user_id
            
        Returns:
            DeleteSavedFilterResponse with success status
            
        Raises:
            SavedFilterNotFoundByIdException: If filter doesn't exist
            SavedFilterAccessDeniedException: If user doesn't have access
        """
        pass

