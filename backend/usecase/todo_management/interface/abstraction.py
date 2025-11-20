# Standard library
from abc import ABC, abstractmethod

# Internal - from same interface module (direct import, no interface. prefix needed)
from .dataclasses import (
    CreateTodoRequest, CreateTodoResponse,
    GetTodoRequest, TodoDTO,
    TodoFilter, TodoListResponse,
    GetAllMyTodosRequest,
    UpdateTodoRequest, UpdateTodoResponse,
    DeleteTodoRequest, DeleteTodoResponse
)


class AbstractTodoManagementService(ABC):
    """Interface for todo management operations."""
    
    @abstractmethod
    def create_todo(self, request: CreateTodoRequest) -> CreateTodoResponse:
        """
        Create a new todo.
        
        Args:
            request: CreateTodoRequest with todo information and user_id
            
        Returns:
            CreateTodoResponse with created todo information
            
        Raises:
            TodoTitleRequiredException: If title is missing
        """
        pass
    
    @abstractmethod
    def get_todo_by_id(self, request: GetTodoRequest) -> TodoDTO:
        """
        Get a single todo by ID.
        
        Args:
            request: GetTodoRequest with todo_id and user_id
            
        Returns:
            TodoDTO with todo information
            
        Raises:
            TodoNotFoundByIdException: If todo doesn't exist
            TodoAccessDeniedException: If user doesn't have access to todo
        """
        pass
    
    @abstractmethod
    def get_todos(self, request: TodoFilter) -> TodoListResponse:
        """
        Get todos with filtering.
        
        Args:
            request: TodoFilter with filters and user_id
            
        Returns:
            TodoListResponse with list of todos and total count
        """
        pass
    
    @abstractmethod
    def get_all_my_todos(self, request: GetAllMyTodosRequest) -> TodoListResponse:
        """
        Get all my todos (unified view - combines personal and project todos).
        
        Args:
            request: GetAllMyTodosRequest with user_id and optional filters
            
        Returns:
            TodoListResponse with list of all todos (personal + project) and total count
        """
        pass
    
    @abstractmethod
    def update_todo(self, request: UpdateTodoRequest) -> UpdateTodoResponse:
        """
        Update an existing todo.
        
        Args:
            request: UpdateTodoRequest with todo_id, user_id, and fields to update
            
        Returns:
            UpdateTodoResponse with updated todo information
            
        Raises:
            TodoNotFoundByIdException: If todo doesn't exist
            TodoAccessDeniedException: If user doesn't have access to todo
        """
        pass
    
    @abstractmethod
    def delete_todo(self, request: DeleteTodoRequest) -> DeleteTodoResponse:
        """
        Delete a todo.
        
        Args:
            request: DeleteTodoRequest with todo_id and user_id
            
        Returns:
            DeleteTodoResponse with success status
            
        Raises:
            TodoNotFoundByIdException: If todo doesn't exist
            TodoAccessDeniedException: If user doesn't have access to todo
        """
        pass
