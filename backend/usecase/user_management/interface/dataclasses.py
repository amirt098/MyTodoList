# Standard library
from typing import Optional

# Third-party
from pydantic import EmailStr, Field

# Internal - from other modules
from lib.base_models import BaseRequest, BaseResponse

# Internal - from same interface module
# (none needed)


class RegisterUserRequest(BaseRequest):
    """Request DTO for user registration."""
    email: EmailStr | None = None
    username: str
    password: str = Field(..., min_length=8)
    phone: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool = True
    is_verified: bool = False


class RegisterUserResponse(BaseResponse):
    """Response DTO for user registration."""
    user_id: int
    email: str
    created_at: int


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


class UpdateProfileResponse(BaseResponse):
    """Response DTO for profile update."""
    user_id: int
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    phone: str
    updated_at: int

