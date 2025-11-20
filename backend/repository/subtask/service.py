# Standard library
import logging

# Third-party
# (none needed)

# Internal - from other modules
# (none needed)

# Internal - from same module
from .models import Subtask
from . import interface

logger = logging.getLogger(__name__)


class SubtaskRepositoryService(interface.AbstractSubtaskRepository):
    """Repository service for subtask data access."""
    
    def create(self, subtask_data: interface.SubtaskCreateRequest) -> interface.SubtaskDTO:
        logger.info(f"Creating subtask with title: {subtask_data.title}", extra={"input": subtask_data.model_dump()})
        
        if not subtask_data.title:
            logger.warning("Failed to create subtask - title is required")
            raise interface.SubtaskTitleRequiredException()
        
        subtask = Subtask()
        subtask.title = subtask_data.title
        subtask.status = subtask_data.status
        subtask.todo_id = subtask_data.todo_id
        subtask.order = subtask_data.order
        subtask.created_at = subtask_data.created_at
        subtask.updated_at = subtask_data.updated_at
        subtask.completed_at = subtask_data.completed_at_timestamp_ms
        
        subtask.save()
        
        result = interface.SubtaskDTO.from_model(subtask)
        logger.info(f"Subtask created successfully: {result.subtask_id}", extra={"output": result.model_dump()})
        return result
    
    def get_by_id(self, subtask_id: int) -> interface.SubtaskDTO | None:
        logger.info(f"Fetching subtask by id: {subtask_id}", extra={"input": {"subtask_id": subtask_id}})
        
        try:
            subtask = Subtask.objects.get(id=subtask_id)
            result = interface.SubtaskDTO.from_model(subtask)
            logger.info(f"Subtask fetched successfully: {subtask_id}", extra={"output": result.model_dump()})
            return result
        except Subtask.DoesNotExist:
            logger.info(f"Subtask not found: {subtask_id}")
            return None
    
    def get_subtasks(self, filters: interface.SubtaskFilter) -> list[interface.SubtaskDTO]:
        logger.info(f"Filtering subtasks", extra={"input": filters.model_dump()})
        
        queryset = Subtask.objects.all()
        
        # Apply basic filters
        if filters.todo_id:
            queryset = queryset.filter(todo_id=filters.todo_id)
        if filters.status:
            queryset = queryset.filter(status=filters.status)
        
        # Apply ordering
        queryset = queryset.order_by(filters.order_by)
        
        # Apply pagination
        if filters.offset is not None and filters.limit is not None:
            queryset = queryset[filters.offset:filters.offset + filters.limit]
        
        results = [interface.SubtaskDTO.from_model(subtask) for subtask in queryset]
        logger.info(f"Found {len(results)} subtasks matching filter", extra={"output": {"count": len(results)}})
        return results
    
    def update(self, subtask_id: int, subtask_data: interface.SubtaskUpdateRequest) -> interface.SubtaskDTO:
        logger.info(f"Updating subtask: {subtask_id}", extra={"input": {"subtask_id": subtask_id}})
        
        try:
            subtask = Subtask.objects.get(id=subtask_id)
        except Subtask.DoesNotExist:
            logger.warning(f"Subtask not found for update: {subtask_id}")
            raise interface.SubtaskNotFoundByIdException(subtask_id)
        
        # Update fields if provided
        if subtask_data.title is not None:
            subtask.title = subtask_data.title
        if subtask_data.status is not None:
            subtask.status = subtask_data.status
            # Set completed_at when status changes to Done
            if subtask_data.status == 'Done' and subtask.completed_at is None:
                if subtask_data.completed_at_timestamp_ms:
                    subtask.completed_at = subtask_data.completed_at_timestamp_ms
            # Clear completed_at when status changes from Done
            elif subtask_data.status != 'Done' and subtask.completed_at is not None:
                subtask.completed_at = None
        if subtask_data.order is not None:
            subtask.order = subtask_data.order
        if subtask_data.completed_at_timestamp_ms is not None:
            subtask.completed_at = subtask_data.completed_at_timestamp_ms
        # Updated timestamp is provided by usecase layer
        if subtask_data.updated_at:
            subtask.updated_at = subtask_data.updated_at
        
        subtask.save()
        
        result = interface.SubtaskDTO.from_model(subtask)
        logger.info(f"Subtask updated successfully: {subtask_id}", extra={"output": result.model_dump()})
        return result
    
    def delete(self, subtask_id: int) -> None:
        logger.info(f"Deleting subtask: {subtask_id}", extra={"input": {"subtask_id": subtask_id}})
        
        try:
            subtask = Subtask.objects.get(id=subtask_id)
            subtask.delete()
            logger.info(f"Subtask deleted successfully: {subtask_id}")
        except Subtask.DoesNotExist:
            logger.warning(f"Subtask not found for deletion: {subtask_id}")
            raise interface.SubtaskNotFoundByIdException(subtask_id)

