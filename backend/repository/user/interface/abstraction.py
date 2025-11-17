# Standard library
from abc import ABC, abstractmethod

# Internal - from same interface module (direct import, no interface. prefix needed)
from .dataclasses import UserData, UserDTO, UserFilter


class AbstractUserRepository(ABC):
    """Interface for user repository operations."""
    
    @abstractmethod
    def create(self, user_data: UserData) -> UserDTO:
        """
        Create a new user in the database.
        
        Args:
            user_data: UserData object with user information (including created_at and updated_at timestamps)
            
        Returns:
            UserDTO with created user information
            
        Raises:
            UserEmailAlreadyExistsException: If email already exists
        """
        pass
    
    @abstractmethod
    def get_by_id(self, user_id: int) -> UserDTO | None:
        """
        Get user by ID.
        
        Args:
            user_id: User ID to fetch
            
        Returns:
            UserDTO if found, None otherwise
        """
        pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> UserDTO | None:
        """
        Get user by email.
        
        Args:
            email: User email to fetch
            
        Returns:
            UserDTO if found, None otherwise
        """
        pass
    
    @abstractmethod
    def get_users(self, filters: UserFilter) -> list[UserDTO]:
        """
        Get users with filtering.
        
        General method for querying users with various filters.
        
        Args:
            filters: UserFilter Pydantic object extending BaseFilter from lib
            
        Returns:
            List of UserDTO matching the filters
        """
        pass
    
    @abstractmethod
    def update(self, user_id: int, user_data: UserData) -> UserDTO:
        """
        Update an existing user.
        
        Args:
            user_id: User ID to update
            user_data: UserData with fields to update (only provided fields will be updated, including updated_at timestamp)
            
        Returns:
            UserDTO with updated user information
            
        Raises:
            UserNotFoundByIdException: If user doesn't exist
            UserEmailConflictException: If email is already in use
        """
        pass
    
    @abstractmethod
    def delete(self, user_id: int) -> None:
        """
        Delete a user.
        
        Args:
            user_id: User ID to delete
            
        Raises:
            UserNotFoundByIdException: If user doesn't exist
        """
        pass
    
    @abstractmethod
    def verify_password(self, user_id: int, raw_password: str) -> bool:
        """
        Verify if provided password matches user's password.
        
        Args:
            user_id: User ID to verify password for
            raw_password: Plain text password to verify
            
        Returns:
            True if password matches, False otherwise
            
        Raises:
            UserNotFoundByIdException: If user doesn't exist
        """
        pass

