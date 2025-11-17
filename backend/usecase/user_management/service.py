# Standard library
import logging
import secrets
import hashlib
from datetime import datetime, timezone

# Third-party
# (none needed)

# Internal - from other modules
from repository.user import interface as user_repository_interface
from utils.date_utils import interface as date_utils_interface
from utils.date_utils import datetime_service

# Internal - from same module
from . import interface

logger = logging.getLogger(__name__)


class UserManagementService(interface.AbstractUserManagementService):
    """Service for managing user operations."""
    
    def __init__(
        self,
        user_repo: user_repository_interface.AbstractUserRepository
    ):
        self.user_repo = user_repo
    
    def register_user(self, request: interface.RegisterUserRequest) -> interface.RegisterUserResponse:
        logger.info(f"Registering user with email: {request.email}", extra={"input": request.model_dump()})
        
        # Check if user already exists
        existing_user = self.user_repo.get_by_email(request.email)
        if existing_user:
            logger.warning(f"Registration failed - email already exists: {request.email}")
            raise interface.UserRegistrationEmailExistsException(request.email)
        
        # Calculate timestamps in usecase layer
        now_dto = datetime_service.now()
        created_at = datetime.fromtimestamp(now_dto.timestamp_ms / 1000, tz=timezone.utc)
        updated_at = datetime.fromtimestamp(now_dto.timestamp_ms / 1000, tz=timezone.utc)
        
        # Create user with timestamps
        user_data = request.to_user_data(created_at, updated_at)
        user_dto = self.user_repo.create(user_data)
        
        response = interface.RegisterUserResponse(
            user_id=user_dto.user_id,
            email=user_dto.email,
            created_at=user_dto.created_at
        )
        
        logger.info(f"User registered successfully: {response.user_id}", extra={"output": response.model_dump()})
        return response
    
    def login(self, request: interface.LoginRequest) -> interface.LoginResponse:
        logger.info(f"Login attempt for email: {request.email}", extra={"input": {"email": request.email}})
        
        # Get user by email
        user_dto = self.user_repo.get_by_email(request.email)
        if not user_dto:
            logger.warning(f"Login failed - user not found: {request.email}")
            raise interface.UserLoginInvalidCredentialsException()
        
        # Verify password
        is_valid = self.user_repo.verify_password(user_dto.user_id, request.password)
        if not is_valid:
            logger.warning(f"Login failed - invalid password for user: {user_dto.user_id}")
            raise interface.UserLoginInvalidCredentialsException()
        
        # Check if user is active
        if not user_dto.is_active:
            logger.warning(f"Login failed - user inactive: {user_dto.user_id}")
            raise interface.UserLoginInactiveAccountException()
        
        # Generate token (simple implementation - should use JWT in production)
        token = self._generate_token(user_dto.user_id, user_dto.email)
        
        response = interface.LoginResponse(
            user_id=user_dto.user_id,
            token=token,
            email=user_dto.email
        )
        
        logger.info(f"User logged in successfully: {user_dto.user_id}", extra={"output": {"user_id": user_dto.user_id}})
        return response
    
    def password_recovery(self, request: interface.PasswordRecoveryRequest) -> interface.PasswordRecoveryResponse:
        logger.info(f"Password recovery requested for email: {request.email}", extra={"input": {"email": request.email}})
        
        # Get user by email
        user_dto = self.user_repo.get_by_email(request.email)
        if not user_dto:
            # For security, always return success even if user doesn't exist
            response = interface.PasswordRecoveryResponse(
                success=True,
                message="If the email exists, a password recovery link has been sent"
            )
            logger.info(f"Password recovery response sent (user not found): {request.email}", extra={"output": response.model_dump()})
            return response
        
        # TODO: Send password recovery email
        # For now, just return success
        response = interface.PasswordRecoveryResponse(
            success=True,
            message="Password recovery link has been sent to your email"
        )
        
        logger.info(f"Password recovery email sent to: {request.email}", extra={"output": response.model_dump()})
        return response
    
    def update_profile(self, request: interface.UpdateProfileRequest) -> interface.UpdateProfileResponse:
        logger.info(f"Updating profile for user: {request.user_id}", extra={"input": request.model_dump()})
        
        # Verify user exists
        user_dto = self.user_repo.get_by_id(request.user_id)
        if not user_dto:
            logger.warning(f"Profile update failed - user not found: {request.user_id}")
            raise interface.UserProfileNotFoundException(request.user_id)
        
        # Calculate updated timestamp in usecase layer
        now_dto = datetime_service.now()
        updated_at = datetime.fromtimestamp(now_dto.timestamp_ms / 1000, tz=timezone.utc)
        
        # Update user with timestamp
        user_data = request.to_user_data(updated_at)
        updated_user_dto = self.user_repo.update(request.user_id, user_data)
        
        response = interface.UpdateProfileResponse(
            user_id=updated_user_dto.user_id,
            email=updated_user_dto.email,
            first_name=updated_user_dto.first_name,
            last_name=updated_user_dto.last_name,
            phone=updated_user_dto.phone,
            updated_at=updated_user_dto.updated_at
        )
        
        logger.info(f"Profile updated successfully for user: {request.user_id}", extra={"output": response.model_dump()})
        return response
    
    def _generate_token(self, user_id: int, email: str) -> str:
        """
        Generate a simple token for authentication.
        TODO: Replace with proper JWT implementation.
        """
        # Simple token generation - should use JWT in production
        token_data = f"{user_id}:{email}:{secrets.token_urlsafe(32)}"
        token_hash = hashlib.sha256(token_data.encode()).hexdigest()
        return token_hash

