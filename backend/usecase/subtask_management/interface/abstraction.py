# Standard library
from abc import ABC, abstractmethod

# Internal - from same interface module (direct import, no interface. prefix needed)
from .dataclasses import (
    AddSubtaskRequest, AddSubtaskResponse,
    UpdateSubtaskRequest, UpdateSubtaskResponse,
    DeleteSubtaskRequest, DeleteSubtaskResponse,
    MarkSubtaskDoneRequest, MarkSubtaskDoneResponse,
    GetSubtasksRequest, GetSubtasksResponse
)


class AbstractSubtaskManagementService(ABC):
    """Interface for subtask management operations."""
    
    @abstractmethod
    def add_subtask(self, request: AddSubtaskRequest) -> AddSubtaskResponse:
        """
        Add a subtask to a todo.
        
        Args:
            request: AddSubtaskRequest with todo_id, title, user_id, and optional order
            
        Returns:
            AddSubtaskResponse with created subtask information
            
        Raises:
            TodoNotFoundByIdException: If todo doesn't exist
            TodoAccessDeniedException: If user doesn't have access to todo
            SubtaskTitleRequiredException: If title is missing
        """
        pass
    
    @abstractmethod
    def update_subtask(self, request: UpdateSubtaskRequest) -> UpdateSubtaskResponse:
        """
        Update an existing subtask.
        
        Args:
            request: UpdateSubtaskRequest with subtask_id, todo_id, user_id, and fields to update
            
        Returns:
            UpdateSubtaskResponse with updated subtask information
            
        Raises:
            SubtaskNotFoundByIdException: If subtask doesn't exist
            TodoAccessDeniedException: If user doesn't have access to todo
        """
        pass
    
    @abstractmethod
    def delete_subtask(self, request: DeleteSubtaskRequest) -> DeleteSubtaskResponse:
        """
        Delete a subtask.
        
        Args:
            request: DeleteSubtaskRequest with subtask_id, todo_id, and user_id
            
        Returns:
            DeleteSubtaskResponse with success status
            
        Raises:
            SubtaskNotFoundByIdException: If subtask doesn't exist
            TodoAccessDeniedException: If user doesn't have access to todo
        """
        pass
    
    @abstractmethod
    def mark_subtask_done(self, request: MarkSubtaskDoneRequest) -> MarkSubtaskDoneResponse:
        """
        Mark a subtask as done or undone.
        
        Args:
            request: MarkSubtaskDoneRequest with subtask_id, todo_id, user_id, and done flag
            
        Returns:
            MarkSubtaskDoneResponse with updated subtask status
            
        Raises:
            SubtaskNotFoundByIdException: If subtask doesn't exist
            TodoAccessDeniedException: If user doesn't have access to todo
        """
        pass
    
    @abstractmethod
    def get_subtasks(self, request: GetSubtasksRequest) -> GetSubtasksResponse:
        """
        Get subtasks for a todo with progress calculation.
        
        Args:
            request: GetSubtasksRequest with todo_id, user_id, and optional status filter
            
        Returns:
            GetSubtasksResponse with subtasks list and progress percentage
            
        Raises:
            TodoNotFoundByIdException: If todo doesn't exist
            TodoAccessDeniedException: If user doesn't have access to todo
        """
        pass

