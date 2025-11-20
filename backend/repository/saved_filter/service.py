# Standard library
import logging

# Third-party
# (none needed)

# Internal - from other modules
# (none needed)

# Internal - from same module
from .models import SavedFilter
from . import interface

logger = logging.getLogger(__name__)


class SavedFilterRepositoryService(interface.AbstractSavedFilterRepository):
    """Repository service for saved filter data access."""
    
    def create(self, filter_data: interface.SavedFilterCreateRequest) -> interface.SavedFilterDTO:
        logger.info(f"Creating saved filter with name: {filter_data.name}", extra={"input": filter_data.model_dump()})
        
        if not filter_data.name:
            logger.warning("Failed to create saved filter - name is required")
            raise interface.SavedFilterNameRequiredException()
        
        saved_filter = SavedFilter()
        saved_filter.name = filter_data.name
        saved_filter.description = filter_data.description or ""
        saved_filter.filter_criteria = filter_data.filter_criteria or {}
        saved_filter.user_id = filter_data.user_id
        saved_filter.is_default = filter_data.is_default
        saved_filter.created_at = filter_data.created_at
        saved_filter.updated_at = filter_data.updated_at
        
        saved_filter.save()
        
        result = interface.SavedFilterDTO.from_model(saved_filter)
        logger.info(f"Saved filter created successfully: {result.filter_id}", extra={"output": result.model_dump()})
        return result
    
    def get_by_id(self, filter_id: int) -> interface.SavedFilterDTO | None:
        logger.info(f"Fetching saved filter by id: {filter_id}", extra={"input": {"filter_id": filter_id}})
        
        try:
            saved_filter = SavedFilter.objects.get(id=filter_id)
            result = interface.SavedFilterDTO.from_model(saved_filter)
            logger.info(f"Saved filter fetched successfully: {filter_id}", extra={"output": result.model_dump()})
            return result
        except SavedFilter.DoesNotExist:
            logger.info(f"Saved filter not found: {filter_id}")
            return None
    
    def get_filters(self, filters: interface.SavedFilterFilter) -> list[interface.SavedFilterDTO]:
        logger.info(f"Filtering saved filters", extra={"input": filters.model_dump()})
        
        queryset = SavedFilter.objects.all()
        
        # Apply basic filters
        if filters.user_id:
            queryset = queryset.filter(user_id=filters.user_id)
        if filters.is_default is not None:
            queryset = queryset.filter(is_default=filters.is_default)
        
        # Apply ordering
        queryset = queryset.order_by(filters.order_by)
        
        # Apply pagination
        if filters.offset is not None and filters.limit is not None:
            queryset = queryset[filters.offset:filters.offset + filters.limit]
        
        results = [interface.SavedFilterDTO.from_model(saved_filter) for saved_filter in queryset]
        logger.info(f"Found {len(results)} saved filters matching filter", extra={"output": {"count": len(results)}})
        return results
    
    def update(self, filter_id: int, filter_data: interface.SavedFilterUpdateRequest) -> interface.SavedFilterDTO:
        logger.info(f"Updating saved filter: {filter_id}", extra={"input": {"filter_id": filter_id}})
        
        try:
            saved_filter = SavedFilter.objects.get(id=filter_id)
        except SavedFilter.DoesNotExist:
            logger.warning(f"Saved filter not found for update: {filter_id}")
            raise interface.SavedFilterNotFoundByIdException(filter_id)
        
        # Update fields if provided
        if filter_data.name is not None:
            saved_filter.name = filter_data.name
        if filter_data.description is not None:
            saved_filter.description = filter_data.description
        if filter_data.filter_criteria is not None:
            saved_filter.filter_criteria = filter_data.filter_criteria
        if filter_data.is_default is not None:
            saved_filter.is_default = filter_data.is_default
        # Updated timestamp is provided by usecase layer
        if filter_data.updated_at:
            saved_filter.updated_at = filter_data.updated_at
        
        saved_filter.save()
        
        result = interface.SavedFilterDTO.from_model(saved_filter)
        logger.info(f"Saved filter updated successfully: {filter_id}", extra={"output": result.model_dump()})
        return result
    
    def delete(self, filter_id: int) -> None:
        logger.info(f"Deleting saved filter: {filter_id}", extra={"input": {"filter_id": filter_id}})
        
        try:
            saved_filter = SavedFilter.objects.get(id=filter_id)
            saved_filter.delete()
            logger.info(f"Saved filter deleted successfully: {filter_id}")
        except SavedFilter.DoesNotExist:
            logger.warning(f"Saved filter not found for deletion: {filter_id}")
            raise interface.SavedFilterNotFoundByIdException(filter_id)

