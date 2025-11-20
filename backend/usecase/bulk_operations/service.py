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


class BulkOperationsService(interface.AbstractBulkOperationsService):
    """Service for managing bulk operations."""
    
    def __init__(
        self,
        todo_repo: todo_repository_interface.AbstractTodoRepository,
        todo_management_service: todo_management_interface.AbstractTodoManagementService,
        date_time_service: date_utils_interface.AbstractDateTimeService,
    ):
        self.todo_repo = todo_repo
        self.todo_management_service = todo_management_service
        self.date_time_service = date_time_service
    
    def bulk_update(self, request: interface.BulkUpdateRequest) -> interface.BulkUpdateResponse:
        logger.info(f"Bulk updating {len(request.todo_ids)} todos", extra={"input": request.model_dump()})
        
        if not request.todo_ids:
            logger.warning("Bulk update failed - todo_ids list is empty")
            raise interface.EmptyTodoListException()
        
        updated_count = 0
        failed_count = 0
        failed_todo_ids = []
        
        for todo_id in request.todo_ids:
            try:
                # Verify todo exists and user has access
                todo_dto = self.todo_repo.get_by_id(todo_id)
                if not todo_dto:
                    logger.warning(f"Todo not found in bulk update: {todo_id}")
                    failed_count += 1
                    failed_todo_ids.append(todo_id)
                    continue
                
                if todo_dto.user_id != request.user_id:
                    logger.warning(f"Access denied - user {request.user_id} tried to bulk update todo {todo_id}")
                    failed_count += 1
                    failed_todo_ids.append(todo_id)
                    continue
                
                # Update todo
                update_request = todo_management_interface.UpdateTodoRequest(
                    todo_id=todo_id,
                    user_id=request.user_id,
                    status=request.status,
                    priority=request.priority,
                    category=request.category,
                    labels=request.labels,
                    project_id=request.project_id
                )
                
                self.todo_management_service.update_todo(update_request)
                updated_count += 1
                
            except Exception as e:
                logger.exception(f"Error updating todo {todo_id} in bulk update")
                failed_count += 1
                failed_todo_ids.append(todo_id)
        
        success = failed_count == 0
        message = f"Updated {updated_count} todos successfully" if success else f"Updated {updated_count} todos, {failed_count} failed"
        
        response = interface.BulkUpdateResponse(
            updated_count=updated_count,
            failed_count=failed_count,
            failed_todo_ids=failed_todo_ids,
            success=success,
            message=message
        )
        
        logger.info(f"Bulk update completed: {updated_count} updated, {failed_count} failed", 
                   extra={"output": response.model_dump()})
        return response
    
    def bulk_delete(self, request: interface.BulkDeleteRequest) -> interface.BulkDeleteResponse:
        logger.info(f"Bulk deleting {len(request.todo_ids)} todos", extra={"input": request.model_dump()})
        
        if not request.todo_ids:
            logger.warning("Bulk delete failed - todo_ids list is empty")
            raise interface.EmptyTodoListException()
        
        deleted_count = 0
        failed_count = 0
        failed_todo_ids = []
        
        for todo_id in request.todo_ids:
            try:
                # Verify todo exists and user has access
                todo_dto = self.todo_repo.get_by_id(todo_id)
                if not todo_dto:
                    logger.warning(f"Todo not found in bulk delete: {todo_id}")
                    failed_count += 1
                    failed_todo_ids.append(todo_id)
                    continue
                
                if todo_dto.user_id != request.user_id:
                    logger.warning(f"Access denied - user {request.user_id} tried to bulk delete todo {todo_id}")
                    failed_count += 1
                    failed_todo_ids.append(todo_id)
                    continue
                
                # Delete todo
                delete_request = todo_management_interface.DeleteTodoRequest(
                    todo_id=todo_id,
                    user_id=request.user_id
                )
                
                self.todo_management_service.delete_todo(delete_request)
                deleted_count += 1
                
            except Exception as e:
                logger.exception(f"Error deleting todo {todo_id} in bulk delete")
                failed_count += 1
                failed_todo_ids.append(todo_id)
        
        success = failed_count == 0
        message = f"Deleted {deleted_count} todos successfully" if success else f"Deleted {deleted_count} todos, {failed_count} failed"
        
        response = interface.BulkDeleteResponse(
            deleted_count=deleted_count,
            failed_count=failed_count,
            failed_todo_ids=failed_todo_ids,
            success=success,
            message=message
        )
        
        logger.info(f"Bulk delete completed: {deleted_count} deleted, {failed_count} failed", 
                   extra={"output": response.model_dump()})
        return response

