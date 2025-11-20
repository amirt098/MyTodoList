# Standard library
import logging

# Third-party
from django.db import IntegrityError

# Internal - from other modules
# (none needed)

# Internal - from same module
from .models import User
from . import interface

logger = logging.getLogger(__name__)


class UserRepositoryService(interface.AbstractUserRepository):
    """Repository service for user data access."""
    
    def create(self, user_data: interface.UserCreateRequest) -> interface.UserDTO:
        logger.info(f"Creating user with username: {user_data.username}, user data: {user_data}")
        
        try:
            user = User()
            user.email = user_data.email
            user.set_password(user_data.password)
            user.phone = user_data.phone or ""
            user.first_name = user_data.first_name
            user.last_name = user_data.last_name
            user.is_active = user_data.is_active
            user.is_verified = user_data.is_verified
            user.created_at = user_data.created_at
            user.updated_at = user_data.updated_at
            user.save()
            
            result = interface.UserDTO.from_model(user)
            logger.info(f"User created successfully: {result.user_id}", extra={"output": result.model_dump()})
            return result
        except IntegrityError as e:
            logger.warning(f"Failed to create user - username already exists: {user_data.email}")
            raise interface.UserUsernameAlreadyExistsException(user_data.email)
    
    def get_by_id(self, user_id: int) -> interface.UserDTO | None:
        logger.info(f"Fetching user by id: {user_id}", extra={"input": {"user_id": user_id}})
        
        try:
            user = User.objects.get(id=user_id)
            result = interface.UserDTO.from_model(user)
            logger.info(f"User fetched successfully: {user_id}", extra={"output": result.model_dump()})
            return result
        except User.DoesNotExist:
            logger.info(f"User not found: {user_id}")
            return None
    
    def get_by_email(self, email: str) -> interface.UserDTO | None:
        logger.info(f"Fetching user by email: {email}", extra={"input": {"email": email}})
        
        try:
            user = User.objects.get(email=email)
            result = interface.UserDTO.from_model(user)
            logger.info(f'result: {result}')
            return result
        except User.DoesNotExist:
            logger.info(f"User not found by email: {email}")
            return None

    def get_by_username(self, username: str) -> interface.UserDTO | None:
        logger.info(f"Fetching user by username: {username}")

        try:
            user = User.objects.get(username=username)
            result = interface.UserDTO.from_model(user)
            logger.info(f'result: {result}')
            return result
        except User.DoesNotExist:
            logger.info(f"User not found by username: {username}")
            return None
    
    def get_users(self, filters: interface.UserFilter) -> list[interface.UserDTO]:
        logger.info(f"Filtering users", extra={"input": filters.model_dump()})
        

        filter_dict = filters.as_dict()

        queryset = User.objects.filter(**filter_dict)

        # Apply ordering
        queryset = queryset.order_by(filters.order_by)
        
        # Apply pagination
        if filters.offset is not None and filters.limit is not None:
            queryset = queryset[filters.offset:filters.offset + filters.limit]
        
        results = [interface.UserDTO.from_model(user) for user in queryset]
        logger.info(f"Found {len(results)} users matching filter", extra={"output": {"count": len(results)}})
        return results
    
    def update(self, user_id: int, user_data: interface.UserUpdateRequest) -> interface.UserDTO:
        logger.info(f"Updating user: {user_id}", extra={"input": {"user_id": user_id}})
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            logger.warning(f"User not found for update: {user_id}")
            raise interface.UserNotFoundByIdException(user_id)
        
        # Update fields if provided
        if user_data.username:
            user.username = user_data.username
        if user_data.email:
            user.email = user_data.email
        if user_data.password:
            user.set_password(user_data.password)
        if user_data.phone is not None:
            user.phone = user_data.phone
        if user_data.first_name is not None:
            user.first_name = user_data.first_name
        if user_data.last_name is not None:
            user.last_name = user_data.last_name
        if user_data.is_active is not None:
            user.is_active = user_data.is_active
        if user_data.is_verified is not None:
            user.is_verified = user_data.is_verified
        # Updated timestamp is provided by usecase layer
        if user_data.updated_at:
            user.updated_at = user_data.updated_at
        
        try:
            user.save()
        except IntegrityError as e:
            logger.warning(f"Failed to update user - email conflict: {user_id}")
            raise interface.UserEmailConflictException(user_data.email)
        
        result = interface.UserDTO.from_model(user)
        logger.info(f"User updated successfully: {user_id}", extra={"output": result.model_dump()})
        return result
    
    def delete(self, user_id: int) -> None:
        logger.info(f"Deleting user: {user_id}", extra={"input": {"user_id": user_id}})
        
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            logger.info(f"User deleted successfully: {user_id}")
        except User.DoesNotExist:
            logger.warning(f"User not found for deletion: {user_id}")
            raise interface.UserNotFoundByIdException(user_id)
    
    def verify_password(self, user_id: int, raw_password: str) -> bool:
        logger.info(f"Verifying password for user: {user_id}", extra={"input": {"user_id": user_id}})
        
        try:
            user = User.objects.get(id=user_id)
            is_valid = user.check_password(raw_password)
            logger.info(f"Password verification result: {is_valid}", extra={"output": {"is_valid": is_valid}})
            return is_valid
        except User.DoesNotExist:
            logger.warning(f"User not found for password verification: {user_id}")
            raise interface.UserNotFoundByIdException(user_id)

