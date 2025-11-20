# Standard library
import logging

# Third-party
# (none needed)

# Internal - from other modules
# (none needed)

# Internal - from same module
from .models import Project, ProjectMember
from . import interface

logger = logging.getLogger(__name__)


class ProjectRepositoryService(interface.AbstractProjectRepository):
    """Repository service for project data access."""
    
    def create(self, project_data: interface.ProjectCreateRequest) -> interface.ProjectDTO:
        logger.info(f"Creating project with name: {project_data.name}", extra={"input": project_data.model_dump()})
        
        if not project_data.name:
            logger.warning("Failed to create project - name is required")
            raise interface.ProjectNameRequiredException()
        
        project = Project()
        project.name = project_data.name
        project.description = project_data.description or ""
        project.is_private = project_data.is_private
        project.owner_id = project_data.owner_id
        project.created_at = project_data.created_at
        project.updated_at = project_data.updated_at
        
        project.save()
        
        result = interface.ProjectDTO.from_model(project)
        logger.info(f"Project created successfully: {result.project_id}", extra={"output": result.model_dump()})
        return result
    
    def get_by_id(self, project_id: int) -> interface.ProjectDTO | None:
        logger.info(f"Fetching project by id: {project_id}", extra={"input": {"project_id": project_id}})
        
        try:
            project = Project.objects.get(id=project_id)
            result = interface.ProjectDTO.from_model(project)
            logger.info(f"Project fetched successfully: {project_id}", extra={"output": result.model_dump()})
            return result
        except Project.DoesNotExist:
            logger.info(f"Project not found: {project_id}")
            return None
    
    def get_projects(self, filters: interface.ProjectFilter) -> list[interface.ProjectDTO]:
        logger.info(f"Filtering projects", extra={"input": filters.model_dump()})
        
        queryset = Project.objects.all()
        
        # Apply basic filters
        if filters.owner_id:
            queryset = queryset.filter(owner_id=filters.owner_id)
        if filters.is_private is not None:
            queryset = queryset.filter(is_private=filters.is_private)
        
        if filters.search:
            from django.db.models import Q
            queryset = queryset.filter(
                Q(name__icontains=filters.search) |
                Q(description__icontains=filters.search)
            )
        
        # Apply ordering
        queryset = queryset.order_by(filters.order_by)
        
        # Apply pagination
        if filters.offset is not None and filters.limit is not None:
            queryset = queryset[filters.offset:filters.offset + filters.limit]
        
        results = [interface.ProjectDTO.from_model(project) for project in queryset]
        logger.info(f"Found {len(results)} projects matching filter", extra={"output": {"count": len(results)}})
        return results
    
    def update(self, project_id: int, project_data: interface.ProjectUpdateRequest) -> interface.ProjectDTO:
        logger.info(f"Updating project: {project_id}", extra={"input": {"project_id": project_id}})
        
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            logger.warning(f"Project not found for update: {project_id}")
            raise interface.ProjectNotFoundByIdException(project_id)
        
        # Update fields if provided
        if project_data.name is not None:
            project.name = project_data.name
        if project_data.description is not None:
            project.description = project_data.description
        if project_data.is_private is not None:
            project.is_private = project_data.is_private
        # Updated timestamp is provided by usecase layer
        if project_data.updated_at:
            project.updated_at = project_data.updated_at
        
        project.save()
        
        result = interface.ProjectDTO.from_model(project)
        logger.info(f"Project updated successfully: {project_id}", extra={"output": result.model_dump()})
        return result
    
    def delete(self, project_id: int) -> None:
        logger.info(f"Deleting project: {project_id}", extra={"input": {"project_id": project_id}})
        
        try:
            project = Project.objects.get(id=project_id)
            project.delete()
            logger.info(f"Project deleted successfully: {project_id}")
        except Project.DoesNotExist:
            logger.warning(f"Project not found for deletion: {project_id}")
            raise interface.ProjectNotFoundByIdException(project_id)
    
    # Project Member methods
    
    def create_member(self, member_data: interface.ProjectMemberCreateRequest) -> interface.ProjectMemberDTO:
        logger.info(f"Creating project member: project_id={member_data.project_id}, user_id={member_data.user_id}", 
                   extra={"input": member_data.model_dump()})
        
        # Check if member already exists
        if ProjectMember.objects.filter(project_id=member_data.project_id, user_id=member_data.user_id).exists():
            logger.warning(f"Project member already exists: project_id={member_data.project_id}, user_id={member_data.user_id}")
            raise interface.ProjectMemberAlreadyExistsException(member_data.project_id, member_data.user_id)
        
        member = ProjectMember()
        member.project_id = member_data.project_id
        member.user_id = member_data.user_id
        member.role = member_data.role
        member.joined_at = member_data.joined_at
        
        member.save()
        
        result = interface.ProjectMemberDTO.from_model(member)
        logger.info(f"Project member created successfully: {result.member_id}", extra={"output": result.model_dump()})
        return result
    
    def get_member(self, project_id: int, user_id: int) -> interface.ProjectMemberDTO | None:
        logger.info(f"Fetching project member: project_id={project_id}, user_id={user_id}", 
                   extra={"input": {"project_id": project_id, "user_id": user_id}})
        
        try:
            member = ProjectMember.objects.get(project_id=project_id, user_id=user_id)
            result = interface.ProjectMemberDTO.from_model(member)
            logger.info(f"Project member fetched successfully", extra={"output": result.model_dump()})
            return result
        except ProjectMember.DoesNotExist:
            logger.info(f"Project member not found: project_id={project_id}, user_id={user_id}")
            return None
    
    def get_members(self, filters: interface.ProjectMemberFilter) -> list[interface.ProjectMemberDTO]:
        logger.info(f"Filtering project members", extra={"input": filters.model_dump()})
        
        queryset = ProjectMember.objects.all()
        
        # Apply basic filters
        if filters.project_id:
            queryset = queryset.filter(project_id=filters.project_id)
        if filters.user_id:
            queryset = queryset.filter(user_id=filters.user_id)
        if filters.role:
            queryset = queryset.filter(role=filters.role)
        
        # Apply ordering (use joined_at for ProjectMember, fallback to id)
        order_by = filters.order_by
        # ProjectMember doesn't have created_at, use joined_at or id
        if order_by and 'created_at' in order_by:
            order_by = order_by.replace('created_at', 'joined_at')
        elif not order_by or order_by == '-created_at':
            order_by = '-joined_at'
        queryset = queryset.order_by(order_by)
        
        # Apply pagination
        if filters.offset is not None and filters.limit is not None:
            queryset = queryset[filters.offset:filters.offset + filters.limit]
        
        results = [interface.ProjectMemberDTO.from_model(member) for member in queryset]
        logger.info(f"Found {len(results)} project members matching filter", extra={"output": {"count": len(results)}})
        return results
    
    def update_member(self, project_id: int, user_id: int, member_data: interface.ProjectMemberUpdateRequest) -> interface.ProjectMemberDTO:
        logger.info(f"Updating project member: project_id={project_id}, user_id={user_id}", 
                   extra={"input": {"project_id": project_id, "user_id": user_id}})
        
        try:
            member = ProjectMember.objects.get(project_id=project_id, user_id=user_id)
        except ProjectMember.DoesNotExist:
            logger.warning(f"Project member not found for update: project_id={project_id}, user_id={user_id}")
            raise interface.ProjectMemberNotFoundException(project_id, user_id)
        
        # Update fields if provided
        if member_data.role is not None:
            member.role = member_data.role
        
        member.save()
        
        result = interface.ProjectMemberDTO.from_model(member)
        logger.info(f"Project member updated successfully", extra={"output": result.model_dump()})
        return result
    
    def delete_member(self, project_id: int, user_id: int) -> None:
        logger.info(f"Deleting project member: project_id={project_id}, user_id={user_id}", 
                   extra={"input": {"project_id": project_id, "user_id": user_id}})
        
        try:
            member = ProjectMember.objects.get(project_id=project_id, user_id=user_id)
            member.delete()
            logger.info(f"Project member deleted successfully: project_id={project_id}, user_id={user_id}")
        except ProjectMember.DoesNotExist:
            logger.warning(f"Project member not found for deletion: project_id={project_id}, user_id={user_id}")
            raise interface.ProjectMemberNotFoundException(project_id, user_id)

