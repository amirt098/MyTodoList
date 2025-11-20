# Standard library
from typing import Optional, List

# Third-party
# (none needed)

# Internal - from other modules
from lib.base_models import BaseModel, BaseFilter

# Internal - from same interface module
# (none needed)


class ProjectCreateRequest(BaseModel):
    """Request for creating a project."""
    name: str
    description: Optional[str] = None
    is_private: bool = True
    owner_id: int
    created_at: int | None = None
    updated_at: int | None = None


class ProjectUpdateRequest(BaseModel):
    """Request for updating a project."""
    name: str | None = None
    description: str | None = None
    is_private: bool | None = None
    updated_at: int | None = None


class ProjectDTO(BaseModel):
    """DTO for Project responses."""
    project_id: int
    name: str
    description: str
    is_private: bool
    owner_id: int
    created_at: int
    updated_at: int
    
    @classmethod
    def from_model(cls, project) -> 'ProjectDTO':
        """Create ProjectDTO from Django Project model."""
        return cls(
            project_id=project.id,
            name=project.name,
            description=project.description or "",
            is_private=project.is_private,
            owner_id=project.owner_id,
            created_at=project.created_at,
            updated_at=project.updated_at
        )


class ProjectFilter(BaseFilter):
    """Filter for querying projects."""
    owner_id: Optional[int] = None
    is_private: Optional[bool] = None
    search: Optional[str] = None


class ProjectMemberCreateRequest(BaseModel):
    """Request for creating a project member."""
    project_id: int
    user_id: int
    role: str = 'Member'
    joined_at: int | None = None


class ProjectMemberUpdateRequest(BaseModel):
    """Request for updating a project member."""
    role: str | None = None


class ProjectMemberDTO(BaseModel):
    """DTO for ProjectMember responses."""
    member_id: int
    project_id: int
    user_id: int
    role: str
    joined_at: int
    
    @classmethod
    def from_model(cls, member) -> 'ProjectMemberDTO':
        """Create ProjectMemberDTO from Django ProjectMember model."""
        return cls(
            member_id=member.id,
            project_id=member.project_id,
            user_id=member.user_id,
            role=member.role,
            joined_at=member.joined_at
        )


class ProjectMemberFilter(BaseFilter):
    """Filter for querying project members."""
    project_id: Optional[int] = None
    user_id: Optional[int] = None
    role: Optional[str] = None

