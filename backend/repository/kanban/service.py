# Standard library
import logging

# Third-party
# (none needed)

# Internal - from other modules
# (none needed)

# Internal - from same module
from .models import KanbanColumn
from . import interface

logger = logging.getLogger(__name__)


class KanbanRepositoryService(interface.AbstractKanbanRepository):
    """Repository service for kanban data access."""
    
    def create_column(self, column_data: interface.KanbanColumnCreateRequest) -> interface.KanbanColumnDTO:
        logger.info(f"Creating kanban column with name: {column_data.name}", extra={"input": column_data.model_dump()})
        
        if not column_data.name:
            logger.warning("Failed to create kanban column - name is required")
            raise interface.KanbanColumnNameRequiredException()
        
        column = KanbanColumn()
        column.name = column_data.name
        column.status_value = column_data.status_value or ""
        column.color = column_data.color or "#6B7280"
        column.project_id = column_data.project_id
        column.user_id = column_data.user_id
        column.order = column_data.order
        column.is_default = column_data.is_default
        column.is_active = column_data.is_active
        column.created_at = column_data.created_at
        column.updated_at = column_data.updated_at
        
        column.save()
        
        result = interface.KanbanColumnDTO.from_model(column)
        logger.info(f"Kanban column created successfully: {result.column_id}", extra={"output": result.model_dump()})
        return result
    
    def get_column_by_id(self, column_id: int) -> interface.KanbanColumnDTO | None:
        logger.info(f"Fetching kanban column by id: {column_id}", extra={"input": {"column_id": column_id}})
        
        try:
            column = KanbanColumn.objects.get(id=column_id)
            result = interface.KanbanColumnDTO.from_model(column)
            logger.info(f"Kanban column fetched successfully: {column_id}", extra={"output": result.model_dump()})
            return result
        except KanbanColumn.DoesNotExist:
            logger.info(f"Kanban column not found: {column_id}")
            return None
    
    def get_columns(self, filters: interface.KanbanColumnFilter) -> list[interface.KanbanColumnDTO]:
        logger.info(f"Filtering kanban columns", extra={"input": filters.model_dump()})
        
        queryset = KanbanColumn.objects.all()
        
        # Apply basic filters
        if filters.project_id is not None:
            queryset = queryset.filter(project_id=filters.project_id)
        if filters.user_id is not None:
            queryset = queryset.filter(user_id=filters.user_id)
        if filters.is_default is not None:
            queryset = queryset.filter(is_default=filters.is_default)
        if filters.is_active is not None:
            queryset = queryset.filter(is_active=filters.is_active)
        
        # Apply ordering
        queryset = queryset.order_by(filters.order_by)
        
        # Apply pagination
        if filters.offset is not None and filters.limit is not None:
            queryset = queryset[filters.offset:filters.offset + filters.limit]
        
        results = [interface.KanbanColumnDTO.from_model(column) for column in queryset]
        logger.info(f"Found {len(results)} kanban columns matching filter", extra={"output": {"count": len(results)}})
        return results
    
    def update_column(self, column_id: int, column_data: interface.KanbanColumnUpdateRequest) -> interface.KanbanColumnDTO:
        logger.info(f"Updating kanban column: {column_id}", extra={"input": {"column_id": column_id}})
        
        try:
            column = KanbanColumn.objects.get(id=column_id)
        except KanbanColumn.DoesNotExist:
            logger.warning(f"Kanban column not found for update: {column_id}")
            raise interface.KanbanColumnNotFoundByIdException(column_id)
        
        # Update fields if provided
        if column_data.name is not None:
            column.name = column_data.name
        if column_data.status_value is not None:
            column.status_value = column_data.status_value
        if column_data.color is not None:
            column.color = column_data.color
        if column_data.order is not None:
            column.order = column_data.order
        if column_data.is_active is not None:
            column.is_active = column_data.is_active
        # Updated timestamp is provided by usecase layer
        if column_data.updated_at:
            column.updated_at = column_data.updated_at
        
        column.save()
        
        result = interface.KanbanColumnDTO.from_model(column)
        logger.info(f"Kanban column updated successfully: {column_id}", extra={"output": result.model_dump()})
        return result
    
    def delete_column(self, column_id: int) -> None:
        logger.info(f"Deleting kanban column: {column_id}", extra={"input": {"column_id": column_id}})
        
        try:
            column = KanbanColumn.objects.get(id=column_id)
            column.delete()
            logger.info(f"Kanban column deleted successfully: {column_id}")
        except KanbanColumn.DoesNotExist:
            logger.warning(f"Kanban column not found for deletion: {column_id}")
            raise interface.KanbanColumnNotFoundByIdException(column_id)

