# Standard library
# (none needed)

# Third-party
# (none needed)

# Internal - from other modules
from repository.user.service import UserRepositoryService
from repository.todo.service import TodoRepositoryService
from repository.project.service import ProjectRepositoryService
from repository.kanban.service import KanbanRepositoryService
from repository.subtask.service import SubtaskRepositoryService
from repository.saved_filter.service import SavedFilterRepositoryService
from repository.reminder.service import ReminderRepositoryService
from usecase.user_management.service import UserManagementService
from usecase.todo_management.service import TodoManagementService
from usecase.project_management.service import ProjectManagementService
from usecase.kanban_management.service import KanbanManagementService
from usecase.subtask_management.service import SubtaskManagementService
from usecase.todo_dependency_management.service import TodoDependencyManagementService
from usecase.filter_management.service import FilterManagementService
from usecase.bulk_operations.service import BulkOperationsService
from usecase.export_management.service import ExportManagementService
from usecase.reminder_management.service import ReminderManagementService
from usecase.smart_todo_management.service import SmartTodoManagementService
from externals.email.service import EmailService
from externals.sms.service import SMSService
from externals.llm.service import LLMService
from utils.date_utils.service import DateTimeService


class Bootstrapper:
    """
    Central bootstrapper for dependency injection.
    Constructs all services and wires dependencies.
    """
    
    def __init__(self):
        # Repositories (concrete implementations)
        self.user_repo = UserRepositoryService()
        self.todo_repo = TodoRepositoryService()
        self.project_repo = ProjectRepositoryService()
        self.kanban_repo = KanbanRepositoryService()
        self.subtask_repo = SubtaskRepositoryService()
        self.saved_filter_repo = SavedFilterRepositoryService()
        self.reminder_repo = ReminderRepositoryService()
        
        # Externals (concrete implementations)
        self.sms_service = SMSService()
        self.email_service = EmailService()
        self.llm_service = LLMService()
        
        # Utils (shared services)
        self.date_time_service = DateTimeService()
        
        # Common UseCase Components
        # self.registration_policy = RegistrationPolicy()
        # self.auth_validator = AuthValidator()
        
        # UseCases (injecting abstract types, but using concrete instances)
        self.user_management_service = UserManagementService(
            user_repo=self.user_repo,        # AbstractUserRepository type expected
            date_time_service=self.date_time_service  # AbstractDateTimeService type expected
        )
        
        self.todo_management_service = TodoManagementService(
            todo_repo=self.todo_repo,        # AbstractTodoRepository type expected
            date_time_service=self.date_time_service,  # AbstractDateTimeService type expected
            subtask_repo=self.subtask_repo  # AbstractSubtaskRepository type expected (optional)
        )
        
        self.project_management_service = ProjectManagementService(
            project_repo=self.project_repo,  # AbstractProjectRepository type expected
            date_time_service=self.date_time_service  # AbstractDateTimeService type expected
        )
        
        self.kanban_management_service = KanbanManagementService(
            kanban_repo=self.kanban_repo,  # AbstractKanbanRepository type expected
            todo_repo=self.todo_repo,  # AbstractTodoRepository type expected
            project_repo=self.project_repo,  # AbstractProjectRepository type expected
            todo_management_service=self.todo_management_service,  # AbstractTodoManagementService type expected
            date_time_service=self.date_time_service  # AbstractDateTimeService type expected
        )
        
        self.subtask_management_service = SubtaskManagementService(
            subtask_repo=self.subtask_repo,  # AbstractSubtaskRepository type expected
            todo_repo=self.todo_repo,  # AbstractTodoRepository type expected
            date_time_service=self.date_time_service  # AbstractDateTimeService type expected
        )
        
        self.todo_dependency_management_service = TodoDependencyManagementService(
            todo_repo=self.todo_repo,  # AbstractTodoRepository type expected
            todo_management_service=self.todo_management_service,  # AbstractTodoManagementService type expected
            date_time_service=self.date_time_service  # AbstractDateTimeService type expected
        )
        
        self.filter_management_service = FilterManagementService(
            saved_filter_repo=self.saved_filter_repo,  # AbstractSavedFilterRepository type expected
            date_time_service=self.date_time_service  # AbstractDateTimeService type expected
        )
        
        self.bulk_operations_service = BulkOperationsService(
            todo_repo=self.todo_repo,  # AbstractTodoRepository type expected
            todo_management_service=self.todo_management_service,  # AbstractTodoManagementService type expected
            date_time_service=self.date_time_service  # AbstractDateTimeService type expected
        )
        
        self.export_management_service = ExportManagementService(
            todo_management_service=self.todo_management_service  # AbstractTodoManagementService type expected
        )
        
        self.reminder_management_service = ReminderManagementService(
            reminder_repo=self.reminder_repo,  # AbstractReminderRepository type expected
            user_repo=self.user_repo,  # AbstractUserRepository type expected
            email_service=self.email_service,  # AbstractEmailService type expected
            sms_service=self.sms_service,  # AbstractSMSService type expected
            date_time_service=self.date_time_service  # AbstractDateTimeService type expected
        )
        
        self.smart_todo_management_service = SmartTodoManagementService(
            llm_service=self.llm_service,  # AbstractLLMService type expected
            todo_management_service=self.todo_management_service,  # AbstractTodoManagementService type expected
            subtask_management_service=self.subtask_management_service,  # AbstractSubtaskManagementService type expected (optional)
            date_time_service=self.date_time_service  # AbstractDateTimeService type expected (optional)
        )
    
    def get_user_management_service(self) -> UserManagementService:
        return self.user_management_service
    
    def get_todo_management_service(self) -> TodoManagementService:
        return self.todo_management_service
    
    def get_project_management_service(self) -> ProjectManagementService:
        return self.project_management_service
    
    def get_kanban_management_service(self) -> KanbanManagementService:
        return self.kanban_management_service
    
    def get_subtask_management_service(self) -> SubtaskManagementService:
        return self.subtask_management_service
    
    def get_todo_dependency_management_service(self) -> TodoDependencyManagementService:
        return self.todo_dependency_management_service
    
    def get_filter_management_service(self) -> FilterManagementService:
        return self.filter_management_service
    
    def get_bulk_operations_service(self) -> BulkOperationsService:
        return self.bulk_operations_service
    
    def get_export_management_service(self) -> ExportManagementService:
        return self.export_management_service
    
    def get_reminder_management_service(self) -> ReminderManagementService:
        return self.reminder_management_service
    
    def get_smart_todo_management_service(self) -> SmartTodoManagementService:
        return self.smart_todo_management_service


# Global bootstrapper instance
bootstrapper = Bootstrapper()

