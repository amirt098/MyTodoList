# Standard library
import logging

# Third-party
# (none needed)

# Internal - from other modules
from repository.saved_filter import interface as saved_filter_repository_interface
from utils.date_utils import interface as date_utils_interface

# Internal - from same module
from . import interface

logger = logging.getLogger(__name__)


def _repo_dto_to_usecase_dto(repo_dto: saved_filter_repository_interface.SavedFilterDTO) -> interface.SavedFilterDTO:
    """Simple converter: Repository SavedFilterDTO to UseCase SavedFilterDTO."""
    return interface.SavedFilterDTO(
        filter_id=repo_dto.filter_id,
        name=repo_dto.name,
        description=repo_dto.description,
        filter_criteria=repo_dto.filter_criteria,
        user_id=repo_dto.user_id,
        is_default=repo_dto.is_default,
        created_at=repo_dto.created_at,
        updated_at=repo_dto.updated_at
    )


class FilterManagementService(interface.AbstractFilterManagementService):
    """Service for managing saved filter operations."""
    
    def __init__(
        self,
        saved_filter_repo: saved_filter_repository_interface.AbstractSavedFilterRepository,
        date_time_service: date_utils_interface.AbstractDateTimeService,
    ):
        self.saved_filter_repo = saved_filter_repo
        self.date_time_service = date_time_service
    
    def save_filter(self, request: interface.SaveFilterRequest) -> interface.SaveFilterResponse:
        logger.info(f"Saving filter: {request.name}", extra={"input": request.model_dump()})
        
        if not request.name:
            logger.warning("Filter save failed - name is required")
            raise interface.SavedFilterNameRequiredException()
        
        # Calculate timestamps
        now_dto = self.date_time_service.now()
        
        # Create saved filter
        filter_create_request = saved_filter_repository_interface.SavedFilterCreateRequest(
            name=request.name,
            description=request.description or "",
            filter_criteria=request.filter_criteria,
            user_id=request.user_id,
            is_default=request.is_default,
            created_at=now_dto.timestamp_ms,
            updated_at=now_dto.timestamp_ms
        )
        
        filter_dto = self.saved_filter_repo.create(filter_create_request)
        
        response = interface.SaveFilterResponse(
            filter_id=filter_dto.filter_id,
            name=filter_dto.name,
            description=filter_dto.description,
            filter_criteria=filter_dto.filter_criteria,
            created_at=filter_dto.created_at
        )
        
        logger.info(f"Filter saved successfully: {response.filter_id}", extra={"output": response.model_dump()})
        return response
    
    def get_saved_filters(self, request: interface.GetSavedFiltersRequest) -> interface.GetSavedFiltersResponse:
        logger.info(f"Getting saved filters for user: {request.user_id}", extra={"input": request.model_dump()})
        
        # Get saved filters
        filter_filter = saved_filter_repository_interface.SavedFilterFilter(
            user_id=request.user_id,
            is_default=request.is_default,
            order_by='-created_at'
        )
        filter_dtos = self.saved_filter_repo.get_filters(filter_filter)
        
        # Convert to usecase DTOs
        filters = [_repo_dto_to_usecase_dto(dto) for dto in filter_dtos]
        
        response = interface.GetSavedFiltersResponse(
            filters=filters,
            total=len(filters)
        )
        
        logger.info(f"Found {len(filters)} saved filters for user: {request.user_id}", 
                   extra={"output": {"count": len(filters)}})
        return response
    
    def delete_saved_filter(self, request: interface.DeleteSavedFilterRequest) -> interface.DeleteSavedFilterResponse:
        logger.info(f"Deleting saved filter: {request.filter_id}", extra={"input": request.model_dump()})
        
        # Verify filter exists and user has access
        filter_dto = self.saved_filter_repo.get_by_id(request.filter_id)
        if not filter_dto:
            logger.warning(f"Saved filter not found: {request.filter_id}")
            raise interface.SavedFilterNotFoundByIdException(request.filter_id)
        
        if filter_dto.user_id != request.user_id:
            logger.warning(f"Access denied - user {request.user_id} tried to delete filter {request.filter_id}")
            raise interface.SavedFilterAccessDeniedException(request.filter_id, request.user_id)
        
        # Delete filter
        self.saved_filter_repo.delete(request.filter_id)
        
        response = interface.DeleteSavedFilterResponse(
            success=True,
            message=f"Saved filter {request.filter_id} deleted successfully"
        )
        
        logger.info(f"Saved filter deleted successfully: {request.filter_id}", extra={"output": response.model_dump()})
        return response

