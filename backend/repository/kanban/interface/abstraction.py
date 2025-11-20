# Standard library
from abc import ABC, abstractmethod

# Internal - from same interface module (direct import, no interface. prefix needed)
from .dataclasses import KanbanColumnDTO, KanbanColumnFilter, KanbanColumnCreateRequest, KanbanColumnUpdateRequest


class AbstractKanbanRepository(ABC):
    """Interface for kanban repository operations."""
    
    @abstractmethod
    def create_column(self, column_data: KanbanColumnCreateRequest) -> KanbanColumnDTO:
        """
        Create a new kanban column in the database.
        
        Args:
            column_data: KanbanColumnCreateRequest object with column information (including created_at and updated_at timestamps)
            
        Returns:
            KanbanColumnDTO with created column information
            
        Raises:
            KanbanColumnNameRequiredException: If name is missing
        """
        pass
    
    @abstractmethod
    def get_column_by_id(self, column_id: int) -> KanbanColumnDTO | None:
        """
        Get kanban column by ID.
        
        Args:
            column_id: Column ID to fetch
            
        Returns:
            KanbanColumnDTO if found, None otherwise
        """
        pass
    
    @abstractmethod
    def get_columns(self, filters: KanbanColumnFilter) -> list[KanbanColumnDTO]:
        """
        Get kanban columns with filtering.
        
        General method for querying columns with various filters.
        
        Args:
            filters: KanbanColumnFilter Pydantic object extending BaseFilter from lib
            
        Returns:
            List of KanbanColumnDTO matching the filters
        """
        pass
    
    @abstractmethod
    def update_column(self, column_id: int, column_data: KanbanColumnUpdateRequest) -> KanbanColumnDTO:
        """
        Update an existing kanban column.
        
        Args:
            column_id: Column ID to update
            column_data: KanbanColumnUpdateRequest with fields to update (only provided fields will be updated, including updated_at timestamp)
            
        Returns:
            KanbanColumnDTO with updated column information
            
        Raises:
            KanbanColumnNotFoundByIdException: If column doesn't exist
        """
        pass
    
    @abstractmethod
    def delete_column(self, column_id: int) -> None:
        """
        Delete a kanban column.
        
        Args:
            column_id: Column ID to delete
            
        Raises:
            KanbanColumnNotFoundByIdException: If column doesn't exist
        """
        pass

