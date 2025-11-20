# Standard library
from abc import ABC, abstractmethod

# Internal - from same interface module (direct import, no interface. prefix needed)
from .dataclasses import SubtaskDTO, SubtaskFilter, SubtaskCreateRequest, SubtaskUpdateRequest


class AbstractSubtaskRepository(ABC):
    """Interface for subtask repository operations."""
    
    @abstractmethod
    def create(self, subtask_data: SubtaskCreateRequest) -> SubtaskDTO:
        """
        Create a new subtask in the database.
        
        Args:
            subtask_data: SubtaskCreateRequest object with subtask information (including created_at and updated_at timestamps)
            
        Returns:
            SubtaskDTO with created subtask information
            
        Raises:
            SubtaskTitleRequiredException: If title is missing
        """
        pass
    
    @abstractmethod
    def get_by_id(self, subtask_id: int) -> SubtaskDTO | None:
        """
        Get subtask by ID.
        
        Args:
            subtask_id: Subtask ID to fetch
            
        Returns:
            SubtaskDTO if found, None otherwise
        """
        pass
    
    @abstractmethod
    def get_subtasks(self, filters: SubtaskFilter) -> list[SubtaskDTO]:
        """
        Get subtasks with filtering.
        
        General method for querying subtasks with various filters.
        
        Args:
            filters: SubtaskFilter Pydantic object extending BaseFilter from lib
            
        Returns:
            List of SubtaskDTO matching the filters
        """
        pass
    
    @abstractmethod
    def update(self, subtask_id: int, subtask_data: SubtaskUpdateRequest) -> SubtaskDTO:
        """
        Update an existing subtask.
        
        Args:
            subtask_id: Subtask ID to update
            subtask_data: SubtaskUpdateRequest with fields to update (only provided fields will be updated, including updated_at timestamp)
            
        Returns:
            SubtaskDTO with updated subtask information
            
        Raises:
            SubtaskNotFoundByIdException: If subtask doesn't exist
        """
        pass
    
    @abstractmethod
    def delete(self, subtask_id: int) -> None:
        """
        Delete a subtask.
        
        Args:
            subtask_id: Subtask ID to delete
            
        Raises:
            SubtaskNotFoundByIdException: If subtask doesn't exist
        """
        pass

