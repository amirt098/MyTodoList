# Standard library
import logging

# Third-party
# (none needed)

# Internal - from other modules
from repository.kanban import interface as kanban_repository_interface
from repository.todo import interface as todo_repository_interface
from repository.project import interface as project_repository_interface
from usecase.todo_management import interface as todo_management_interface
from utils.date_utils import interface as date_utils_interface

# Internal - from same module
from . import interface

logger = logging.getLogger(__name__)


# Default columns for kanban board
DEFAULT_COLUMNS = [
    {"name": "ToDo", "status_value": "ToDo", "color": "#6B7280", "order": 0, "is_default": True},
    {"name": "In Progress", "status_value": "In Progress", "color": "#3B82F6", "order": 1, "is_default": True},
    {"name": "Done", "status_value": "Done", "color": "#10B981", "order": 2, "is_default": True},
]


def _repo_column_dto_to_usecase_dto(repo_dto: kanban_repository_interface.KanbanColumnDTO) -> interface.KanbanColumnDTO:
    """Simple converter: Repository KanbanColumnDTO to UseCase KanbanColumnDTO."""
    return interface.KanbanColumnDTO(
        column_id=repo_dto.column_id,
        name=repo_dto.name,
        status_value=repo_dto.status_value,
        color=repo_dto.color,
        project_id=repo_dto.project_id,
        user_id=repo_dto.user_id,
        order=repo_dto.order,
        is_default=repo_dto.is_default,
        is_active=repo_dto.is_active
    )


def _todo_dto_to_kanban_card(todo_dto: todo_repository_interface.TodoDTO) -> interface.KanbanCardDTO:
    """Convert TodoDTO to KanbanCardDTO."""
    return interface.KanbanCardDTO(
        todo_id=todo_dto.todo_id,
        title=todo_dto.title,
        description=todo_dto.description or "",
        priority=todo_dto.priority,
        status=todo_dto.status,
        labels=todo_dto.labels if todo_dto.labels else [],
        deadline_timestamp_ms=todo_dto.deadline_timestamp_ms,
        project_id=todo_dto.project_id,
        order=todo_dto.order,
        progress=0.0  # TODO: Calculate progress based on subtasks (Phase 6)
    )


class KanbanManagementService(interface.AbstractKanbanManagementService):
    """Service for managing kanban board operations."""
    
    def __init__(
        self,
        kanban_repo: kanban_repository_interface.AbstractKanbanRepository,
        todo_repo: todo_repository_interface.AbstractTodoRepository,
        project_repo: project_repository_interface.AbstractProjectRepository,
        todo_management_service: todo_management_interface.AbstractTodoManagementService,
        date_time_service: date_utils_interface.AbstractDateTimeService,
    ):
        self.kanban_repo = kanban_repo
        self.todo_repo = todo_repo
        self.project_repo = project_repo
        self.todo_management_service = todo_management_service
        self.date_time_service = date_time_service
    
    def get_kanban_board(self, request: interface.GetKanbanBoardRequest) -> interface.GetKanbanBoardResponse:
        logger.info(f"Getting kanban board for project_id={request.project_id}, user_id={request.user_id}", 
                   extra={"input": request.model_dump()})
        
        # Verify project access if project_id is provided
        if request.project_id:
            project_dto = self.project_repo.get_by_id(request.project_id)
            if not project_dto:
                logger.warning(f"Project not found: {request.project_id}")
                raise interface.KanbanManagementNotFoundException(f"Project {request.project_id} not found")
            
            # Check access for private projects
            if project_dto.is_private and project_dto.owner_id != request.user_id:
                member = self.project_repo.get_member(request.project_id, request.user_id)
                if not member:
                    logger.warning(f"Access denied - user {request.user_id} tried to access project {request.project_id}")
                    raise interface.KanbanManagementBadRequestException(
                        f"User {request.user_id} does not have access to project {request.project_id}"
                    )
        
        # Get columns (custom columns for project/user, or default columns)
        column_filter = kanban_repository_interface.KanbanColumnFilter(
            project_id=request.project_id,
            user_id=request.user_id if not request.project_id else None,
            is_active=True,
            order_by='order'
        )
        custom_columns = self.kanban_repo.get_columns(column_filter)
        
        # If no custom columns, use default columns
        columns = []
        if custom_columns:
            columns = [_repo_column_dto_to_usecase_dto(col) for col in custom_columns]
        else:
            # Create default columns DTOs
            for col_data in DEFAULT_COLUMNS:
                columns.append(interface.KanbanColumnDTO(
                    column_id=0,  # Default columns don't have IDs
                    name=col_data["name"],
                    status_value=col_data["status_value"],
                    color=col_data["color"],
                    project_id=request.project_id,
                    user_id=request.user_id if not request.project_id else None,
                    order=col_data["order"],
                    is_default=col_data["is_default"],
                    is_active=True
                ))
        
        # Get todos for the board
        todo_filter = todo_repository_interface.TodoFilter(
            user_id=request.user_id,
            project_id=request.project_id,
            order_by='order'
        )
        todos = self.todo_repo.get_todos(todo_filter)
        
        # Convert todos to kanban cards
        cards = [_todo_dto_to_kanban_card(todo) for todo in todos]
        
        response = interface.GetKanbanBoardResponse(
            columns=columns,
            cards=cards,
            project_id=request.project_id
        )
        
        logger.info(f"Kanban board retrieved: {len(columns)} columns, {len(cards)} cards", 
                   extra={"output": {"columns_count": len(columns), "cards_count": len(cards)}})
        return response
    
    def move_todo(self, request: interface.MoveTodoRequest) -> interface.MoveTodoResponse:
        logger.info(f"Moving todo {request.todo_id} to status {request.new_status}", 
                   extra={"input": request.model_dump()})
        
        # Get existing todo
        todo_dto = self.todo_repo.get_by_id(request.todo_id)
        if not todo_dto:
            logger.warning(f"Todo not found: {request.todo_id}")
            raise interface.TodoNotFoundByIdException(request.todo_id)
        
        # Verify access
        if todo_dto.user_id != request.user_id:
            logger.warning(f"Access denied - user {request.user_id} tried to move todo {request.todo_id}")
            raise interface.KanbanManagementBadRequestException(
                f"User {request.user_id} does not have access to todo {request.todo_id}"
            )
        
        old_status = todo_dto.status
        
        # Update todo status via TodoManagementService
        update_request = todo_management_interface.UpdateTodoRequest(
            todo_id=request.todo_id,
            user_id=request.user_id,
            status=request.new_status,
            order=request.new_order
        )
        
        self.todo_management_service.update_todo(update_request)
        
        response = interface.MoveTodoResponse(
            todo_id=request.todo_id,
            old_status=old_status,
            new_status=request.new_status,
            success=True
        )
        
        logger.info(f"Todo moved successfully: {request.todo_id} from {old_status} to {request.new_status}", 
                   extra={"output": response.model_dump()})
        return response
    
    def create_column(self, request: interface.CreateColumnRequest) -> interface.CreateColumnResponse:
        logger.info(f"Creating kanban column: {request.name}", extra={"input": request.model_dump()})
        
        if not request.name:
            logger.warning("Column creation failed - name is required")
            raise interface.KanbanColumnNameRequiredException()
        
        # Calculate timestamps
        now_dto = self.date_time_service.now()
        
        # Determine order if not provided
        order = request.order
        if order is None:
            # Get max order for this project/user
            column_filter = kanban_repository_interface.KanbanColumnFilter(
                project_id=request.project_id,
                user_id=request.user_id if not request.project_id else None,
                is_active=True
            )
            existing_columns = self.kanban_repo.get_columns(column_filter)
            if existing_columns:
                max_order = max(col.order for col in existing_columns)
                order = max_order + 1
            else:
                order = 0
        
        # Create column
        column_create_request = kanban_repository_interface.KanbanColumnCreateRequest(
            name=request.name,
            status_value=request.status_value or "",
            color=request.color or "#6B7280",
            project_id=request.project_id,
            user_id=request.user_id if not request.project_id else None,
            order=order,
            is_default=False,
            is_active=True,
            created_at=now_dto.timestamp_ms,
            updated_at=now_dto.timestamp_ms
        )
        
        column_dto = self.kanban_repo.create_column(column_create_request)
        
        response = interface.CreateColumnResponse(
            column_id=column_dto.column_id,
            name=column_dto.name,
            status_value=column_dto.status_value,
            color=column_dto.color,
            order=column_dto.order
        )
        
        logger.info(f"Kanban column created successfully: {response.column_id}", 
                   extra={"output": response.model_dump()})
        return response
    
    def delete_column(self, request: interface.DeleteColumnRequest) -> interface.DeleteColumnResponse:
        logger.info(f"Deleting kanban column: {request.column_id}", extra={"input": request.model_dump()})
        
        # Get column
        column_dto = self.kanban_repo.get_column_by_id(request.column_id)
        if not column_dto:
            logger.warning(f"Kanban column not found: {request.column_id}")
            raise interface.KanbanColumnNotFoundByIdException(request.column_id)
        
        # Verify access (user must own the column or be project owner/admin)
        if column_dto.user_id and column_dto.user_id != request.user_id:
            logger.warning(f"Access denied - user {request.user_id} tried to delete column {request.column_id}")
            raise interface.KanbanManagementBadRequestException(
                f"User {request.user_id} does not have access to column {request.column_id}"
            )
        
        if column_dto.project_id:
            project_dto = self.project_repo.get_by_id(column_dto.project_id)
            if project_dto:
                if project_dto.owner_id != request.user_id:
                    member = self.project_repo.get_member(column_dto.project_id, request.user_id)
                    if not member or member.role not in ['Owner', 'Admin']:
                        logger.warning(f"Access denied - user {request.user_id} tried to delete column {request.column_id}")
                        raise interface.KanbanManagementBadRequestException(
                            f"User {request.user_id} does not have access to column {request.column_id}"
                        )
        
        # Cannot delete default columns
        if column_dto.is_default:
            logger.warning(f"Cannot delete default column: {request.column_id}")
            raise interface.KanbanManagementBadRequestException("Cannot delete default columns")
        
        # Delete column
        self.kanban_repo.delete_column(request.column_id)
        
        response = interface.DeleteColumnResponse(
            success=True,
            message=f"Kanban column {request.column_id} deleted successfully"
        )
        
        logger.info(f"Kanban column deleted successfully: {request.column_id}", 
                   extra={"output": response.model_dump()})
        return response
    
    def reorder_columns(self, request: interface.ReorderColumnsRequest) -> interface.ReorderColumnsResponse:
        logger.info(f"Reordering columns for project_id={request.project_id}, user_id={request.user_id}", 
                   extra={"input": request.model_dump()})
        
        # Verify project access if project_id is provided
        if request.project_id:
            project_dto = self.project_repo.get_by_id(request.project_id)
            if project_dto and project_dto.is_private and project_dto.owner_id != request.user_id:
                member = self.project_repo.get_member(request.project_id, request.user_id)
                if not member or member.role not in ['Owner', 'Admin']:
                    logger.warning(f"Access denied - user {request.user_id} tried to reorder columns")
                    raise interface.KanbanManagementBadRequestException(
                        f"User {request.user_id} does not have access to reorder columns"
                    )
        
        # Update each column's order
        now_dto = self.date_time_service.now()
        for col_order in request.column_orders:
            column_id = col_order.get('column_id')
            new_order = col_order.get('order')
            
            if column_id is None or new_order is None:
                continue
            
            # Verify column exists and user has access
            column_dto = self.kanban_repo.get_column_by_id(column_id)
            if not column_dto:
                continue
            
            # Update column order
            column_update_request = kanban_repository_interface.KanbanColumnUpdateRequest(
                order=new_order,
                updated_at=now_dto.timestamp_ms
            )
            self.kanban_repo.update_column(column_id, column_update_request)
        
        response = interface.ReorderColumnsResponse(
            success=True,
            message="Columns reordered successfully"
        )
        
        logger.info(f"Columns reordered successfully", extra={"output": response.model_dump()})
        return response

