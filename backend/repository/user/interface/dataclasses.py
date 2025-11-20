# Standard library
from datetime import datetime
from typing import Optional

# Third-party
from pydantic import EmailStr, Field

# Internal - from other modules
from lib.base_models import BaseFilter, BaseModel

# Internal - from same interface module
# (none needed)


class UserData:
    """Data class for creating/updating users (not Pydantic, used internally)."""
    
    def __init__(
        self,
        email: str,
        password: str,
        phone: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        is_active: bool = True,
        is_verified: bool = False,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.email = email
        self.password = password
        self.phone = phone or ""
        self.first_name = first_name
        self.last_name = last_name
        self.is_active = is_active
        self.is_verified = is_verified
        self.created_at = created_at
        self.updated_at = updated_at


class UserUpdateRequest(BaseModel):
    email: str | None = None
    username: str | None = None
    password: str | None = None
    phone: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    is_active: bool | None = None
    is_verified: bool | None = None
    created_at: int | None = None
    updated_at: int | None = None


class UserCreateRequest(BaseModel):
    email: str | None = None
    username: str
    password: str
    phone: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool = True
    is_verified: bool = False
    created_at: int = None
    updated_at: int = None


class UserDTO(BaseModel):

    user_id: int
    email: str
    phone: str
    first_name: Optional[str]
    last_name: Optional[str]
    is_active: bool
    is_verified: bool
    created_at: int
    updated_at: int


    
    @classmethod
    def from_model(cls, user: 'User') -> 'UserDTO':
        """Create UserDTO from Django User model."""
        return cls(
            user_id=user.id,
            email=user.email,
            phone=user.phone,
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=user.is_active,
            is_verified=user.is_verified,
            created_at=user.created_at,
            updated_at=user.updated_at
        )


class UserFilter(BaseFilter):
    """Filter for querying users."""
    username: str | None = None
    email: str | None = None
    is_active: bool | None = None
    is_verified: bool | None = None
    created_after__gte: int | None = None
    created_after__lte: int | None = None
    created_before__gte: int | None = None
    created_before__lte: int | None = None

