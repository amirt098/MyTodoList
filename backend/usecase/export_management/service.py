# Standard library
import json
import csv
import io
import logging
from datetime import datetime

# Third-party
# (none needed)

# Internal - from other modules
from usecase.todo_management import interface as todo_management_interface

# Internal - from same module
from . import interface

logger = logging.getLogger(__name__)


def _todo_to_dict(todo: todo_management_interface.TodoDTO) -> dict:
    """Convert TodoDTO to dictionary for export."""
    return {
        'id': todo.todo_id,
        'title': todo.title,
        'description': todo.description,
        'status': todo.status,
        'priority': todo.priority,
        'category': todo.category,
        'labels': ','.join(todo.labels) if todo.labels else '',
        'project_id': todo.project_id,
        'deadline': datetime.fromtimestamp(todo.deadline_timestamp_ms / 1000).isoformat() if todo.deadline_timestamp_ms else '',
        'created_at': datetime.fromtimestamp(todo.created_at / 1000).isoformat(),
        'updated_at': datetime.fromtimestamp(todo.updated_at / 1000).isoformat(),
        'completed_at': datetime.fromtimestamp(todo.completed_at_timestamp_ms / 1000).isoformat() if todo.completed_at_timestamp_ms else '',
        'progress': todo.progress,
        'auto_repeat': todo.auto_repeat
    }


class ExportManagementService(interface.AbstractExportManagementService):
    """Service for managing export operations."""
    
    def __init__(
        self,
        todo_management_service: todo_management_interface.AbstractTodoManagementService,
    ):
        self.todo_management_service = todo_management_service
    
    def export_todos(self, request: interface.ExportTodosRequest) -> interface.ExportTodosResponse:
        logger.info(f"Exporting todos in {request.format} format", extra={"input": request.model_dump()})
        
        # Validate format
        if request.format not in ['json', 'csv']:
            logger.warning(f"Invalid export format: {request.format}")
            raise interface.InvalidExportFormatException(request.format)
        
        # Get todos using TodoManagementService
        todo_filter = todo_management_interface.TodoFilter(
            user_id=request.user_id,
            project_id=request.project_id,
            status=request.status,
            priority=request.priority,
            category=request.category,
            label=request.label
        )
        
        todo_list_response = self.todo_management_service.get_todos(todo_filter)
        todos = todo_list_response.todos
        
        # Generate filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"todos_export_{timestamp}.{request.format}"
        
        # Export based on format
        if request.format == 'json':
            content = self._export_json(todos)
        else:  # csv
            content = self._export_csv(todos)
        
        response = interface.ExportTodosResponse(
            format=request.format,
            content=content,
            total_todos=len(todos),
            filename=filename
        )
        
        logger.info(f"Exported {len(todos)} todos in {request.format} format", 
                   extra={"output": {"total": len(todos), "format": request.format}})
        return response
    
    def _export_json(self, todos: list[todo_management_interface.TodoDTO]) -> str:
        """Export todos as JSON."""
        todos_data = [_todo_to_dict(todo) for todo in todos]
        return json.dumps(todos_data, indent=2, ensure_ascii=False)
    
    def _export_csv(self, todos: list[todo_management_interface.TodoDTO]) -> str:
        """Export todos as CSV."""
        if not todos:
            return ""
        
        output = io.StringIO()
        fieldnames = ['id', 'title', 'description', 'status', 'priority', 'category', 'labels', 
                     'project_id', 'deadline', 'created_at', 'updated_at', 'completed_at', 
                     'progress', 'auto_repeat']
        
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        
        for todo in todos:
            writer.writerow(_todo_to_dict(todo))
        
        return output.getvalue()

