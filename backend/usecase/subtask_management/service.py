# Standard library
import logging

# Third-party
# (none needed)

# Internal - from other modules
from repository.subtask import interface as subtask_repository_interface
from repository.todo import interface as todo_repository_interface
from utils.date_utils import interface as date_utils_interface

# Internal - from same module
from . import interface

logger = logging.getLogger(__name__)


def _repo_dto_to_usecase_dto(repo_dto: subtask_repository_interface.SubtaskDTO) -> interface.SubtaskDTO:
    """Simple converter: Repository SubtaskDTO to UseCase SubtaskDTO."""
    return interface.SubtaskDTO(
        subtask_id=repo_dto.subtask_id,
        title=repo_dto.title,
        status=repo_dto.status,
        todo_id=repo_dto.todo_id,
        order=repo_dto.order,
        created_at=repo_dto.created_at,
        updated_at=repo_dto.updated_at,
        completed_at_timestamp_ms=repo_dto.completed_at_timestamp_ms
    )


def _calculate_progress(subtasks: list[subtask_repository_interface.SubtaskDTO]) -> float:
    """Calculate progress percentage based on completed subtasks."""
    if not subtasks:
        return 0.0
    
    completed_count = sum(1 for subtask in subtasks if subtask.status == 'Done')
    total_count = len(subtasks)
    
    if total_count == 0:
        return 0.0
    
    return round((completed_count / total_count) * 100, 2)


class SubtaskManagementService(interface.AbstractSubtaskManagementService):
    """Service for managing subtask operations."""
    
    def __init__(
        self,
        subtask_repo: subtask_repository_interface.AbstractSubtaskRepository,
        todo_repo: todo_repository_interface.AbstractTodoRepository,
        date_time_service: date_utils_interface.AbstractDateTimeService,
    ):
        self.subtask_repo = subtask_repo
        self.todo_repo = todo_repo
        self.date_time_service = date_time_service
    
    def add_subtask(self, request: interface.AddSubtaskRequest) -> interface.AddSubtaskResponse:
        logger.info(f"Adding subtask to todo: {request.todo_id}", extra={"input": request.model_dump()})
        
        if not request.title:
            logger.warning("Subtask creation failed - title is required")
            raise interface.SubtaskTitleRequiredException()
        
        # Verify todo exists and user has access
        todo_dto = self.todo_repo.get_by_id(request.todo_id)
        if not todo_dto:
            logger.warning(f"Todo not found: {request.todo_id}")
            raise interface.TodoNotFoundByIdException(request.todo_id)
        
        if todo_dto.user_id != request.user_id:
            logger.warning(f"Access denied - user {request.user_id} tried to add subtask to todo {request.todo_id}")
            raise interface.TodoAccessDeniedException(request.todo_id, request.user_id)
        
        # Calculate timestamps
        now_dto = self.date_time_service.now()
        
        # Determine order if not provided
        order = request.order
        if order is None:
            # Get max order for this todo
            subtask_filter = subtask_repository_interface.SubtaskFilter(
                todo_id=request.todo_id
            )
            existing_subtasks = self.subtask_repo.get_subtasks(subtask_filter)
            if existing_subtasks:
                max_order = max(st.order for st in existing_subtasks)
                order = max_order + 1
            else:
                order = 0
        
        # Create subtask
        subtask_create_request = subtask_repository_interface.SubtaskCreateRequest(
            title=request.title,
            status='ToDo',
            todo_id=request.todo_id,
            order=order,
            created_at=now_dto.timestamp_ms,
            updated_at=now_dto.timestamp_ms,
            completed_at_timestamp_ms=None
        )
        
        subtask_dto = self.subtask_repo.create(subtask_create_request)
        
        response = interface.AddSubtaskResponse(
            subtask_id=subtask_dto.subtask_id,
            title=subtask_dto.title,
            status=subtask_dto.status,
            todo_id=subtask_dto.todo_id,
            order=subtask_dto.order,
            created_at=subtask_dto.created_at
        )
        
        logger.info(f"Subtask added successfully: {response.subtask_id}", extra={"output": response.model_dump()})
        return response
    
    def update_subtask(self, request: interface.UpdateSubtaskRequest) -> interface.UpdateSubtaskResponse:
        logger.info(f"Updating subtask: {request.subtask_id}", extra={"input": request.model_dump()})
        
        # Verify subtask exists
        subtask_dto = self.subtask_repo.get_by_id(request.subtask_id)
        if not subtask_dto:
            logger.warning(f"Subtask not found: {request.subtask_id}")
            raise interface.SubtaskNotFoundByIdException(request.subtask_id)
        
        # Verify todo exists and user has access
        todo_dto = self.todo_repo.get_by_id(request.todo_id)
        if not todo_dto:
            logger.warning(f"Todo not found: {request.todo_id}")
            raise interface.TodoNotFoundByIdException(request.todo_id)
        
        if todo_dto.user_id != request.user_id:
            logger.warning(f"Access denied - user {request.user_id} tried to update subtask in todo {request.todo_id}")
            raise interface.TodoAccessDeniedException(request.todo_id, request.user_id)
        
        # Verify subtask belongs to todo
        if subtask_dto.todo_id != request.todo_id:
            logger.warning(f"Subtask {request.subtask_id} does not belong to todo {request.todo_id}")
            raise interface.SubtaskManagementBadRequestException(
                f"Subtask {request.subtask_id} does not belong to todo {request.todo_id}"
            )
        
        # Calculate timestamps
        now_dto = self.date_time_service.now()
        
        # Determine completed_at if status is changing to Done
        completed_at = None
        if request.status == 'Done' and subtask_dto.status != 'Done':
            completed_at = now_dto.timestamp_ms
        elif request.status and request.status != 'Done' and subtask_dto.status == 'Done':
            completed_at = None
        elif subtask_dto.status == 'Done' and not request.status:
            completed_at = subtask_dto.completed_at_timestamp_ms
        
        # Update subtask
        subtask_update_request = subtask_repository_interface.SubtaskUpdateRequest(
            title=request.title,
            status=request.status,
            order=request.order,
            updated_at=now_dto.timestamp_ms,
            completed_at_timestamp_ms=completed_at
        )
        
        updated_subtask_dto = self.subtask_repo.update(request.subtask_id, subtask_update_request)
        
        response = interface.UpdateSubtaskResponse(
            subtask_id=updated_subtask_dto.subtask_id,
            title=updated_subtask_dto.title,
            status=updated_subtask_dto.status,
            todo_id=updated_subtask_dto.todo_id,
            order=updated_subtask_dto.order,
            updated_at=updated_subtask_dto.updated_at
        )
        
        logger.info(f"Subtask updated successfully: {request.subtask_id}", extra={"output": response.model_dump()})
        return response
    
    def delete_subtask(self, request: interface.DeleteSubtaskRequest) -> interface.DeleteSubtaskResponse:
        logger.info(f"Deleting subtask: {request.subtask_id}", extra={"input": request.model_dump()})
        
        # Verify subtask exists
        subtask_dto = self.subtask_repo.get_by_id(request.subtask_id)
        if not subtask_dto:
            logger.warning(f"Subtask not found: {request.subtask_id}")
            raise interface.SubtaskNotFoundByIdException(request.subtask_id)
        
        # Verify todo exists and user has access
        todo_dto = self.todo_repo.get_by_id(request.todo_id)
        if not todo_dto:
            logger.warning(f"Todo not found: {request.todo_id}")
            raise interface.TodoNotFoundByIdException(request.todo_id)
        
        if todo_dto.user_id != request.user_id:
            logger.warning(f"Access denied - user {request.user_id} tried to delete subtask from todo {request.todo_id}")
            raise interface.TodoAccessDeniedException(request.todo_id, request.user_id)
        
        # Verify subtask belongs to todo
        if subtask_dto.todo_id != request.todo_id:
            logger.warning(f"Subtask {request.subtask_id} does not belong to todo {request.todo_id}")
            raise interface.SubtaskManagementBadRequestException(
                f"Subtask {request.subtask_id} does not belong to todo {request.todo_id}"
            )
        
        # Delete subtask
        self.subtask_repo.delete(request.subtask_id)
        
        response = interface.DeleteSubtaskResponse(
            success=True,
            message=f"Subtask {request.subtask_id} deleted successfully"
        )
        
        logger.info(f"Subtask deleted successfully: {request.subtask_id}", extra={"output": response.model_dump()})
        return response
    
    def mark_subtask_done(self, request: interface.MarkSubtaskDoneRequest) -> interface.MarkSubtaskDoneResponse:
        logger.info(f"Marking subtask {request.subtask_id} as {'done' if request.done else 'undone'}", 
                   extra={"input": request.model_dump()})
        
        # Verify subtask exists
        subtask_dto = self.subtask_repo.get_by_id(request.subtask_id)
        if not subtask_dto:
            logger.warning(f"Subtask not found: {request.subtask_id}")
            raise interface.SubtaskNotFoundByIdException(request.subtask_id)
        
        # Verify todo exists and user has access
        todo_dto = self.todo_repo.get_by_id(request.todo_id)
        if not todo_dto:
            logger.warning(f"Todo not found: {request.todo_id}")
            raise interface.TodoNotFoundByIdException(request.todo_id)
        
        if todo_dto.user_id != request.user_id:
            logger.warning(f"Access denied - user {request.user_id} tried to mark subtask in todo {request.todo_id}")
            raise interface.TodoAccessDeniedException(request.todo_id, request.user_id)
        
        # Verify subtask belongs to todo
        if subtask_dto.todo_id != request.todo_id:
            logger.warning(f"Subtask {request.subtask_id} does not belong to todo {request.todo_id}")
            raise interface.SubtaskManagementBadRequestException(
                f"Subtask {request.subtask_id} does not belong to todo {request.todo_id}"
            )
        
        # Calculate timestamps
        now_dto = self.date_time_service.now()
        
        # Update status
        new_status = 'Done' if request.done else 'ToDo'
        completed_at = now_dto.timestamp_ms if request.done else None
        
        subtask_update_request = subtask_repository_interface.SubtaskUpdateRequest(
            status=new_status,
            updated_at=now_dto.timestamp_ms,
            completed_at_timestamp_ms=completed_at
        )
        
        updated_subtask_dto = self.subtask_repo.update(request.subtask_id, subtask_update_request)
        
        response = interface.MarkSubtaskDoneResponse(
            subtask_id=updated_subtask_dto.subtask_id,
            status=updated_subtask_dto.status,
            completed_at_timestamp_ms=updated_subtask_dto.completed_at_timestamp_ms
        )
        
        logger.info(f"Subtask marked as {new_status} successfully: {request.subtask_id}", 
                   extra={"output": response.model_dump()})
        return response
    
    def get_subtasks(self, request: interface.GetSubtasksRequest) -> interface.GetSubtasksResponse:
        logger.info(f"Getting subtasks for todo: {request.todo_id}", extra={"input": request.model_dump()})
        
        # Verify todo exists and user has access
        todo_dto = self.todo_repo.get_by_id(request.todo_id)
        if not todo_dto:
            logger.warning(f"Todo not found: {request.todo_id}")
            raise interface.TodoNotFoundByIdException(request.todo_id)
        
        if todo_dto.user_id != request.user_id:
            logger.warning(f"Access denied - user {request.user_id} tried to get subtasks for todo {request.todo_id}")
            raise interface.TodoAccessDeniedException(request.todo_id, request.user_id)
        
        # Get subtasks
        subtask_filter = subtask_repository_interface.SubtaskFilter(
            todo_id=request.todo_id,
            status=request.status,
            order_by='order'
        )
        subtask_dtos = self.subtask_repo.get_subtasks(subtask_filter)
        
        # Calculate progress
        progress = _calculate_progress(subtask_dtos)
        
        # Convert to usecase DTOs
        subtasks = [_repo_dto_to_usecase_dto(dto) for dto in subtask_dtos]
        
        response = interface.GetSubtasksResponse(
            subtasks=subtasks,
            total=len(subtasks),
            progress=progress
        )
        
        logger.info(f"Found {len(subtasks)} subtasks for todo {request.todo_id}, progress: {progress}%", 
                   extra={"output": {"count": len(subtasks), "progress": progress}})
        return response

