# Standard library
from abc import ABC, abstractmethod

# Internal - from same interface module (direct import, no interface. prefix needed)
from .dataclasses import TodoDTO, TodoFilter, TodoCreateRequest, TodoUpdateRequest


class AbstractTodoRepository(ABC):
    """Interface for todo repository operations."""
    
    @abstractmethod
    def create(self, todo_data: TodoCreateRequest) -> TodoDTO:
        """
        Create a new todo in the database.
        
        Args:
            todo_data: TodoCreateRequest object with todo information (including created_at and updated_at timestamps)
            
        Returns:
            TodoDTO with created todo information
            
        Raises:
            TodoTitleRequiredException: If title is missing
        """
        pass
    
    @abstractmethod
    def get_by_id(self, todo_id: int) -> TodoDTO | None:
        """
        Get todo by ID.
        
        Args:
            todo_id: Todo ID to fetch
            
        Returns:
            TodoDTO if found, None otherwise
        """
        pass
    
    @abstractmethod
    def get_todos(self, filters: TodoFilter) -> list[TodoDTO]:
        """
        Get todos with filtering.
        
        General method for querying todos with various filters.
        
        Args:
            filters: TodoFilter Pydantic object extending BaseFilter from lib
            
        Returns:
            List of TodoDTO matching the filters
        """
        pass
    
    @abstractmethod
    def update(self, todo_id: int, todo_data: TodoUpdateRequest) -> TodoDTO:
        """
        Update an existing todo.
        
        Args:
            todo_id: Todo ID to update
            todo_data: TodoUpdateRequest with fields to update (only provided fields will be updated, including updated_at timestamp)
            
        Returns:
            TodoDTO with updated todo information
            
        Raises:
            TodoNotFoundByIdException: If todo doesn't exist
        """
        pass
    
    @abstractmethod
    def delete(self, todo_id: int) -> None:
        """
        Delete a todo.
        
        Args:
            todo_id: Todo ID to delete
            
        Raises:
            TodoNotFoundByIdException: If todo doesn't exist
        """
        pass


