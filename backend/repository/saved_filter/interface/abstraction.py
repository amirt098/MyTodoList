# Standard library
from abc import ABC, abstractmethod

# Internal - from same interface module (direct import, no interface. prefix needed)
from .dataclasses import SavedFilterDTO, SavedFilterFilter, SavedFilterCreateRequest, SavedFilterUpdateRequest


class AbstractSavedFilterRepository(ABC):
    """Interface for saved filter repository operations."""
    
    @abstractmethod
    def create(self, filter_data: SavedFilterCreateRequest) -> SavedFilterDTO:
        """
        Create a new saved filter in the database.
        
        Args:
            filter_data: SavedFilterCreateRequest object with filter information (including created_at and updated_at timestamps)
            
        Returns:
            SavedFilterDTO with created filter information
            
        Raises:
            SavedFilterNameRequiredException: If name is missing
        """
        pass
    
    @abstractmethod
    def get_by_id(self, filter_id: int) -> SavedFilterDTO | None:
        """
        Get saved filter by ID.
        
        Args:
            filter_id: Filter ID to fetch
            
        Returns:
            SavedFilterDTO if found, None otherwise
        """
        pass
    
    @abstractmethod
    def get_filters(self, filters: SavedFilterFilter) -> list[SavedFilterDTO]:
        """
        Get saved filters with filtering.
        
        General method for querying saved filters with various filters.
        
        Args:
            filters: SavedFilterFilter Pydantic object extending BaseFilter from lib
            
        Returns:
            List of SavedFilterDTO matching the filters
        """
        pass
    
    @abstractmethod
    def update(self, filter_id: int, filter_data: SavedFilterUpdateRequest) -> SavedFilterDTO:
        """
        Update an existing saved filter.
        
        Args:
            filter_id: Filter ID to update
            filter_data: SavedFilterUpdateRequest with fields to update (only provided fields will be updated, including updated_at timestamp)
            
        Returns:
            SavedFilterDTO with updated filter information
            
        Raises:
            SavedFilterNotFoundByIdException: If filter doesn't exist
        """
        pass
    
    @abstractmethod
    def delete(self, filter_id: int) -> None:
        """
        Delete a saved filter.
        
        Args:
            filter_id: Filter ID to delete
            
        Raises:
            SavedFilterNotFoundByIdException: If filter doesn't exist
        """
        pass

