# Standard library
from abc import ABC, abstractmethod

# Internal - from same interface module (direct import, no interface. prefix needed)
from .dataclasses import (
    GetKanbanBoardRequest, GetKanbanBoardResponse,
    MoveTodoRequest, MoveTodoResponse,
    CreateColumnRequest, CreateColumnResponse,
    DeleteColumnRequest, DeleteColumnResponse,
    ReorderColumnsRequest, ReorderColumnsResponse
)


class AbstractKanbanManagementService(ABC):
    """Interface for kanban management operations."""
    
    @abstractmethod
    def get_kanban_board(self, request: GetKanbanBoardRequest) -> GetKanbanBoardResponse:
        """
        Get kanban board with todos organized by columns.
        
        Args:
            request: GetKanbanBoardRequest with project_id (optional) and user_id
            
        Returns:
            GetKanbanBoardResponse with columns and cards
        """
        pass
    
    @abstractmethod
    def move_todo(self, request: MoveTodoRequest) -> MoveTodoResponse:
        """
        Move todo between columns (updates status).
        
        Args:
            request: MoveTodoRequest with todo_id, new_status, user_id, and optional new_order
            
        Returns:
            MoveTodoResponse with old and new status
            
        Raises:
            TodoNotFoundByIdException: If todo doesn't exist
        """
        pass
    
    @abstractmethod
    def create_column(self, request: CreateColumnRequest) -> CreateColumnResponse:
        """
        Create a custom kanban column.
        
        Args:
            request: CreateColumnRequest with column information
            
        Returns:
            CreateColumnResponse with created column information
            
        Raises:
            KanbanColumnNameRequiredException: If name is missing
        """
        pass
    
    @abstractmethod
    def delete_column(self, request: DeleteColumnRequest) -> DeleteColumnResponse:
        """
        Delete a kanban column.
        
        Args:
            request: DeleteColumnRequest with column_id and user_id
            
        Returns:
            DeleteColumnResponse with success status
            
        Raises:
            KanbanColumnNotFoundByIdException: If column doesn't exist
        """
        pass
    
    @abstractmethod
    def reorder_columns(self, request: ReorderColumnsRequest) -> ReorderColumnsResponse:
        """
        Reorder kanban columns.
        
        Args:
            request: ReorderColumnsRequest with column_orders list and user_id
            
        Returns:
            ReorderColumnsResponse with success status
        """
        pass

