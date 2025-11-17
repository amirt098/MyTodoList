# Code Examples

[← Back to Architecture Index](./ARCHITECTURE.md)

---

This document contains complete code examples for UseCase and Repository modules following the architecture patterns.

## Example: UseCase Module (Consolidated Service)

### Interface Definition

```python
# usecase/user_management/interface/abstraction.py
# Standard library
from abc import ABC, abstractmethod

# Internal - from same interface module (direct import, no interface. prefix needed)
from .dataclasses import (
    RegisterUserRequest, RegisterUserResponse,
    LoginRequest, LoginResponse,
    PasswordRecoveryRequest, PasswordRecoveryResponse,
    UpdateProfileRequest, UpdateProfileResponse
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
            BadRequestRootException: If email is already registered or invalid
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
            UnauthorizedRootException: If credentials are invalid
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
            NotFoundRootException: If user doesn't exist
        """
        pass
```

### Service Implementation

```python
# usecase/user_management/service.py
# Standard library
import logging

# Third-party
# (none in this example)

# Internal - from other modules
from lib.exceptions import BadRequestRootException, UnauthorizedRootException, NotFoundRootException
from repository.user import interface as user_repository_interface
from externals.sms import interface as sms_interface
from externals.email import interface as email_interface
from usecase.common_usecase.policies.registration import RegistrationPolicy

# Internal - from same module
from . import interface

logger = logging.getLogger(__name__)

class UserManagementService(interface.AbstractUserManagementService):
    def __init__(
        self,
        user_repo: user_repository_interface.AbstractUserRepository,      # ✅ Abstract class type
        sms_client: sms_interface.AbstractSMSService,          # ✅ Abstract class type
        email_client: email_interface.AbstractEmailService,      # ✅ Abstract class type
        policy: RegistrationPolicy        # Policy class
    ):
        self.user_repo = user_repo
        self.sms_client = sms_client
        self.email_client = email_client
        self.policy = policy
    
    def register_user(self, request: interface.RegisterUserRequest) -> interface.RegisterUserResponse:
        logger.info(f"Registering user with email: {request.email}", extra={"input": request.model_dump()})
        
        if not self.policy.can_register(request.email):
            raise BadRequestRootException("Cannot register with this email")
        
        user = self.user_repo.create(request.to_user_data())
        self.sms_client.send_verification(user.phone)
        
        response = RegisterUserResponse.from_user(user)
        logger.info(f"User registered successfully: {response.user_id}", extra={"output": response.model_dump()})
        return response
    
    def login(self, request: LoginRequest) -> LoginResponse:
        logger.info(f"Login attempt for email: {request.email}", extra={"input": request.model_dump()})
        
        user = self.user_repo.get_by_email(request.email)
        if not user or not user.verify_password(request.password):
            raise UnauthorizedRootException("Invalid credentials")
        
        token = self._generate_token(user)
        response = interface.LoginResponse(user_id=user.id, token=token)
        
        logger.info(f"User logged in successfully: {user.id}", extra={"output": response.model_dump()})
        return response
    
    def password_recovery(self, request: PasswordRecoveryRequest) -> PasswordRecoveryResponse:
        logger.info(f"Password recovery requested for email: {request.email}", extra={"input": request.model_dump()})
        
        user = self.user_repo.get_by_email(request.email)
        if not user:
            response = interface.PasswordRecoveryResponse(success=True, message="If email exists, recovery link sent")
            logger.info(f"Password recovery response sent (user not found): {request.email}", extra={"output": response.model_dump()})
            return response
        
        recovery_token = self._generate_recovery_token(user)
        self.email_client.send_password_recovery(user.email, recovery_token)
        
        response = interface.PasswordRecoveryResponse(success=True, message="Recovery link sent")
        logger.info(f"Password recovery email sent to: {request.email}", extra={"output": response.model_dump()})
        return response
    
    def update_profile(self, request: UpdateProfileRequest) -> UpdateProfileResponse:
        logger.info(f"Updating profile for user: {request.user_id}", extra={"input": request.model_dump()})
        
        user = self.user_repo.get_by_id(request.user_id)
        if not user:
            raise NotFoundRootException("User not found")
        
        updated_user = self.user_repo.update(request.user_id, request.to_update_data())
        response = interface.UpdateProfileResponse.from_user(updated_user)
        
        logger.info(f"Profile updated successfully for user: {request.user_id}", extra={"output": response.model_dump()})
        return response
    
    def _generate_token(self, user):
        # Token generation logic
        pass
    
    def _generate_recovery_token(self, user):
        # Recovery token generation logic
        pass
```

### DTOs (Pydantic Models)

```python
# usecase/user_management/interface/dataclasses.py
# Standard library
from datetime import datetime

# Third-party
from pydantic import BaseModel, EmailStr, Field

# Internal - from other modules
from lib.base_models import BaseRequest, BaseResponse, BaseFilter

# All DTOs extend from base Pydantic models in lib
class RegisterUserRequest(BaseRequest):
    email: EmailStr
    password: str = Field(..., min_length=8)
    phone: str

class RegisterUserResponse(BaseResponse):
    user_id: int
    email: str
    created_at: datetime

class LoginRequest(BaseRequest):
    email: EmailStr
    password: str

class LoginResponse(BaseResponse):
    user_id: int
    token: str

class PasswordRecoveryRequest(BaseRequest):
    email: EmailStr

class PasswordRecoveryResponse(BaseResponse):
    success: bool
    message: str

class UpdateProfileRequest(BaseRequest):
    user_id: int
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None

class UpdateProfileResponse(BaseResponse):
    user_id: int
    email: str
    first_name: str | None
    last_name: str | None
    updated_at: datetime

# Filter objects extend BaseFilter from lib
class UserFilter(BaseFilter):
    email: str | None = None
    is_active: bool | None = None
    created_after: datetime | None = None
    created_before: datetime | None = None
```

---

## Example: Todo Management Service

### Interface Definition

```python
# usecase/todo_management/interface/abstraction.py
# Standard library
from abc import ABC, abstractmethod

# Internal - from same interface module (direct import, no interface. prefix needed)
from .dataclasses import (
    CreateTodoRequest, CreateTodoResponse,
    UpdateTodoRequest, UpdateTodoResponse,
    TodoFilter, TodoDTO
)

class AbstractTodoManagementService(ABC):
    """Interface for todo management operations."""
    
    @abstractmethod
    def create_todo(self, request: CreateTodoRequest) -> CreateTodoResponse:
        """
        Create a new todo.
        
        Args:
            request: Create todo request with title, description, etc.
            
        Returns:
            CreateTodoResponse with created todo information
        """
        pass
    
    @abstractmethod
    def get_todo_by_id(self, todo_id: int) -> TodoDTO:
        """
        Get a single todo by ID.
        
        This method is provided separately as it's used frequently throughout the system.
        
        Args:
            todo_id: Todo ID to fetch
            
        Returns:
            TodoDTO with todo information
            
        Raises:
            NotFoundRootException: If todo doesn't exist
        """
        pass
    
    @abstractmethod
    def get_todos(self, filters: TodoFilter) -> list[TodoDTO]:
        """
        Get todos with filtering.
        
        General method for querying todos with various filters. This is the primary
        method for retrieving multiple todos with complex filtering criteria.
        
        Args:
            filters: TodoFilter Pydantic object extending BaseFilter from lib
            
        Returns:
            List of TodoDTO matching the filters
        """
        pass
    
    @abstractmethod
    def update_todo(self, request: UpdateTodoRequest) -> UpdateTodoResponse:
        """
        Update an existing todo.
        
        Args:
            request: Update request with todo_id and fields to update
            
        Returns:
            UpdateTodoResponse with updated todo information
            
        Raises:
            NotFoundRootException: If todo doesn't exist
        """
        pass
    
    @abstractmethod
    def delete_todo(self, todo_id: int) -> None:
        """
        Delete a todo.
        
        Args:
            todo_id: Todo ID to delete
            
        Raises:
            NotFoundRootException: If todo doesn't exist
        """
        pass
```

### Service Implementation

```python
# usecase/todo_management/service.py
# Standard library
import logging

# Third-party
# (none in this example)

# Internal - from other modules
from lib.exceptions import NotFoundRootException, BadRequestRootException
from repository.todo import interface as todo_repository_interface

# Internal - from same module
from . import interface

logger = logging.getLogger(__name__)

class TodoManagementService(interface.AbstractTodoManagementService):
    def __init__(self, todo_repo: todo_repository_interface.AbstractTodoRepository):  # ✅ Abstract class type
        self.todo_repo = todo_repo
    
    def create_todo(self, request: interface.CreateTodoRequest) -> interface.CreateTodoResponse:
        logger.info(f"Creating todo: {request.title}", extra={"input": request.model_dump()})
        
        todo_data = request.to_todo_data()
        todo = self.todo_repo.create(todo_data)
        
        response = CreateTodoResponse.from_todo(todo)
        logger.info(f"Todo created successfully: {response.todo_id}", extra={"output": response.model_dump()})
        return response
    
    def get_todo_by_id(self, todo_id: int) -> interface.TodoDTO:
        logger.info(f"Fetching todo by id: {todo_id}", extra={"input": {"todo_id": todo_id}})
        
        todo = self.todo_repo.get_by_id(todo_id)
        if not todo:
            raise NotFoundRootException(f"Todo with id {todo_id} not found")
        
        logger.info(f"Todo fetched successfully: {todo_id}", extra={"output": todo.model_dump()})
        return todo
    
    def get_todos(self, filters: interface.TodoFilter) -> list[interface.TodoDTO]:
        logger.info(f"Getting todos with filters", extra={"input": filters.model_dump()})
        
        todos = self.todo_repo.get_todos(filters)
        
        logger.info(f"Found {len(todos)} todos matching filters", extra={"output": {"count": len(todos)}})
        return todos
    
    def update_todo(self, request: interface.UpdateTodoRequest) -> interface.UpdateTodoResponse:
        logger.info(f"Updating todo: {request.todo_id}", extra={"input": request.model_dump()})
        
        # Verify todo exists
        self.get_todo_by_id(request.todo_id)
        
        update_data = request.to_update_data()
        updated_todo = self.todo_repo.update(request.todo_id, update_data)
        
        response = interface.UpdateTodoResponse.from_todo(updated_todo)
        logger.info(f"Todo updated successfully: {request.todo_id}", extra={"output": response.model_dump()})
        return response
    
    def delete_todo(self, todo_id: int) -> None:
        logger.info(f"Deleting todo: {todo_id}", extra={"input": {"todo_id": todo_id}})
        
        # Verify todo exists
        self.get_todo_by_id(todo_id)
        
        self.todo_repo.delete(todo_id)
        
        logger.info(f"Todo deleted successfully: {todo_id}")
```

---

## Example: Repository Module

### Models

```python
# repository/user/models.py
from django.db import models

class User(models.Model):
    """User model - no cross-module relationships."""
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'
```

```python
# repository/todo/models.py
from django.db import models

class Todo(models.Model):
    """Todo model - stores user_id, not ForeignKey to User."""
    user_id = models.IntegerField()  # ✅ Store ID, not ForeignKey
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    priority = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    category = models.CharField(max_length=100, blank=True)
    project_id = models.IntegerField(null=True, blank=True)  # ✅ Store ID, not ForeignKey
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'todos'
        # Note: Relationships to User and Project are resolved via repository services
```

### Repository Interface

```python
# repository/user/interface/abstraction.py
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
            user_data: User data to create
            
        Returns:
            UserDTO with created user information
            
        Raises:
            BadRequestRootException: If user data is invalid
        """
        pass
    
    @abstractmethod
    def get_by_id(self, user_id: int) -> UserDTO:
        """
        Get user by ID.
        
        Args:
            user_id: User ID to fetch
            
        Returns:
            UserDTO with user information
            
        Raises:
            NotFoundRootException: If user doesn't exist
        """
        pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> UserDTO | None:
        """
        Get user by email address.
        
        Args:
            email: Email address to search for
            
        Returns:
            UserDTO if found, None otherwise
        """
        pass
    
    @abstractmethod
    def update(self, user_id: int, update_data: dict) -> UserDTO:
        """
        Update user information.
        
        Args:
            user_id: User ID to update
            update_data: Dictionary of fields to update
            
        Returns:
            UserDTO with updated user information
            
        Raises:
            NotFoundRootException: If user doesn't exist
        """
        pass
    
    @abstractmethod
    def get_users(self, filters: interface.UserFilter) -> list[interface.UserDTO]:
        """
        Get users with filtering.
        
        General method for querying users with various filters.
        
        Args:
            filters: UserFilter Pydantic object extending BaseFilter
            
        Returns:
            List of UserDTO matching the filters
        """
        pass
```

### Repository Implementation

```python
# repository/user/service.py
# Standard library
import logging

# Third-party
from django.db import models

# Internal - from other modules
from lib.exceptions import NotFoundRootException, BadRequestRootException

# Internal - from same module
from repository.user.models import User
from . import interface

logger = logging.getLogger(__name__)

class UserRepositoryService(interface.AbstractUserRepository):
    def create(self, user_data: interface.UserData) -> interface.UserDTO:
        logger.info(f"Creating user with email: {user_data.email}", extra={"input": user_data.model_dump()})
        
        user = User.objects.create(
            email=user_data.email,
            password=user_data.password,
            phone=user_data.phone
        )
        
        result = UserDTO.from_model(user)
        logger.info(f"User created successfully: {result.user_id}", extra={"output": result.model_dump()})
        return result
    
    def get_by_id(self, user_id: int) -> interface.UserDTO:
        logger.info(f"Fetching user by id: {user_id}", extra={"input": {"user_id": user_id}})
        
        try:
            user = User.objects.get(id=user_id)
            result = interface.UserDTO.from_model(user)
            logger.info(f"User fetched successfully: {user_id}", extra={"output": result.model_dump()})
            return result
        except User.DoesNotExist:
            logger.warning(f"User not found: {user_id}")
            raise NotFoundRootException(f"User with id {user_id} not found")
    
    def get_by_email(self, email: str) -> interface.UserDTO | None:
        logger.info(f"Fetching user by email: {email}", extra={"input": {"email": email}})
        
        try:
            user = User.objects.get(email=email)
            result = interface.UserDTO.from_model(user)
            logger.info(f"User fetched by email: {email}", extra={"output": result.model_dump()})
            return result
        except User.DoesNotExist:
            logger.info(f"User not found by email: {email}")
            return None
    
    def update(self, user_id: int, update_data: dict) -> interface.UserDTO:
        logger.info(f"Updating user: {user_id}", extra={"input": {"user_id": user_id, "update_data": update_data}})
        
        user = User.objects.get(id=user_id)
        for key, value in update_data.items():
            setattr(user, key, value)
        user.save()
        
        result = UserDTO.from_model(user)
        logger.info(f"User updated successfully: {user_id}", extra={"output": result.model_dump()})
        return result
    
    def get_users(self, filters: interface.UserFilter) -> list[interface.UserDTO]:
        logger.info(f"Filtering users with filter: {filters.model_dump()}", extra={"input": filters.model_dump()})
        
        queryset = User.objects.all()
        
        if filters.email:
            queryset = queryset.filter(email=filters.email)
        if filters.is_active is not None:
            queryset = queryset.filter(is_active=filters.is_active)
        if filters.created_after:
            queryset = queryset.filter(created_at__gte=filters.created_after)
        if filters.created_before:
            queryset = queryset.filter(created_at__lte=filters.created_before)
        
        results = [UserDTO.from_model(user) for user in queryset]
        logger.info(f"Found {len(results)} users matching filter", extra={"output": {"count": len(results)}})
        return results
```

---

## Example: Filter Usage Pattern

This example demonstrates how to create and use filters with pagination, ordering, and field filtering.

### Filter DTO Definition

```python
# repository/claim/interface/dataclasses.py
# Standard library
from typing import List
from enum import Enum

# Third-party
# (none)

# Internal - from other modules
from lib.base_models import BaseFilter
from lib.validators import UIDField, PositiveIntField, PaymentCardNumberField

# Enum for status
class ClaimStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class ClaimFilter(BaseFilter):
    """Filter for querying claims with various criteria."""
    user_uid: UIDField | None = None
    status__in: List[ClaimStatus] | None = None
    claiming_timestamp__gte: PositiveIntField | None = None
    claiming_timestamp__lte: PositiveIntField | None = None
    created_at__gte: PositiveIntField | None = None
    created_at__lte: PositiveIntField | None = None
    source_card_number_first_6_digits: str | None = None
    source_card_number_last_4_digits: str | None = None
    destination_card_number: PaymentCardNumberField | None = None
```

### Using Filter in Repository Service

```python
# repository/claim/service.py
# Standard library
import logging

# Third-party
# (none)

# Internal - from other modules
# (none)

# Internal - from same module
from repository.claim.models import Claim
from . import interface

logger = logging.getLogger(__name__)

class ClaimRepositoryService(interface.AbstractClaimRepository):
    def get_claims(self, filters: interface.ClaimFilter) -> interface.ClaimResult:
        logger.info(f"Getting claims with filters", extra={"input": filters.model_dump()})
        
        # Use as_dict() to get only filter fields (excludes limit, offset, order_by)
        filter_dict = filters.as_dict()
        
        # Apply filters to queryset
        claims = Claim.objects.filter(**filter_dict).order_by(filters.order_by)
        
        # Get total count before pagination
        count = claims.count()
        
        # Apply pagination
        claims = claims[filters.offset: filters.offset + filters.limit]
        
        # Convert to DTOs
        result = interface.ClaimResult(
            count=count,
            results=[self._convert_claim_object_to_dataclass(claim=claim) for claim in claims]
        )
        
        logger.info(f"Found {count} claims matching filters", extra={"output": {"count": count}})
        return result
    
    def _convert_claim_object_to_dataclass(self, claim: Claim) -> interface.ClaimDTO:
        """Convert Django model to DTO."""
        return interface.ClaimDTO.from_model(claim)
```

### Filter Usage Notes

1. **BaseFilter provides:**
   - `order_by`: Default ordering (default: `'-id'`)
   - `limit`: Number of results (default: 20)
   - `offset`: Pagination offset (default: 0)
   - `as_dict()`: Returns only filter fields, excluding pagination fields

2. **Filter field naming:**
   - Use `__gte`, `__lte`, `__in` suffixes for Django ORM query operations
   - Example: `created_at__gte`, `status__in`

3. **Pagination pattern:**
   - Get total count before applying limit/offset
   - Apply pagination after filtering and ordering
   - Return both results and total count

4. **Validation:**
   - BaseFilter validates limit > 0 and offset >= 0
   - Sets defaults if limit/offset are None

---

[← Back to Architecture Index](./ARCHITECTURE.md) | [Next: Principles →](./ARCHITECTURE_PRINCIPLES.md)

