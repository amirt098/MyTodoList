# Standard library
import logging
import secrets
import hashlib

# Third-party
# (none needed)

# Internal - from other modules
from repository.user import interface as user_repository_interface
from utils.date_utils import interface as date_utils_interface

# Internal - from same module
from . import interface

logger = logging.getLogger(__name__)


class UserManagementService(interface.AbstractUserManagementService):
    """Service for managing user operations."""
    
    def __init__(
        self,
        user_repo: user_repository_interface.AbstractUserRepository,
        date_time_service: date_utils_interface.AbstractDateTimeService,
    ):
        self.user_repo = user_repo
        self.date_time_service = date_time_service
    
    def register_user(self, request: interface.RegisterUserRequest) -> interface.RegisterUserResponse:
        logger.info(f"Registering user with username: {request.username}", extra={"input": request.model_dump()})
        
        # Check if user already exists by email
        if request.email:
            existing_user = self.user_repo.get_by_email(request.email)
            if existing_user:
                logger.warning(f"Registration failed - email already exists: {request.email}")
                raise interface.UserRegistrationEmailExistsException(request.email)
        
        # Check if username already exists
        existing_user = self.user_repo.get_by_username(request.username)
        if existing_user:
            logger.warning(f"Registration failed - username already exists: {request.username}")
            raise interface.UserRegistrationUsernameExistsException(request.username)
        
        now_dto = self.date_time_service.now()
        
        # Create UserCreateRequest with timestamps
        user_create_request = user_repository_interface.UserCreateRequest(
            email=request.email,
            username=request.username,
            password=request.password,
            phone=request.phone,
            first_name=request.first_name,
            last_name=request.last_name,
            is_active=request.is_active,
            is_verified=request.is_verified,
            created_at=now_dto,
            updated_at=now_dto
        )
        
        user_dto = self.user_repo.create(user_create_request)
        
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
        now_dto = self.date_time_service.now()

        # Create UserUpdateRequest with only provided fields
        user_update_request = user_repository_interface.UserUpdateRequest(
            email=None,  # Not updating email
            username=None,  # Not updating username
            password=None,  # Not updating password
            phone=request.phone,
            first_name=request.first_name,
            last_name=request.last_name,
            is_active=None,  # Not updating
            is_verified=None,  # Not updating
            created_at=None,  # Not updating
            updated_at=now_dto
        )
        
        updated_user_dto = self.user_repo.update(request.user_id, user_update_request)
        
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

