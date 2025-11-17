# Standard library
from datetime import datetime
from typing import Optional

# Third-party
from pydantic import EmailStr, Field

# Internal - from other modules
from lib.base_models import BaseRequest, BaseResponse, BaseFilter

# Internal - from same interface module
# (none needed)


class RegisterUserRequest(BaseRequest):
    """Request DTO for user registration."""
    email: EmailStr
    password: str = Field(..., min_length=8)
    phone: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    
    def to_user_data(self, created_at, updated_at):
        """Convert to UserData for repository."""
        from repository.user.interface.dataclasses import UserData
        return UserData(
            email=self.email,
            password=self.password,
            phone=self.phone,
            first_name=self.first_name,
            last_name=self.last_name,
            is_active=True,
            is_verified=False,
            created_at=created_at,
            updated_at=updated_at
        )


class RegisterUserResponse(BaseResponse):
    """Response DTO for user registration."""
    user_id: int
    email: str
    created_at: datetime


class LoginRequest(BaseRequest):
    """Request DTO for user login."""
    email: EmailStr
    password: str


class LoginResponse(BaseResponse):
    """Response DTO for user login."""
    user_id: int
    token: str
    email: str


class PasswordRecoveryRequest(BaseRequest):
    """Request DTO for password recovery."""
    email: EmailStr


class PasswordRecoveryResponse(BaseResponse):
    """Response DTO for password recovery."""
    success: bool
    message: str


class UpdateProfileRequest(BaseRequest):
    """Request DTO for profile update."""
    user_id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    
    def to_user_data(self, updated_at):
        """Convert to UserData for repository update."""
        from repository.user.interface.dataclasses import UserData
        return UserData(
            email="",  # Not updating email
            password="",  # Not updating password
            phone=self.phone,
            first_name=self.first_name,
            last_name=self.last_name,
            is_active=None,  # Not updating
            is_verified=None,  # Not updating
            created_at=None,  # Not updating
            updated_at=updated_at
        )


class UpdateProfileResponse(BaseResponse):
    """Response DTO for profile update."""
    user_id: int
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    phone: str
    updated_at: datetime

