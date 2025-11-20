# Standard library
from abc import ABC, abstractmethod

# Internal - from same interface module (direct import, no interface. prefix needed)
from .dataclasses import (
    CreateProjectRequest, CreateProjectResponse,
    GetProjectRequest, ProjectDTO,
    ProjectFilter, ProjectListResponse,
    UpdateProjectRequest, UpdateProjectResponse,
    DeleteProjectRequest, DeleteProjectResponse,
    AddMemberRequest, AddMemberResponse,
    RemoveMemberRequest, RemoveMemberResponse,
    UpdateMemberRoleRequest, UpdateMemberRoleResponse
)


class AbstractProjectManagementService(ABC):
    """Interface for project management operations."""
    
    @abstractmethod
    def create_project(self, request: CreateProjectRequest) -> CreateProjectResponse:
        """
        Create a new project.
        
        Args:
            request: CreateProjectRequest with project information and owner_id
            
        Returns:
            CreateProjectResponse with created project information
            
        Raises:
            ProjectNameRequiredException: If name is missing
        """
        pass
    
    @abstractmethod
    def get_project_by_id(self, request: GetProjectRequest) -> ProjectDTO:
        """
        Get a single project by ID.
        
        Args:
            request: GetProjectRequest with project_id and user_id
            
        Returns:
            ProjectDTO with project information
            
        Raises:
            ProjectNotFoundByIdException: If project doesn't exist
            ProjectAccessDeniedException: If user doesn't have access to project
        """
        pass
    
    @abstractmethod
    def get_projects(self, request: ProjectFilter) -> ProjectListResponse:
        """
        Get projects with filtering.
        
        Args:
            request: ProjectFilter with filters and user_id
            
        Returns:
            ProjectListResponse with list of projects and total count
        """
        pass
    
    @abstractmethod
    def update_project(self, request: UpdateProjectRequest) -> UpdateProjectResponse:
        """
        Update an existing project.
        
        Args:
            request: UpdateProjectRequest with project_id, user_id, and fields to update
            
        Returns:
            UpdateProjectResponse with updated project information
            
        Raises:
            ProjectNotFoundByIdException: If project doesn't exist
            ProjectAccessDeniedException: If user doesn't have access to project
        """
        pass
    
    @abstractmethod
    def delete_project(self, request: DeleteProjectRequest) -> DeleteProjectResponse:
        """
        Delete a project.
        
        Args:
            request: DeleteProjectRequest with project_id and user_id
            
        Returns:
            DeleteProjectResponse with success status
            
        Raises:
            ProjectNotFoundByIdException: If project doesn't exist
            ProjectAccessDeniedException: If user doesn't have access to project
        """
        pass
    
    @abstractmethod
    def add_member(self, request: AddMemberRequest) -> AddMemberResponse:
        """
        Add a member to a project.
        
        Args:
            request: AddMemberRequest with project_id, user_id (requester), new_user_id, and role
            
        Returns:
            AddMemberResponse with created member information
            
        Raises:
            ProjectNotFoundByIdException: If project doesn't exist
            ProjectAccessDeniedException: If user doesn't have permission to add members
            ProjectMemberAlreadyExistsException: If member already exists
        """
        pass
    
    @abstractmethod
    def remove_member(self, request: RemoveMemberRequest) -> RemoveMemberResponse:
        """
        Remove a member from a project.
        
        Args:
            request: RemoveMemberRequest with project_id, user_id (requester), and remove_user_id
            
        Returns:
            RemoveMemberResponse with success status
            
        Raises:
            ProjectNotFoundByIdException: If project doesn't exist
            ProjectAccessDeniedException: If user doesn't have permission to remove members
            ProjectMemberNotFoundException: If member doesn't exist
        """
        pass
    
    @abstractmethod
    def update_member_role(self, request: UpdateMemberRoleRequest) -> UpdateMemberRoleResponse:
        """
        Update a member's role in a project.
        
        Args:
            request: UpdateMemberRoleRequest with project_id, user_id (requester), update_user_id, and new_role
            
        Returns:
            UpdateMemberRoleResponse with updated member information
            
        Raises:
            ProjectNotFoundByIdException: If project doesn't exist
            ProjectAccessDeniedException: If user doesn't have permission to update roles
            ProjectMemberNotFoundException: If member doesn't exist
        """
        pass

