# Standard library
# (none needed)

# Third-party
# (none needed)

# Internal - from other modules
from repository.user.service import UserRepositoryService
from usecase.user_management.service import UserManagementService
# Note: Additional imports will be added as we create more services
# from repository.todo.service import TodoRepositoryService
# from externals.sms.service import SMSService
# from externals.email.service import EmailService
# from usecase.todo_management.service import TodoManagementService


class Bootstrapper:
    """
    Central bootstrapper for dependency injection.
    Constructs all services and wires dependencies.
    """
    
    def __init__(self):
        # Repositories (concrete implementations)
        self.user_repo = UserRepositoryService()
        # self.todo_repo = TodoRepositoryService()
        
        # Externals (concrete implementations)
        # self.sms_client = SMSService()
        # self.email_client = EmailService()
        
        # Common UseCase Components
        # self.registration_policy = RegistrationPolicy()
        # self.auth_validator = AuthValidator()
        
        # UseCases (injecting abstract types, but using concrete instances)
        self.user_management_service = UserManagementService(
            user_repo=self.user_repo        # AbstractUserRepository type expected
        )
        # 
        # self.todo_management_service = TodoManagementService(
        #     todo_repo=self.todo_repo,        # AbstractTodoRepository type expected
        #     user_repo=self.user_repo         # AbstractUserRepository type expected
        # )
    
    def get_user_management_service(self) -> UserManagementService:
        return self.user_management_service
    
    # def get_todo_management_service(self) -> TodoManagementService:
    #     return self.todo_management_service


# Global bootstrapper instance
bootstrapper = Bootstrapper()

