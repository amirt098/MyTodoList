# Dependency Injection (Bootstrapper)

[← Back to Architecture Index](./ARCHITECTURE.md)

---

A central bootstrapper constructs the system and manages all dependencies.

## Bootstrapper Structure

```python
# runner/bootstrap.py
# Standard library
# (none needed)

# Third-party
# (none needed)

# Internal - from other modules
from repository.user.service import UserRepositoryService
from repository.todo.service import TodoRepositoryService
from externals.sms.service import SMSService
from externals.email.service import EmailService
from externals.payment_gateway.service import PaymentGatewayService
from clients.redis.service import RedisService
from usecase.common_usecase.policies.registration import RegistrationPolicy
from usecase.common_usecase.validators.auth import AuthValidator
from usecase.user_management.service import UserManagementService
from usecase.todo_management.service import TodoManagementService

class Bootstrapper:
    def __init__(self):
        # Repositories (concrete implementations)
        self.user_repo = UserRepositoryService()
        self.todo_repo = TodoRepositoryService()
        
        # Externals (concrete implementations)
        self.sms_client = SMSService()
        self.email_client = EmailService()
        self.payment_gateway = PaymentGatewayService()
        self.redis_client = RedisService()
        
        # Common UseCase Components
        self.registration_policy = RegistrationPolicy()
        self.auth_validator = AuthValidator()
        
        # UseCases (injecting abstract types, but using concrete instances)
        self.user_management_service = UserManagementService(
            user_repo=self.user_repo,        # AbstractUserRepository type expected
            sms_client=self.sms_client,      # AbstractSMSService type expected
            email_client=self.email_client,  # AbstractEmailService type expected
            policy=self.registration_policy
        )
        
        self.todo_management_service = TodoManagementService(
            todo_repo=self.todo_repo,        # AbstractTodoRepository type expected
            user_repo=self.user_repo         # AbstractUserRepository type expected
        )
    
    def get_user_management_service(self) -> UserManagementService:
        return self.user_management_service
    
    def get_todo_management_service(self) -> TodoManagementService:
        return self.todo_management_service
```

## Usage in Views

```python
# presentation/rest/user_views.py
# Standard library
# (none needed)

# Third-party
from django.http import JsonResponse

# Internal - from other modules
from runner.bootstrap import bootstrapper
from usecase.user_management import interface

def register_user_view(request):
    service = bootstrapper.get_user_management_service()
    # service is UserManagementService, but we use it through interface.AbstractUserManagementService
    # Use service with interface types:
    # request = interface.RegisterUserRequest(...)
    # response = service.register_user(request)
```

---

[← Back to Architecture Index](./ARCHITECTURE.md) | [Next: Directory Structure →](./ARCHITECTURE_STRUCTURE.md)

