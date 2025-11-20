# Standard library
from abc import ABC, abstractmethod

# Internal - from same interface module (direct import, no interface. prefix needed)
from .dataclasses import (
    SetDependencyRequest, SetDependencyResponse,
    RemoveDependencyRequest, RemoveDependencyResponse,
    ValidateDependencyRequest, ValidateDependencyResponse,
    GetDependencyChainRequest, GetDependencyChainResponse
)


class AbstractTodoDependencyManagementService(ABC):
    """Interface for todo dependency management operations."""
    
    @abstractmethod
    def set_dependency(self, request: SetDependencyRequest) -> SetDependencyResponse:
        """
        Set a todo dependency (previous or next).
        
        Args:
            request: SetDependencyRequest with todo_id, dependency_type, dependency_todo_id, and user_id
            
        Returns:
            SetDependencyResponse with dependency information
            
        Raises:
            TodoNotFoundByIdException: If todo doesn't exist
            TodoAccessDeniedException: If user doesn't have access to todo
            CircularDependencyException: If circular dependency is detected
            InvalidDependencyException: If dependency is invalid
        """
        pass
    
    @abstractmethod
    def remove_dependency(self, request: RemoveDependencyRequest) -> RemoveDependencyResponse:
        """
        Remove a todo dependency.
        
        Args:
            request: RemoveDependencyRequest with todo_id, dependency_type, and user_id
            
        Returns:
            RemoveDependencyResponse with success status
            
        Raises:
            TodoNotFoundByIdException: If todo doesn't exist
            TodoAccessDeniedException: If user doesn't have access to todo
        """
        pass
    
    @abstractmethod
    def validate_dependency(self, request: ValidateDependencyRequest) -> ValidateDependencyResponse:
        """
        Validate a todo's dependency chain for circular dependencies.
        
        Args:
            request: ValidateDependencyRequest with todo_id and user_id
            
        Returns:
            ValidateDependencyResponse with validation results
        """
        pass
    
    @abstractmethod
    def get_dependency_chain(self, request: GetDependencyChainRequest) -> GetDependencyChainResponse:
        """
        Get the dependency chain for a todo.
        
        Args:
            request: GetDependencyChainRequest with todo_id, user_id, and direction
            
        Returns:
            GetDependencyChainResponse with dependency chain
            
        Raises:
            TodoNotFoundByIdException: If todo doesn't exist
            TodoAccessDeniedException: If user doesn't have access to todo
        """
        pass

