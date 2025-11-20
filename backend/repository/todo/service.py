# Standard library
import logging

# Third-party
# (none needed)

# Internal - from other modules
# (none needed)

# Internal - from same module
from .models import Todo
from . import interface

logger = logging.getLogger(__name__)


class TodoRepositoryService(interface.AbstractTodoRepository):
    """Repository service for todo data access."""
    
    def create(self, todo_data: interface.TodoCreateRequest) -> interface.TodoDTO:
        logger.info(f"Creating todo with title: {todo_data.title}", extra={"input": todo_data.model_dump()})
        
        if not todo_data.title:
            logger.warning("Failed to create todo - title is required")
            raise interface.TodoTitleRequiredException()
        
        todo = Todo()
        todo.title = todo_data.title
        todo.description = todo_data.description or ""
        todo.deadline = todo_data.deadline_timestamp_ms
        todo.priority = todo_data.priority
        todo.status = todo_data.status
        todo.category = todo_data.category or ""
        todo.labels = todo_data.labels or []
        todo.user_id = todo_data.user_id
        todo.project_id = todo_data.project_id
        todo.previous_todo_id = todo_data.previous_todo_id
        todo.next_todo_id = todo_data.next_todo_id
        todo.order = todo_data.order
        todo.auto_repeat = todo_data.auto_repeat
        todo.created_at = todo_data.created_at
        todo.updated_at = todo_data.updated_at
        todo.completed_at = todo_data.completed_at_timestamp_ms
        
        todo.save()
        
        result = interface.TodoDTO.from_model(todo)
        logger.info(f"Todo created successfully: {result.todo_id}", extra={"output": result.model_dump()})
        return result
    
    def get_by_id(self, todo_id: int) -> interface.TodoDTO | None:
        logger.info(f"Fetching todo by id: {todo_id}", extra={"input": {"todo_id": todo_id}})
        
        try:
            todo = Todo.objects.get(id=todo_id)
            result = interface.TodoDTO.from_model(todo)
            logger.info(f"Todo fetched successfully: {todo_id}", extra={"output": result.model_dump()})
            return result
        except Todo.DoesNotExist:
            logger.info(f"Todo not found: {todo_id}")
            return None
    
    def get_todos(self, filters: interface.TodoFilter) -> list[interface.TodoDTO]:
        logger.info(f"Filtering todos", extra={"input": filters.model_dump()})
        
        queryset = Todo.objects.all()
        
        # Apply basic filters
        if filters.user_id:
            queryset = queryset.filter(user_id=filters.user_id)
        if filters.project_id is not None:
            queryset = queryset.filter(project_id=filters.project_id)
        if filters.status:
            queryset = queryset.filter(status=filters.status)
        if filters.priority:
            queryset = queryset.filter(priority=filters.priority)
        if filters.category:
            queryset = queryset.filter(category__icontains=filters.category)
        if filters.label:
            queryset = queryset.filter(labels__contains=[filters.label])
        
        # Apply timestamp filters (direct integer comparison)
        if filters.deadline_after__gte:
            queryset = queryset.filter(deadline__gte=filters.deadline_after__gte)
        if filters.deadline_after__lte:
            queryset = queryset.filter(deadline__lte=filters.deadline_after__lte)
        if filters.deadline_before__gte:
            queryset = queryset.filter(deadline__gte=filters.deadline_before__gte)
        if filters.deadline_before__lte:
            queryset = queryset.filter(deadline__lte=filters.deadline_before__lte)
        if filters.created_after__gte:
            queryset = queryset.filter(created_at__gte=filters.created_after__gte)
        if filters.created_after__lte:
            queryset = queryset.filter(created_at__lte=filters.created_after__lte)
        if filters.created_before__gte:
            queryset = queryset.filter(created_at__gte=filters.created_before__gte)
        if filters.created_before__lte:
            queryset = queryset.filter(created_at__lte=filters.created_before__lte)
        
        if filters.search:
            from django.db.models import Q
            queryset = queryset.filter(
                Q(title__icontains=filters.search) |
                Q(description__icontains=filters.search)
            )
        
        # Apply ordering
        queryset = queryset.order_by(filters.order_by)
        
        # Apply pagination
        if filters.offset is not None and filters.limit is not None:
            queryset = queryset[filters.offset:filters.offset + filters.limit]
        
        results = [interface.TodoDTO.from_model(todo) for todo in queryset]
        logger.info(f"Found {len(results)} todos matching filter", extra={"output": {"count": len(results)}})
        return results
    
    def update(self, todo_id: int, todo_data: interface.TodoUpdateRequest) -> interface.TodoDTO:
        logger.info(f"Updating todo: {todo_id}", extra={"input": {"todo_id": todo_id}})
        
        try:
            todo = Todo.objects.get(id=todo_id)
        except Todo.DoesNotExist:
            logger.warning(f"Todo not found for update: {todo_id}")
            raise interface.TodoNotFoundByIdException(todo_id)
        
        # Update fields if provided
        if todo_data.title is not None:
            todo.title = todo_data.title
        if todo_data.description is not None:
            todo.description = todo_data.description
        if todo_data.deadline_timestamp_ms is not None:
            todo.deadline = todo_data.deadline_timestamp_ms
        if todo_data.priority is not None:
            todo.priority = todo_data.priority
        if todo_data.status is not None:
            todo.status = todo_data.status
        if todo_data.category is not None:
            todo.category = todo_data.category
        if todo_data.labels is not None:
            todo.labels = todo_data.labels
        if todo_data.project_id is not None:
            todo.project_id = todo_data.project_id
        if todo_data.previous_todo_id is not None:
            todo.previous_todo_id = todo_data.previous_todo_id
        if todo_data.next_todo_id is not None:
            todo.next_todo_id = todo_data.next_todo_id
        if todo_data.order is not None:
            todo.order = todo_data.order
        if todo_data.auto_repeat is not None:
            todo.auto_repeat = todo_data.auto_repeat
        # Updated timestamp is provided by usecase layer
        if todo_data.updated_at:
            todo.updated_at = todo_data.updated_at
        if todo_data.completed_at_timestamp_ms is not None:
            todo.completed_at = todo_data.completed_at_timestamp_ms
        
        todo.save()
        
        result = interface.TodoDTO.from_model(todo)
        logger.info(f"Todo updated successfully: {todo_id}", extra={"output": result.model_dump()})
        return result
    
    def delete(self, todo_id: int) -> None:
        logger.info(f"Deleting todo: {todo_id}", extra={"input": {"todo_id": todo_id}})
        
        try:
            todo = Todo.objects.get(id=todo_id)
            todo.delete()
            logger.info(f"Todo deleted successfully: {todo_id}")
        except Todo.DoesNotExist:
            logger.warning(f"Todo not found for deletion: {todo_id}")
            raise interface.TodoNotFoundByIdException(todo_id)
