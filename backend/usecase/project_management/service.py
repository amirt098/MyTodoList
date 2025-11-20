# Standard library
import logging

# Third-party
# (none needed)

# Internal - from other modules
from repository.project import interface as project_repository_interface
from utils.date_utils import interface as date_utils_interface

# Internal - from same module
from . import interface

logger = logging.getLogger(__name__)


def _repo_dto_to_usecase_dto(repo_dto: project_repository_interface.ProjectDTO) -> interface.ProjectDTO:
    """Simple converter: Repository ProjectDTO to UseCase ProjectDTO."""
    return interface.ProjectDTO(
        project_id=repo_dto.project_id,
        name=repo_dto.name,
        description=repo_dto.description,
        is_private=repo_dto.is_private,
        owner_id=repo_dto.owner_id,
        created_at=repo_dto.created_at,
        updated_at=repo_dto.updated_at
    )


def _repo_member_dto_to_usecase_dto(repo_dto: project_repository_interface.ProjectMemberDTO) -> interface.ProjectMemberDTO:
    """Simple converter: Repository ProjectMemberDTO to UseCase ProjectMemberDTO."""
    return interface.ProjectMemberDTO(
        member_id=repo_dto.member_id,
        project_id=repo_dto.project_id,
        user_id=repo_dto.user_id,
        role=repo_dto.role,
        joined_at=repo_dto.joined_at
    )


def _check_project_access(project_dto: project_repository_interface.ProjectDTO, user_id: int, require_owner: bool = False, require_admin: bool = False) -> bool:
    """
    Check if user has access to project.
    
    Args:
        project_dto: Project DTO
        user_id: User ID to check
        require_owner: If True, user must be owner
        require_admin: If True, user must be owner or admin
        
    Returns:
        True if user has access, False otherwise
    """
    # Owner always has access
    if project_dto.owner_id == user_id:
        return True
    
    # For private projects, only owner and members have access
    if project_dto.is_private:
        # We'll need to check membership in the service method
        return False
    
    # For public projects, anyone can view
    if not require_owner and not require_admin:
        return True
    
    return False


def _check_member_permission(member_dto: project_repository_interface.ProjectMemberDTO | None, require_owner: bool = False, require_admin: bool = False) -> bool:
    """
    Check if member has required permission.
    
    Args:
        member_dto: ProjectMember DTO or None
        require_owner: If True, must be owner
        require_admin: If True, must be owner or admin
        
    Returns:
        True if member has permission, False otherwise
    """
    if member_dto is None:
        return False
    
    if require_owner:
        return member_dto.role == 'Owner'
    
    if require_admin:
        return member_dto.role in ['Owner', 'Admin']
    
    return True


class ProjectManagementService(interface.AbstractProjectManagementService):
    """Service for managing project operations."""
    
    def __init__(
        self,
        project_repo: project_repository_interface.AbstractProjectRepository,
        date_time_service: date_utils_interface.AbstractDateTimeService,
    ):
        self.project_repo = project_repo
        self.date_time_service = date_time_service
    
    def create_project(self, request: interface.CreateProjectRequest) -> interface.CreateProjectResponse:
        logger.info(f"Creating project with name: {request.name}", extra={"input": request.model_dump()})
        
        if not request.name:
            logger.warning("Project creation failed - name is required")
            raise interface.ProjectNameRequiredException()
        
        # Calculate timestamps in usecase layer
        now_dto = self.date_time_service.now()
        
        # Create ProjectCreateRequest with timestamps
        project_create_request = project_repository_interface.ProjectCreateRequest(
            name=request.name,
            description=request.description,
            is_private=request.is_private,
            owner_id=request.owner_id,
            created_at=now_dto.timestamp_ms,
            updated_at=now_dto.timestamp_ms
        )
        
        project_dto = self.project_repo.create(project_create_request)
        
        # Create owner as first member
        member_create_request = project_repository_interface.ProjectMemberCreateRequest(
            project_id=project_dto.project_id,
            user_id=request.owner_id,
            role='Owner',
            joined_at=now_dto.timestamp_ms
        )
        self.project_repo.create_member(member_create_request)
        
        response = interface.CreateProjectResponse(
            project_id=project_dto.project_id,
            name=project_dto.name,
            is_private=project_dto.is_private,
            owner_id=project_dto.owner_id,
            created_at=project_dto.created_at
        )
        
        logger.info(f"Project created successfully: {response.project_id}", extra={"output": response.model_dump()})
        return response
    
    def get_project_by_id(self, request: interface.GetProjectRequest) -> interface.ProjectDTO:
        logger.info(f"Fetching project by id: {request.project_id}", extra={"input": request.model_dump()})
        
        # Get project
        project_dto = self.project_repo.get_by_id(request.project_id)
        if not project_dto:
            logger.warning(f"Project not found: {request.project_id}")
            raise interface.ProjectNotFoundByIdException(request.project_id)
        
        # Check access
        # For private projects, check if user is owner or member
        if project_dto.is_private:
            if project_dto.owner_id != request.user_id:
                # Check if user is a member
                member = self.project_repo.get_member(request.project_id, request.user_id)
                if not member:
                    logger.warning(f"Access denied - user {request.user_id} tried to access private project {request.project_id}")
                    raise interface.ProjectAccessDeniedException(request.project_id, request.user_id)
        
        response = _repo_dto_to_usecase_dto(project_dto)
        
        logger.info(f"Project fetched successfully: {request.project_id}", extra={"output": response.model_dump()})
        return response
    
    def get_projects(self, request: interface.ProjectFilter) -> interface.ProjectListResponse:
        logger.info(f"Fetching projects for user: {request.user_id}", extra={"input": request.model_dump()})
        
        # Convert to repository filter
        # Get projects where user is owner or member
        project_filter = project_repository_interface.ProjectFilter(
            owner_id=request.user_id,  # Projects owned by user
            is_private=request.is_private,
            search=request.search,
            order_by=request.order_by,
            limit=request.limit,
            offset=request.offset
        )
        
        # Get owned projects
        owned_projects = self.project_repo.get_projects(project_filter)
        
        # Get projects where user is a member
        member_filter = project_repository_interface.ProjectMemberFilter(
            user_id=request.user_id,
            role=request.role if hasattr(request, 'role') else None,
            order_by=request.order_by,
            limit=None,  # Get all memberships
            offset=None
        )
        members = self.project_repo.get_members(member_filter)
        
        # Get project IDs where user is a member
        member_project_ids = {member.project_id for member in members}
        
        # Get projects where user is a member (but not owner)
        member_projects = []
        for project_id in member_project_ids:
            project_dto = self.project_repo.get_by_id(project_id)
            if project_dto and project_dto.owner_id != request.user_id:
                # Apply additional filters
                if request.is_private is not None and project_dto.is_private != request.is_private:
                    continue
                if request.search:
                    if request.search.lower() not in project_dto.name.lower() and \
                       request.search.lower() not in (project_dto.description or "").lower():
                        continue
                member_projects.append(project_dto)
        
        # Combine and deduplicate
        all_projects = {p.project_id: p for p in owned_projects}
        for p in member_projects:
            all_projects[p.project_id] = p
        
        # Convert to usecase DTOs
        projects = [_repo_dto_to_usecase_dto(dto) for dto in all_projects.values()]
        
        # Apply ordering
        if request.order_by:
            reverse = request.order_by.startswith('-')
            order_field = request.order_by.lstrip('-')
            projects.sort(key=lambda p: getattr(p, order_field, 0), reverse=reverse)
        
        # Apply pagination
        if request.offset is not None and request.limit is not None:
            projects = projects[request.offset:request.offset + request.limit]
        
        response = interface.ProjectListResponse(
            projects=projects,
            total=len(projects)
        )
        
        logger.info(f"Found {len(projects)} projects for user: {request.user_id}", extra={"output": {"count": len(projects)}})
        return response
    
    def update_project(self, request: interface.UpdateProjectRequest) -> interface.UpdateProjectResponse:
        logger.info(f"Updating project: {request.project_id}", extra={"input": request.model_dump()})
        
        # Verify project exists and user has access
        existing_project_dto = self.project_repo.get_by_id(request.project_id)
        if not existing_project_dto:
            logger.warning(f"Project update failed - project not found: {request.project_id}")
            raise interface.ProjectNotFoundByIdException(request.project_id)
        
        # Check access - must be owner or admin
        if existing_project_dto.owner_id != request.user_id:
            member = self.project_repo.get_member(request.project_id, request.user_id)
            if not member or member.role not in ['Owner', 'Admin']:
                logger.warning(f"Access denied - user {request.user_id} tried to update project {request.project_id}")
                raise interface.ProjectAccessDeniedException(request.project_id, request.user_id)
        
        # Calculate updated timestamp in usecase layer
        now_dto = self.date_time_service.now()
        
        # Create ProjectUpdateRequest with only provided fields
        project_update_request = project_repository_interface.ProjectUpdateRequest(
            name=request.name,
            description=request.description,
            is_private=request.is_private,
            updated_at=now_dto.timestamp_ms
        )
        
        updated_project_dto = self.project_repo.update(request.project_id, project_update_request)
        
        response = interface.UpdateProjectResponse(
            project_id=updated_project_dto.project_id,
            name=updated_project_dto.name,
            description=updated_project_dto.description,
            is_private=updated_project_dto.is_private,
            owner_id=updated_project_dto.owner_id,
            updated_at=updated_project_dto.updated_at
        )
        
        logger.info(f"Project updated successfully: {request.project_id}", extra={"output": response.model_dump()})
        return response
    
    def delete_project(self, request: interface.DeleteProjectRequest) -> interface.DeleteProjectResponse:
        logger.info(f"Deleting project: {request.project_id}", extra={"input": request.model_dump()})
        
        # Verify project exists and user has access
        existing_project_dto = self.project_repo.get_by_id(request.project_id)
        if not existing_project_dto:
            logger.warning(f"Project deletion failed - project not found: {request.project_id}")
            raise interface.ProjectNotFoundByIdException(request.project_id)
        
        # Only owner can delete
        if existing_project_dto.owner_id != request.user_id:
            logger.warning(f"Access denied - user {request.user_id} tried to delete project {request.project_id}")
            raise interface.ProjectAccessDeniedException(request.project_id, request.user_id)
        
        # Delete project (members will be cascade deleted if foreign key, but we're using IntegerField)
        # So we need to delete members manually
        members = self.project_repo.get_members(
            project_repository_interface.ProjectMemberFilter(project_id=request.project_id)
        )
        for member in members:
            self.project_repo.delete_member(request.project_id, member.user_id)
        
        # Delete project
        self.project_repo.delete(request.project_id)
        
        response = interface.DeleteProjectResponse(
            success=True,
            message=f"Project {request.project_id} deleted successfully"
        )
        
        logger.info(f"Project deleted successfully: {request.project_id}", extra={"output": response.model_dump()})
        return response
    
    def add_member(self, request: interface.AddMemberRequest) -> interface.AddMemberResponse:
        logger.info(f"Adding member to project: project_id={request.project_id}, new_user_id={request.new_user_id}", 
                   extra={"input": request.model_dump()})
        
        # Verify project exists
        project_dto = self.project_repo.get_by_id(request.project_id)
        if not project_dto:
            logger.warning(f"Project not found: {request.project_id}")
            raise interface.ProjectNotFoundByIdException(request.project_id)
        
        # Check permission - must be owner or admin
        if project_dto.owner_id != request.user_id:
            member = self.project_repo.get_member(request.project_id, request.user_id)
            if not member or member.role not in ['Owner', 'Admin']:
                logger.warning(f"Access denied - user {request.user_id} tried to add member to project {request.project_id}")
                raise interface.ProjectAccessDeniedException(request.project_id, request.user_id)
        
        # Calculate timestamp
        now_dto = self.date_time_service.now()
        
        # Create member
        member_create_request = project_repository_interface.ProjectMemberCreateRequest(
            project_id=request.project_id,
            user_id=request.new_user_id,
            role=request.role,
            joined_at=now_dto.timestamp_ms
        )
        
        member_dto = self.project_repo.create_member(member_create_request)
        
        response = interface.AddMemberResponse(
            member_id=member_dto.member_id,
            project_id=member_dto.project_id,
            user_id=member_dto.user_id,
            role=member_dto.role,
            joined_at=member_dto.joined_at
        )
        
        logger.info(f"Member added successfully: {response.member_id}", extra={"output": response.model_dump()})
        return response
    
    def remove_member(self, request: interface.RemoveMemberRequest) -> interface.RemoveMemberResponse:
        logger.info(f"Removing member from project: project_id={request.project_id}, remove_user_id={request.remove_user_id}", 
                   extra={"input": request.model_dump()})
        
        # Verify project exists
        project_dto = self.project_repo.get_by_id(request.project_id)
        if not project_dto:
            logger.warning(f"Project not found: {request.project_id}")
            raise interface.ProjectNotFoundByIdException(request.project_id)
        
        # Check permission - must be owner or admin
        if project_dto.owner_id != request.user_id:
            member = self.project_repo.get_member(request.project_id, request.user_id)
            if not member or member.role not in ['Owner', 'Admin']:
                logger.warning(f"Access denied - user {request.user_id} tried to remove member from project {request.project_id}")
                raise interface.ProjectAccessDeniedException(request.project_id, request.user_id)
        
        # Cannot remove owner
        if project_dto.owner_id == request.remove_user_id:
            logger.warning(f"Cannot remove owner from project {request.project_id}")
            raise interface.ProjectAccessDeniedException(request.project_id, request.user_id)
        
        # Verify member exists
        member = self.project_repo.get_member(request.project_id, request.remove_user_id)
        if not member:
            logger.warning(f"Project member not found: project_id={request.project_id}, user_id={request.remove_user_id}")
            raise interface.ProjectMemberNotFoundException(request.project_id, request.remove_user_id)
        
        # Delete member
        self.project_repo.delete_member(request.project_id, request.remove_user_id)
        
        response = interface.RemoveMemberResponse(
            success=True,
            message=f"Member {request.remove_user_id} removed from project {request.project_id} successfully"
        )
        
        logger.info(f"Member removed successfully", extra={"output": response.model_dump()})
        return response
    
    def update_member_role(self, request: interface.UpdateMemberRoleRequest) -> interface.UpdateMemberRoleResponse:
        logger.info(f"Updating member role: project_id={request.project_id}, update_user_id={request.update_user_id}, new_role={request.new_role}", 
                   extra={"input": request.model_dump()})
        
        # Verify project exists
        project_dto = self.project_repo.get_by_id(request.project_id)
        if not project_dto:
            logger.warning(f"Project not found: {request.project_id}")
            raise interface.ProjectNotFoundByIdException(request.project_id)
        
        # Check permission - must be owner
        if project_dto.owner_id != request.user_id:
            logger.warning(f"Access denied - user {request.user_id} tried to update member role in project {request.project_id}")
            raise interface.ProjectAccessDeniedException(request.project_id, request.user_id)
        
        # Cannot change owner's role
        if project_dto.owner_id == request.update_user_id:
            logger.warning(f"Cannot change owner's role in project {request.project_id}")
            raise interface.ProjectAccessDeniedException(request.project_id, request.user_id)
        
        # Verify member exists
        member = self.project_repo.get_member(request.project_id, request.update_user_id)
        if not member:
            logger.warning(f"Project member not found: project_id={request.project_id}, user_id={request.update_user_id}")
            raise interface.ProjectMemberNotFoundException(request.project_id, request.update_user_id)
        
        # Update member role
        member_update_request = project_repository_interface.ProjectMemberUpdateRequest(
            role=request.new_role
        )
        
        updated_member_dto = self.project_repo.update_member(request.project_id, request.update_user_id, member_update_request)
        
        response = interface.UpdateMemberRoleResponse(
            member_id=updated_member_dto.member_id,
            project_id=updated_member_dto.project_id,
            user_id=updated_member_dto.user_id,
            role=updated_member_dto.role
        )
        
        logger.info(f"Member role updated successfully", extra={"output": response.model_dump()})
        return response

