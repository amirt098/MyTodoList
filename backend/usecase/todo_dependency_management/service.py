# Standard library
import logging

# Third-party
# (none needed)

# Internal - from other modules
from repository.todo import interface as todo_repository_interface
from usecase.todo_management import interface as todo_management_interface
from utils.date_utils import interface as date_utils_interface

# Internal - from same module
from . import interface

logger = logging.getLogger(__name__)


def _check_circular_dependency(
    todo_repo: todo_repository_interface.AbstractTodoRepository,
    todo_id: int,
    dependency_todo_id: int,
    visited: set | None = None
) -> bool:
    """
    Check if setting a dependency would create a circular dependency.
    
    Args:
        todo_repo: Todo repository
        todo_id: Source todo ID
        dependency_todo_id: Target todo ID to link
        visited: Set of visited todo IDs (for recursion)
        
    Returns:
        True if circular dependency would be created, False otherwise
    """
    if visited is None:
        visited = set()
    
    # If we've already visited this todo, we have a cycle
    if dependency_todo_id in visited:
        return True
    
    # If trying to link to itself, it's a cycle
    if todo_id == dependency_todo_id:
        return True
    
    visited.add(dependency_todo_id)
    
    # Get the dependency todo
    dep_todo = todo_repo.get_by_id(dependency_todo_id)
    if not dep_todo:
        return False
    
    # Check if dependency_todo has previous_todo_id that leads back to todo_id
    if dep_todo.previous_todo_id:
        if dep_todo.previous_todo_id == todo_id:
            return True
        # Recursively check
        if _check_circular_dependency(todo_repo, todo_id, dep_todo.previous_todo_id, visited):
            return True
    
    # Check if dependency_todo has next_todo_id that leads back to todo_id
    if dep_todo.next_todo_id:
        if dep_todo.next_todo_id == todo_id:
            return True
        # Recursively check
        if _check_circular_dependency(todo_repo, todo_id, dep_todo.next_todo_id, visited):
            return True
    
    return False


class TodoDependencyManagementService(interface.AbstractTodoDependencyManagementService):
    """Service for managing todo dependency operations."""
    
    def __init__(
        self,
        todo_repo: todo_repository_interface.AbstractTodoRepository,
        todo_management_service: todo_management_interface.AbstractTodoManagementService,
        date_time_service: date_utils_interface.AbstractDateTimeService,
    ):
        self.todo_repo = todo_repo
        self.todo_management_service = todo_management_service
        self.date_time_service = date_time_service
    
    def set_dependency(self, request: interface.SetDependencyRequest) -> interface.SetDependencyResponse:
        logger.info(f"Setting dependency: todo_id={request.todo_id}, type={request.dependency_type}, dependency_todo_id={request.dependency_todo_id}", 
                   extra={"input": request.model_dump()})
        
        # Verify both todos exist and user has access
        todo_dto = self.todo_repo.get_by_id(request.todo_id)
        if not todo_dto:
            logger.warning(f"Todo not found: {request.todo_id}")
            raise interface.TodoNotFoundByIdException(request.todo_id)
        
        if todo_dto.user_id != request.user_id:
            logger.warning(f"Access denied - user {request.user_id} tried to set dependency on todo {request.todo_id}")
            raise interface.TodoAccessDeniedException(request.todo_id, request.user_id)
        
        dependency_todo_dto = self.todo_repo.get_by_id(request.dependency_todo_id)
        if not dependency_todo_dto:
            logger.warning(f"Dependency todo not found: {request.dependency_todo_id}")
            raise interface.TodoNotFoundByIdException(request.dependency_todo_id)
        
        if dependency_todo_dto.user_id != request.user_id:
            logger.warning(f"Access denied - user {request.user_id} tried to set dependency on todo {request.dependency_todo_id}")
            raise interface.TodoAccessDeniedException(request.dependency_todo_id, request.user_id)
        
        # Validate dependency type
        if request.dependency_type not in ['previous', 'next']:
            logger.warning(f"Invalid dependency type: {request.dependency_type}")
            raise interface.InvalidDependencyException(f"Invalid dependency type: {request.dependency_type}. Must be 'previous' or 'next'")
        
        # Check for circular dependency
        if _check_circular_dependency(self.todo_repo, request.todo_id, request.dependency_todo_id):
            logger.warning(f"Circular dependency detected: todo_id={request.todo_id}, dependency_todo_id={request.dependency_todo_id}")
            raise interface.CircularDependencyException(request.todo_id, request.dependency_todo_id)
        
        # Update todo with dependency
        if request.dependency_type == 'previous':
            update_request = todo_management_interface.UpdateTodoRequest(
                todo_id=request.todo_id,
                user_id=request.user_id,
                previous_todo_id=request.dependency_todo_id
            )
        else:  # 'next'
            update_request = todo_management_interface.UpdateTodoRequest(
                todo_id=request.todo_id,
                user_id=request.user_id,
                next_todo_id=request.dependency_todo_id
            )
        
        self.todo_management_service.update_todo(update_request)
        
        response = interface.SetDependencyResponse(
            todo_id=request.todo_id,
            dependency_type=request.dependency_type,
            dependency_todo_id=request.dependency_todo_id,
            success=True
        )
        
        logger.info(f"Dependency set successfully: todo_id={request.todo_id}, type={request.dependency_type}", 
                   extra={"output": response.model_dump()})
        return response
    
    def remove_dependency(self, request: interface.RemoveDependencyRequest) -> interface.RemoveDependencyResponse:
        logger.info(f"Removing dependency: todo_id={request.todo_id}, type={request.dependency_type}", 
                   extra={"input": request.model_dump()})
        
        # Verify todo exists and user has access
        todo_dto = self.todo_repo.get_by_id(request.todo_id)
        if not todo_dto:
            logger.warning(f"Todo not found: {request.todo_id}")
            raise interface.TodoNotFoundByIdException(request.todo_id)
        
        if todo_dto.user_id != request.user_id:
            logger.warning(f"Access denied - user {request.user_id} tried to remove dependency from todo {request.todo_id}")
            raise interface.TodoAccessDeniedException(request.todo_id, request.user_id)
        
        # Validate dependency type
        if request.dependency_type not in ['previous', 'next']:
            logger.warning(f"Invalid dependency type: {request.dependency_type}")
            raise interface.InvalidDependencyException(f"Invalid dependency type: {request.dependency_type}. Must be 'previous' or 'next'")
        
        # Remove dependency
        if request.dependency_type == 'previous':
            update_request = todo_management_interface.UpdateTodoRequest(
                todo_id=request.todo_id,
                user_id=request.user_id,
                previous_todo_id=None
            )
        else:  # 'next'
            update_request = todo_management_interface.UpdateTodoRequest(
                todo_id=request.todo_id,
                user_id=request.user_id,
                next_todo_id=None
            )
        
        self.todo_management_service.update_todo(update_request)
        
        response = interface.RemoveDependencyResponse(
            todo_id=request.todo_id,
            dependency_type=request.dependency_type,
            success=True
        )
        
        logger.info(f"Dependency removed successfully: todo_id={request.todo_id}, type={request.dependency_type}", 
                   extra={"output": response.model_dump()})
        return response
    
    def validate_dependency(self, request: interface.ValidateDependencyRequest) -> interface.ValidateDependencyResponse:
        logger.info(f"Validating dependency chain for todo: {request.todo_id}", extra={"input": request.model_dump()})
        
        # Verify todo exists and user has access
        todo_dto = self.todo_repo.get_by_id(request.todo_id)
        if not todo_dto:
            logger.warning(f"Todo not found: {request.todo_id}")
            raise interface.TodoNotFoundByIdException(request.todo_id)
        
        if todo_dto.user_id != request.user_id:
            logger.warning(f"Access denied - user {request.user_id} tried to validate dependency for todo {request.todo_id}")
            raise interface.TodoAccessDeniedException(request.todo_id, request.user_id)
        
        # Check for circular dependency
        has_circular = False
        visited = set()
        current_todo_id = request.todo_id
        
        # Follow previous chain
        while current_todo_id and current_todo_id not in visited:
            visited.add(current_todo_id)
            current_todo = self.todo_repo.get_by_id(current_todo_id)
            if not current_todo:
                break
            if current_todo.previous_todo_id:
                if current_todo.previous_todo_id in visited:
                    has_circular = True
                    break
                current_todo_id = current_todo.previous_todo_id
            else:
                break
        
        # Follow next chain
        visited.clear()
        current_todo_id = request.todo_id
        while current_todo_id and current_todo_id not in visited:
            visited.add(current_todo_id)
            current_todo = self.todo_repo.get_by_id(current_todo_id)
            if not current_todo:
                break
            if current_todo.next_todo_id:
                if current_todo.next_todo_id in visited:
                    has_circular = True
                    break
                current_todo_id = current_todo.next_todo_id
            else:
                break
        
        is_valid = not has_circular
        chain_length = len(visited) if not has_circular else 0
        
        message = "Dependency chain is valid" if is_valid else "Circular dependency detected"
        
        response = interface.ValidateDependencyResponse(
            todo_id=request.todo_id,
            is_valid=is_valid,
            has_circular_dependency=has_circular,
            chain_length=chain_length,
            message=message
        )
        
        logger.info(f"Dependency validation completed: is_valid={is_valid}, has_circular={has_circular}", 
                   extra={"output": response.model_dump()})
        return response
    
    def get_dependency_chain(self, request: interface.GetDependencyChainRequest) -> interface.GetDependencyChainResponse:
        logger.info(f"Getting dependency chain for todo: {request.todo_id}, direction={request.direction}", 
                   extra={"input": request.model_dump()})
        
        # Verify todo exists and user has access
        todo_dto = self.todo_repo.get_by_id(request.todo_id)
        if not todo_dto:
            logger.warning(f"Todo not found: {request.todo_id}")
            raise interface.TodoNotFoundByIdException(request.todo_id)
        
        if todo_dto.user_id != request.user_id:
            logger.warning(f"Access denied - user {request.user_id} tried to get dependency chain for todo {request.todo_id}")
            raise interface.TodoAccessDeniedException(request.todo_id, request.user_id)
        
        chain = []
        visited = set()
        
        # Add current todo
        chain.append(interface.DependencyNode(
            todo_id=todo_dto.todo_id,
            title=todo_dto.title,
            status=todo_dto.status,
            previous_todo_id=todo_dto.previous_todo_id,
            next_todo_id=todo_dto.next_todo_id
        ))
        visited.add(todo_dto.todo_id)
        
        # Follow previous chain if requested
        if request.direction in ['previous', 'both']:
            current_todo_id = todo_dto.previous_todo_id
            while current_todo_id and current_todo_id not in visited:
                visited.add(current_todo_id)
                current_todo = self.todo_repo.get_by_id(current_todo_id)
                if not current_todo:
                    break
                chain.insert(0, interface.DependencyNode(
                    todo_id=current_todo.todo_id,
                    title=current_todo.title,
                    status=current_todo.status,
                    previous_todo_id=current_todo.previous_todo_id,
                    next_todo_id=current_todo.next_todo_id
                ))
                current_todo_id = current_todo.previous_todo_id
        
        # Follow next chain if requested
        if request.direction in ['next', 'both']:
            current_todo_id = todo_dto.next_todo_id
            while current_todo_id and current_todo_id not in visited:
                visited.add(current_todo_id)
                current_todo = self.todo_repo.get_by_id(current_todo_id)
                if not current_todo:
                    break
                chain.append(interface.DependencyNode(
                    todo_id=current_todo.todo_id,
                    title=current_todo.title,
                    status=current_todo.status,
                    previous_todo_id=current_todo.previous_todo_id,
                    next_todo_id=current_todo.next_todo_id
                ))
                current_todo_id = current_todo.next_todo_id
        
        response = interface.GetDependencyChainResponse(
            todo_id=request.todo_id,
            chain=chain,
            total_todos=len(chain)
        )
        
        logger.info(f"Dependency chain retrieved: {len(chain)} todos", extra={"output": {"count": len(chain)}})
        return response

