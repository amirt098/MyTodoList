# Standard library
import logging

# Third-party
# (none needed)

# Internal - from other modules
from repository.todo import interface as todo_repository_interface
from repository.subtask import interface as subtask_repository_interface
from utils.date_utils import interface as date_utils_interface

# Internal - from same module
from . import interface

logger = logging.getLogger(__name__)


def _calculate_progress_from_subtasks(
    subtask_repo: subtask_repository_interface.AbstractSubtaskRepository,
    todo_id: int
) -> float:
    """Calculate progress percentage based on completed subtasks."""
    subtask_filter = subtask_repository_interface.SubtaskFilter(todo_id=todo_id)
    subtasks = subtask_repo.get_subtasks(subtask_filter)
    
    if not subtasks:
        return 0.0
    
    completed_count = sum(1 for subtask in subtasks if subtask.status == 'Done')
    total_count = len(subtasks)
    
    if total_count == 0:
        return 0.0
    
    return round((completed_count / total_count) * 100, 2)


def _repo_dto_to_usecase_dto(
    repo_dto: todo_repository_interface.TodoDTO,
    subtask_repo: subtask_repository_interface.AbstractSubtaskRepository | None = None
) -> interface.TodoDTO:
    """Simple converter: Repository TodoDTO to UseCase TodoDTO with progress calculation."""
    progress = 0.0
    if subtask_repo:
        progress = _calculate_progress_from_subtasks(subtask_repo, repo_dto.todo_id)
    
    return interface.TodoDTO(
        todo_id=repo_dto.todo_id,
        title=repo_dto.title,
        description=repo_dto.description,
        deadline_timestamp_ms=repo_dto.deadline_timestamp_ms,
        priority=repo_dto.priority,
        status=repo_dto.status,
        category=repo_dto.category,
        labels=repo_dto.labels,
        user_id=repo_dto.user_id,
        project_id=repo_dto.project_id,
        previous_todo_id=repo_dto.previous_todo_id,
        next_todo_id=repo_dto.next_todo_id,
        order=repo_dto.order,
        created_at=repo_dto.created_at,
        updated_at=repo_dto.updated_at,
        completed_at_timestamp_ms=repo_dto.completed_at_timestamp_ms,
        auto_repeat=repo_dto.auto_repeat,
        progress=progress
    )


class TodoManagementService(interface.AbstractTodoManagementService):
    """Service for managing todo operations."""
    
    def __init__(
        self,
        todo_repo: todo_repository_interface.AbstractTodoRepository,
        date_time_service: date_utils_interface.AbstractDateTimeService,
        subtask_repo: subtask_repository_interface.AbstractSubtaskRepository | None = None,
    ):
        self.todo_repo = todo_repo
        self.subtask_repo = subtask_repo
        self.date_time_service = date_time_service
    
    def create_todo(self, request: interface.CreateTodoRequest) -> interface.CreateTodoResponse:
        logger.info(f"Creating todo with title: {request.title}", extra={"input": request.model_dump()})
        
        if not request.title:
            logger.warning("Todo creation failed - title is required")
            raise interface.TodoTitleRequiredException()
        
        # Calculate timestamps in usecase layer
        now_dto = self.date_time_service.now()
        
        # Create TodoCreateRequest with timestamps
        todo_create_request = todo_repository_interface.TodoCreateRequest(
            title=request.title,
            description=request.description,
            deadline_timestamp_ms=request.deadline_timestamp_ms,
            priority=request.priority,
            status=request.status,
            category=request.category,
            labels=request.labels,
            user_id=request.user_id,
            project_id=request.project_id,
            previous_todo_id=request.previous_todo_id,
            next_todo_id=request.next_todo_id,
            order=request.order,
            created_at=now_dto.timestamp_ms,
            updated_at=now_dto.timestamp_ms,
            completed_at_timestamp_ms=None,
            auto_repeat=request.auto_repeat
        )
        
        todo_dto = self.todo_repo.create(todo_create_request)
        
        response = interface.CreateTodoResponse(
            todo_id=todo_dto.todo_id,
            title=todo_dto.title,
            status=todo_dto.status,
            user_id=todo_dto.user_id,
            created_at=todo_dto.created_at
        )
        
        logger.info(f"Todo created successfully: {response.todo_id}", extra={"output": response.model_dump()})
        return response
    
    def get_todo_by_id(self, request: interface.GetTodoRequest) -> interface.TodoDTO:
        logger.info(f"Fetching todo by id: {request.todo_id}", extra={"input": request.model_dump()})
        
        # Get todo
        todo_dto = self.todo_repo.get_by_id(request.todo_id)
        if not todo_dto:
            logger.warning(f"Todo not found: {request.todo_id}")
            raise interface.TodoNotFoundByIdException(request.todo_id)
        
        # Verify access
        if todo_dto.user_id != request.user_id:
            logger.warning(f"Access denied - user {request.user_id} tried to access todo {request.todo_id}")
            raise interface.TodoAccessDeniedException(request.todo_id, request.user_id)
        
        response = _repo_dto_to_usecase_dto(todo_dto, self.subtask_repo)
        
        logger.info(f"Todo fetched successfully: {request.todo_id}", extra={"output": response.model_dump()})
        return response
    
    def get_todos(self, request: interface.TodoFilter) -> interface.TodoListResponse:
        logger.info(f"Fetching todos for user: {request.user_id}", extra={"input": request.model_dump()})
        
        # Convert to repository filter
        todo_filter = todo_repository_interface.TodoFilter(
            user_id=request.user_id,
            project_id=request.project_id,
            status=request.status,
            priority=request.priority,
            category=request.category,
            label=request.label,
            deadline_after__gte=request.deadline_after__gte,
            deadline_after__lte=request.deadline_after__lte,
            deadline_before__gte=request.deadline_before__gte,
            deadline_before__lte=request.deadline_before__lte,
            created_after__gte=request.created_after__gte,
            created_after__lte=request.created_after__lte,
            created_before__gte=request.created_before__gte,
            created_before__lte=request.created_before__lte,
            search=request.search,
            order_by=request.order_by,
            limit=request.limit,
            offset=request.offset
        )
        
        todo_dtos = self.todo_repo.get_todos(todo_filter)
        
        # Convert to usecase DTOs with progress calculation
        todos = [_repo_dto_to_usecase_dto(dto, self.subtask_repo) for dto in todo_dtos]
        
        response = interface.TodoListResponse(
            todos=todos,
            total=len(todos)
        )
        
        logger.info(f"Found {len(todos)} todos for user: {request.user_id}", extra={"output": {"count": len(todos)}})
        return response
    
    def get_all_my_todos(self, request: interface.GetAllMyTodosRequest) -> interface.TodoListResponse:
        logger.info(f"Getting all todos for user: {request.user_id} (unified view)", extra={"input": request.model_dump()})
        
        # Convert to TodoFilter (project_id=None means all todos)
        todo_filter = todo_repository_interface.TodoFilter(
            user_id=request.user_id,
            project_id=None,  # None = all todos (personal + projects)
            status=request.status,
            priority=request.priority,
            category=request.category,
            label=request.label,
            deadline_after__gte=request.deadline_after__gte,
            deadline_after__lte=request.deadline_after__lte,
            search=request.search,
            order_by=request.order_by,
            limit=request.limit,
            offset=request.offset
        )
        
        # Use existing get_todos method
        return self.get_todos(todo_filter)
    
    def update_todo(self, request: interface.UpdateTodoRequest) -> interface.UpdateTodoResponse:
        logger.info(f"Updating todo: {request.todo_id}", extra={"input": request.model_dump()})
        
        # Verify todo exists and user has access
        existing_todo_dto = self.todo_repo.get_by_id(request.todo_id)
        if not existing_todo_dto:
            logger.warning(f"Todo update failed - todo not found: {request.todo_id}")
            raise interface.TodoNotFoundByIdException(request.todo_id)
        
        existing_todo = _repo_dto_to_usecase_dto(existing_todo_dto, self.subtask_repo)
        
        if existing_todo.user_id != request.user_id:
            logger.warning(f"Access denied - user {request.user_id} tried to update todo {request.todo_id}")
            raise interface.TodoAccessDeniedException(request.todo_id, request.user_id)
        
        # Calculate updated timestamp in usecase layer
        now_dto = self.date_time_service.now()
        
        # Create TodoUpdateRequest with only provided fields
        todo_update_request = todo_repository_interface.TodoUpdateRequest(
            title=request.title,
            description=request.description,
            deadline_timestamp_ms=request.deadline_timestamp_ms,
            priority=request.priority,
            status=request.status,
            category=request.category,
            labels=request.labels,
            project_id=request.project_id,
            previous_todo_id=request.previous_todo_id,
            next_todo_id=request.next_todo_id,
            order=request.order,
            created_at=None,  # Not updating
            updated_at=now_dto.timestamp_ms,
            completed_at_timestamp_ms=request.completed_at_timestamp_ms,
            auto_repeat=request.auto_repeat
        )
        
        updated_todo_dto = self.todo_repo.update(request.todo_id, todo_update_request)
        
        response = interface.UpdateTodoResponse(
            todo_id=updated_todo_dto.todo_id,
            title=updated_todo_dto.title,
            description=updated_todo_dto.description,
            deadline_timestamp_ms=updated_todo_dto.deadline_timestamp_ms,
            priority=updated_todo_dto.priority,
            status=updated_todo_dto.status,
            category=updated_todo_dto.category,
            labels=updated_todo_dto.labels,
            user_id=updated_todo_dto.user_id,
            project_id=updated_todo_dto.project_id,
            updated_at=updated_todo_dto.updated_at
        )
        
        logger.info(f"Todo updated successfully: {request.todo_id}", extra={"output": response.model_dump()})
        return response
    
    def delete_todo(self, request: interface.DeleteTodoRequest) -> interface.DeleteTodoResponse:
        logger.info(f"Deleting todo: {request.todo_id}", extra={"input": request.model_dump()})
        
        # Verify todo exists and user has access
        existing_todo_dto = self.todo_repo.get_by_id(request.todo_id)
        if not existing_todo_dto:
            logger.warning(f"Todo deletion failed - todo not found: {request.todo_id}")
            raise interface.TodoNotFoundByIdException(request.todo_id)
        
        if existing_todo_dto.user_id != request.user_id:
            logger.warning(f"Access denied - user {request.user_id} tried to delete todo {request.todo_id}")
            raise interface.TodoAccessDeniedException(request.todo_id, request.user_id)
        
        # Delete todo
        self.todo_repo.delete(request.todo_id)
        
        response = interface.DeleteTodoResponse(
            success=True,
            message=f"Todo {request.todo_id} deleted successfully"
        )
        
        logger.info(f"Todo deleted successfully: {request.todo_id}", extra={"output": response.model_dump()})
        return response
