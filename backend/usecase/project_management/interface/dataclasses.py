# Standard library
from typing import Optional, List

# Third-party
# (none needed)

# Internal - from other modules
from lib.base_models import BaseRequest, BaseResponse, BaseFilter

# Internal - from same interface module
# (none needed)


class CreateProjectRequest(BaseRequest):
    """Request DTO for creating a project."""
    name: str
    description: Optional[str] = None
    is_private: bool = True
    owner_id: int


class CreateProjectResponse(BaseResponse):
    """Response DTO for creating a project."""
    project_id: int
    name: str
    is_private: bool
    owner_id: int
    created_at: int


class GetProjectRequest(BaseRequest):
    """Request DTO for getting a project."""
    project_id: int
    user_id: int  # For access control


class ProjectDTO(BaseResponse):
    """Pydantic DTO for Project (used in get responses)."""
    project_id: int
    name: str
    description: str
    is_private: bool
    owner_id: int
    created_at: int
    updated_at: int


class ProjectFilter(BaseFilter):
    """Filter for querying projects (extends BaseFilter)."""
    user_id: int  # User ID to filter projects (owner or member)
    is_private: Optional[bool] = None
    search: Optional[str] = None


class ProjectListResponse(BaseResponse):
    """Response DTO for getting projects list."""
    projects: List[ProjectDTO]
    total: int


class UpdateProjectRequest(BaseRequest):
    """Request DTO for updating a project."""
    project_id: int
    user_id: int  # For access control
    name: Optional[str] = None
    description: Optional[str] = None
    is_private: Optional[bool] = None


class UpdateProjectResponse(BaseResponse):
    """Response DTO for updating a project."""
    project_id: int
    name: str
    description: str
    is_private: bool
    owner_id: int
    updated_at: int


class DeleteProjectRequest(BaseRequest):
    """Request DTO for deleting a project."""
    project_id: int
    user_id: int  # For access control


class DeleteProjectResponse(BaseResponse):
    """Response DTO for deleting a project."""
    success: bool
    message: str


# Project Member DTOs

class ProjectMemberDTO(BaseResponse):
    """Pydantic DTO for ProjectMember."""
    member_id: int
    project_id: int
    user_id: int
    role: str
    joined_at: int


class AddMemberRequest(BaseRequest):
    """Request DTO for adding a member to a project."""
    project_id: int
    user_id: int  # User adding the member (must be owner/admin)
    new_user_id: int  # User to add as member
    role: str = 'Member'


class AddMemberResponse(BaseResponse):
    """Response DTO for adding a member."""
    member_id: int
    project_id: int
    user_id: int
    role: str
    joined_at: int


class RemoveMemberRequest(BaseRequest):
    """Request DTO for removing a member from a project."""
    project_id: int
    user_id: int  # User removing the member (must be owner/admin)
    remove_user_id: int  # User to remove


class RemoveMemberResponse(BaseResponse):
    """Response DTO for removing a member."""
    success: bool
    message: str


class UpdateMemberRoleRequest(BaseRequest):
    """Request DTO for updating a member's role."""
    project_id: int
    user_id: int  # User updating the role (must be owner/admin)
    update_user_id: int  # User whose role to update
    new_role: str


class UpdateMemberRoleResponse(BaseResponse):
    """Response DTO for updating a member's role."""
    member_id: int
    project_id: int
    user_id: int
    role: str

