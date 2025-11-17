# Standard library
from abc import ABC, abstractmethod

# Internal - from same interface module (direct import, no interface. prefix needed)
from .dataclasses import (
    RegisterUserRequest, RegisterUserResponse,
    LoginRequest, LoginResponse,
    PasswordRecoveryRequest, PasswordRecoveryResponse,
    UpdateProfileRequest, UpdateProfileResponse
)
from .exceptions import (
    UserRegistrationEmailExistsException,
    UserLoginInvalidCredentialsException,
    UserLoginInactiveAccountException,
    UserProfileNotFoundException
)


class AbstractUserManagementService(ABC):
    """Interface for user management operations."""
    
    @abstractmethod
    def register_user(self, request: RegisterUserRequest) -> RegisterUserResponse:
        """
        Register a new user in the system.
        
        Validates email availability, creates user account, and sends verification SMS.
        Groups: registration, user creation
        
        Args:
            request: Registration request with email, password, and phone
            
        Returns:
            RegisterUserResponse with user_id, email, and created_at
            
        Raises:
            UserRegistrationEmailExistsException: If email is already registered
        """
        pass
    
    @abstractmethod
    def login(self, request: LoginRequest) -> LoginResponse:
        """
        Authenticate user and return access token.
        
        Validates credentials and generates JWT token for session management.
        Groups: authentication, login
        
        Args:
            request: Login request with email and password
            
        Returns:
            LoginResponse with user_id and JWT token
            
        Raises:
            UserLoginInvalidCredentialsException: If credentials are invalid
            UserLoginInactiveAccountException: If user account is inactive
        """
        pass
    
    @abstractmethod
    def password_recovery(self, request: PasswordRecoveryRequest) -> PasswordRecoveryResponse:
        """
        Initiate password recovery process.
        
        Sends password recovery email with reset link. For security, always returns
        success message even if user doesn't exist.
        Groups: password recovery, authentication
        
        Args:
            request: Password recovery request with email
            
        Returns:
            PasswordRecoveryResponse with success status and message
        """
        pass
    
    @abstractmethod
    def update_profile(self, request: UpdateProfileRequest) -> UpdateProfileResponse:
        """
        Update user profile information.
        
        Updates user's profile fields (first_name, last_name, phone).
        Groups: profile management, user updates
        
        Args:
            request: Update request with user_id and fields to update
            
        Returns:
            UpdateProfileResponse with updated user information
            
        Raises:
            UserProfileNotFoundException: If user doesn't exist
        """
        pass

