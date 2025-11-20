# Standard library
from abc import ABC, abstractmethod

# Internal - from same interface module (direct import, no interface. prefix needed)
from .dataclasses import BulkUpdateRequest, BulkUpdateResponse, BulkDeleteRequest, BulkDeleteResponse


class AbstractBulkOperationsService(ABC):
    """Interface for bulk operations."""
    
    @abstractmethod
    def bulk_update(self, request: BulkUpdateRequest) -> BulkUpdateResponse:
        """
        Update multiple todos at once.
        
        Args:
            request: BulkUpdateRequest with todo_ids, user_id, and fields to update
            
        Returns:
            BulkUpdateResponse with update results
            
        Raises:
            EmptyTodoListException: If todo_ids list is empty
        """
        pass
    
    @abstractmethod
    def bulk_delete(self, request: BulkDeleteRequest) -> BulkDeleteResponse:
        """
        Delete multiple todos at once.
        
        Args:
            request: BulkDeleteRequest with todo_ids and user_id
            
        Returns:
            BulkDeleteResponse with delete results
            
        Raises:
            EmptyTodoListException: If todo_ids list is empty
        """
        pass

