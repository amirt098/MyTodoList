# Standard library
import json
import logging

# Third-party
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Internal - from other modules
from runner.bootstrap import bootstrapper
from usecase.todo_management import interface as todo_management_interface
from lib.exceptions import BaseRootException

# Internal - from same module
# (none needed)

logger = logging.getLogger(__name__)


def handle_exception(exception: Exception) -> JsonResponse:
    """Convert exceptions to appropriate JSON responses."""
    if isinstance(exception, BaseRootException):
        # Map exception types to HTTP status codes
        if isinstance(exception, todo_management_interface.TodoTitleRequiredException):
            status = 400
        elif isinstance(exception, todo_management_interface.TodoAccessDeniedException):
            status = 403
        elif isinstance(exception, todo_management_interface.TodoNotFoundByIdException):
            status = 404
        else:
            # Default based on exception base class
            from lib.exceptions import (
                BadRequestRootException,
                UnauthorizedRootException,
                ForbiddenRootException,
                NotFoundRootException,
                InternalServerErrorRootException
            )
            if isinstance(exception, BadRequestRootException):
                status = 400
            elif isinstance(exception, UnauthorizedRootException):
                status = 401
            elif isinstance(exception, ForbiddenRootException):
                status = 403
            elif isinstance(exception, NotFoundRootException):
                status = 404
            elif isinstance(exception, InternalServerErrorRootException):
                status = 500
            else:
                status = 500
        
        return JsonResponse(
            {
                "error": {
                    "message": exception.message,
                    "code": exception.code or "UNKNOWN_ERROR"
                }
            },
            status=status
        )
    else:
        # Unknown exception
        logger.exception("Unhandled exception in REST view")
        return JsonResponse(
            {
                "error": {
                    "message": "Internal server error",
                    "code": "INTERNAL_SERVER_ERROR"
                }
            },
            status=500
        )


@method_decorator(csrf_exempt, name='dispatch')
class CreateTodoView(View):
    """View for creating a todo."""
    
    def post(self, request):
        try:
            # Parse JSON body
            body = json.loads(request.body)
            
            # Convert deadline from datetime string to timestamp_ms if provided
            if 'deadline' in body and body['deadline']:
                from utils.date_utils import datetime_service
                from utils.date_utils.interface.dataclasses import DateTimeParseRequest
                parse_request = DateTimeParseRequest(
                    date_string=body['deadline'],
                    format_str="%Y-%m-%dT%H:%M:%S"  # ISO format
                )
                deadline_dto = datetime_service.parse_datetime(parse_request)
                body['deadline_timestamp_ms'] = deadline_dto.timestamp_ms
                del body['deadline']
            
            # Create request DTO
            create_request = todo_management_interface.CreateTodoRequest(**body)
            
            # Call usecase service
            todo_service = bootstrapper.get_todo_management_service()
            response = todo_service.create_todo(create_request)
            
            # Return JSON response
            return JsonResponse(response.model_dump(), status=201)
        except json.JSONDecodeError:
            return JsonResponse(
                {"error": {"message": "Invalid JSON", "code": "INVALID_JSON"}},
                status=400
            )
        except Exception as e:
            if isinstance(e, BaseRootException):
                return handle_exception(e)
            # Validation errors from Pydantic
            if hasattr(e, 'errors'):
                return JsonResponse(
                    {"error": {"message": "Validation error", "code": "VALIDATION_ERROR", "details": e.errors()}},
                    status=400
                )
            return handle_exception(e)


@method_decorator(csrf_exempt, name='dispatch')
class GetTodoView(View):
    """View for getting a single todo."""
    
    def get(self, request, todo_id):
        try:
            # Get user_id from query params (TODO: should come from authentication)
            user_id = int(request.GET.get('user_id', 0))
            
            # Create request DTO
            get_request = todo_management_interface.GetTodoRequest(
                todo_id=int(todo_id),
                user_id=user_id
            )
            
            # Call usecase service
            todo_service = bootstrapper.get_todo_management_service()
            response = todo_service.get_todo_by_id(get_request)  # Returns TodoDTO
            
            # Return JSON response
            return JsonResponse(response.model_dump(), status=200)
        except ValueError:
            return JsonResponse(
                {"error": {"message": "Invalid todo_id or user_id", "code": "INVALID_ID"}},
                status=400
            )
        except Exception as e:
            if isinstance(e, BaseRootException):
                return handle_exception(e)
            # Validation errors from Pydantic
            if hasattr(e, 'errors'):
                return JsonResponse(
                    {"error": {"message": "Validation error", "code": "VALIDATION_ERROR", "details": e.errors()}},
                    status=400
                )
            return handle_exception(e)


@method_decorator(csrf_exempt, name='dispatch')
class GetTodosView(View):
    """View for getting todos with filters."""
    
    def get(self, request):
        try:
            # Get user_id from query params (TODO: should come from authentication)
            user_id = int(request.GET.get('user_id', 0))
            
            # Build request from query params (convert datetime strings to timestamp_ms if needed)
            request_data = {
                "user_id": user_id,
                "project_id": int(request.GET.get('project_id')) if request.GET.get('project_id') else None,
                "status": request.GET.get('status'),
                "priority": request.GET.get('priority'),
                "category": request.GET.get('category'),
                "label": request.GET.get('label'),
                "deadline_after_timestamp_ms": int(request.GET.get('deadline_after_timestamp_ms')) if request.GET.get('deadline_after_timestamp_ms') else None,
                "deadline_before_timestamp_ms": int(request.GET.get('deadline_before_timestamp_ms')) if request.GET.get('deadline_before_timestamp_ms') else None,
                "created_after_timestamp_ms": int(request.GET.get('created_after_timestamp_ms')) if request.GET.get('created_after_timestamp_ms') else None,
                "created_before_timestamp_ms": int(request.GET.get('created_before_timestamp_ms')) if request.GET.get('created_before_timestamp_ms') else None,
                "search": request.GET.get('search'),
                "order_by": request.GET.get('order_by', '-created_at'),
                "limit": int(request.GET.get('limit')) if request.GET.get('limit') else None,
                "offset": int(request.GET.get('offset')) if request.GET.get('offset') else None,
            }
            # Remove None values
            request_data = {k: v for k, v in request_data.items() if v is not None}
            
            # Create request DTO (TodoFilter)
            todo_filter = todo_management_interface.TodoFilter(**request_data)
            
            # Call usecase service
            todo_service = bootstrapper.get_todo_management_service()
            response = todo_service.get_todos(todo_filter)
            
            # Convert response to dict
            response_dict = {
                "todos": [todo.model_dump() for todo in response.todos],
                "total": response.total
            }
            
            # Return JSON response
            return JsonResponse(response_dict, status=200)
        except ValueError:
            return JsonResponse(
                {"error": {"message": "Invalid user_id or query parameters", "code": "INVALID_PARAMS"}},
                status=400
            )
        except Exception as e:
            if isinstance(e, BaseRootException):
                return handle_exception(e)
            # Validation errors from Pydantic
            if hasattr(e, 'errors'):
                return JsonResponse(
                    {"error": {"message": "Validation error", "code": "VALIDATION_ERROR", "details": e.errors()}},
                    status=400
                )
            return handle_exception(e)


@method_decorator(csrf_exempt, name='dispatch')
class UpdateTodoView(View):
    """View for updating a todo."""
    
    def put(self, request, todo_id):
        try:
            # Parse JSON body
            body = json.loads(request.body)
            body['todo_id'] = int(todo_id)
            
            # Create request DTO
            update_request = todo_management_interface.UpdateTodoRequest(**body)
            
            # Call usecase service
            todo_service = bootstrapper.get_todo_management_service()
            response = todo_service.update_todo(update_request)
            
            # Return JSON response
            return JsonResponse(response.model_dump(), status=200)
        except json.JSONDecodeError:
            return JsonResponse(
                {"error": {"message": "Invalid JSON", "code": "INVALID_JSON"}},
                status=400
            )
        except ValueError:
            return JsonResponse(
                {"error": {"message": "Invalid todo_id", "code": "INVALID_ID"}},
                status=400
            )
        except Exception as e:
            if isinstance(e, BaseRootException):
                return handle_exception(e)
            # Validation errors from Pydantic
            if hasattr(e, 'errors'):
                return JsonResponse(
                    {"error": {"message": "Validation error", "code": "VALIDATION_ERROR", "details": e.errors()}},
                    status=400
                )
            return handle_exception(e)


@method_decorator(csrf_exempt, name='dispatch')
class DeleteTodoView(View):
    """View for deleting a todo."""
    
    def delete(self, request, todo_id):
        try:
            # Get user_id from query params (TODO: should come from authentication)
            user_id = int(request.GET.get('user_id', 0))
            
            # Create request DTO
            delete_request = todo_management_interface.DeleteTodoRequest(
                todo_id=int(todo_id),
                user_id=user_id
            )
            
            # Call usecase service
            todo_service = bootstrapper.get_todo_management_service()
            response = todo_service.delete_todo(delete_request)
            
            # Return JSON response
            return JsonResponse(response.model_dump(), status=200)
        except ValueError:
            return JsonResponse(
                {"error": {"message": "Invalid todo_id or user_id", "code": "INVALID_ID"}},
                status=400
            )
        except Exception as e:
            if isinstance(e, BaseRootException):
                return handle_exception(e)
            # Validation errors from Pydantic
            if hasattr(e, 'errors'):
                return JsonResponse(
                    {"error": {"message": "Validation error", "code": "VALIDATION_ERROR", "details": e.errors()}},
                    status=400
                )
            return handle_exception(e)

