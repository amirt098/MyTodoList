# Standard library
from abc import ABC, abstractmethod

# Internal - from same interface module (direct import, no interface. prefix needed)
from .dataclasses import (
    ProjectDTO, ProjectFilter, ProjectCreateRequest, ProjectUpdateRequest,
    ProjectMemberDTO, ProjectMemberFilter, ProjectMemberCreateRequest, ProjectMemberUpdateRequest
)


class AbstractProjectRepository(ABC):
    """Interface for project repository operations."""
    
    @abstractmethod
    def create(self, project_data: ProjectCreateRequest) -> ProjectDTO:
        """
        Create a new project in the database.
        
        Args:
            project_data: ProjectCreateRequest object with project information (including created_at and updated_at timestamps)
            
        Returns:
            ProjectDTO with created project information
            
        Raises:
            ProjectNameRequiredException: If name is missing
        """
        pass
    
    @abstractmethod
    def get_by_id(self, project_id: int) -> ProjectDTO | None:
        """
        Get project by ID.
        
        Args:
            project_id: Project ID to fetch
            
        Returns:
            ProjectDTO if found, None otherwise
        """
        pass
    
    @abstractmethod
    def get_projects(self, filters: ProjectFilter) -> list[ProjectDTO]:
        """
        Get projects with filtering.
        
        General method for querying projects with various filters.
        
        Args:
            filters: ProjectFilter Pydantic object extending BaseFilter from lib
            
        Returns:
            List of ProjectDTO matching the filters
        """
        pass
    
    @abstractmethod
    def update(self, project_id: int, project_data: ProjectUpdateRequest) -> ProjectDTO:
        """
        Update an existing project.
        
        Args:
            project_id: Project ID to update
            project_data: ProjectUpdateRequest with fields to update (only provided fields will be updated, including updated_at timestamp)
            
        Returns:
            ProjectDTO with updated project information
            
        Raises:
            ProjectNotFoundByIdException: If project doesn't exist
        """
        pass
    
    @abstractmethod
    def delete(self, project_id: int) -> None:
        """
        Delete a project.
        
        Args:
            project_id: Project ID to delete
            
        Raises:
            ProjectNotFoundByIdException: If project doesn't exist
        """
        pass
    
    # Project Member methods
    
    @abstractmethod
    def create_member(self, member_data: ProjectMemberCreateRequest) -> ProjectMemberDTO:
        """
        Create a new project member.
        
        Args:
            member_data: ProjectMemberCreateRequest object with member information (including joined_at timestamp)
            
        Returns:
            ProjectMemberDTO with created member information
            
        Raises:
            ProjectMemberAlreadyExistsException: If member already exists
        """
        pass
    
    @abstractmethod
    def get_member(self, project_id: int, user_id: int) -> ProjectMemberDTO | None:
        """
        Get project member by project_id and user_id.
        
        Args:
            project_id: Project ID
            user_id: User ID
            
        Returns:
            ProjectMemberDTO if found, None otherwise
        """
        pass
    
    @abstractmethod
    def get_members(self, filters: ProjectMemberFilter) -> list[ProjectMemberDTO]:
        """
        Get project members with filtering.
        
        Args:
            filters: ProjectMemberFilter Pydantic object extending BaseFilter from lib
            
        Returns:
            List of ProjectMemberDTO matching the filters
        """
        pass
    
    @abstractmethod
    def update_member(self, project_id: int, user_id: int, member_data: ProjectMemberUpdateRequest) -> ProjectMemberDTO:
        """
        Update an existing project member.
        
        Args:
            project_id: Project ID
            user_id: User ID
            member_data: ProjectMemberUpdateRequest with fields to update
            
        Returns:
            ProjectMemberDTO with updated member information
            
        Raises:
            ProjectMemberNotFoundException: If member doesn't exist
        """
        pass
    
    @abstractmethod
    def delete_member(self, project_id: int, user_id: int) -> None:
        """
        Delete a project member.
        
        Args:
            project_id: Project ID
            user_id: User ID
            
        Raises:
            ProjectMemberNotFoundException: If member doesn't exist
        """
        pass

