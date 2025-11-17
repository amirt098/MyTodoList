# Standard library
from datetime import datetime
from typing import Optional

# Third-party
from pydantic import EmailStr, Field

# Internal - from other modules
from lib.base_models import BaseFilter

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


class UserDTO:
    """Data Transfer Object for User (Pydantic-like, used for responses)."""
    
    def __init__(
        self,
        user_id: int,
        email: str,
        phone: str,
        first_name: Optional[str],
        last_name: Optional[str],
        is_active: bool,
        is_verified: bool,
        created_at: datetime,
        updated_at: datetime
    ):
        self.user_id = user_id
        self.email = email
        self.phone = phone
        self.first_name = first_name
        self.last_name = last_name
        self.is_active = is_active
        self.is_verified = is_verified
        self.created_at = created_at
        self.updated_at = updated_at
    
    def model_dump(self) -> dict:
        """Convert to dictionary for logging/serialization."""
        return {
            "user_id": self.user_id,
            "email": self.email,
            "phone": self.phone,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
    
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
    
    email: Optional[str] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    created_after: Optional[datetime] = None
    created_before: Optional[datetime] = None

