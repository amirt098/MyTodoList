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
from usecase.kanban_management import interface as kanban_management_interface
from lib.exceptions import BaseRootException

# Internal - from same module
# (none needed)

logger = logging.getLogger(__name__)


def handle_exception(exception: Exception) -> JsonResponse:
    """Convert exceptions to appropriate JSON responses."""
    if isinstance(exception, BaseRootException):
        # Map exception types to HTTP status codes
        if isinstance(exception, kanban_management_interface.KanbanColumnNameRequiredException):
            status = 400
        elif isinstance(exception, kanban_management_interface.KanbanColumnNotFoundByIdException):
            status = 404
        elif isinstance(exception, kanban_management_interface.TodoNotFoundByIdException):
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
class GetKanbanBoardView(View):
    """View for getting kanban board."""
    
    def get(self, request):
        try:
            # Get user_id from authentication token
            from .auth_utils import get_user_from_token
            user_id = get_user_from_token(request)
            
            if user_id is None:
                return JsonResponse(
                    {"error": {"message": "Authentication required", "code": "AUTHENTICATION_REQUIRED"}},
                    status=401
                )
            
            project_id = int(request.GET.get('project_id')) if request.GET.get('project_id') else None
            
            # Create request DTO
            get_request = kanban_management_interface.GetKanbanBoardRequest(
                project_id=project_id,
                user_id=user_id
            )
            
            # Call usecase service
            kanban_service = bootstrapper.get_kanban_management_service()
            response = kanban_service.get_kanban_board(get_request)
            
            # Convert response to dict
            response_dict = {
                "columns": [col.model_dump() for col in response.columns],
                "cards": [card.model_dump() for card in response.cards],
                "project_id": response.project_id
            }
            
            # Return JSON response
            return JsonResponse(response_dict, status=200)
        except ValueError:
            return JsonResponse(
                {"error": {"message": "Invalid user_id or project_id", "code": "INVALID_ID"}},
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
class MoveTodoView(View):
    """View for moving todo between columns."""
    
    def post(self, request):
        try:
            # Get user_id from authentication token
            from .auth_utils import get_user_from_token
            user_id = get_user_from_token(request)
            
            if user_id is None:
                return JsonResponse(
                    {"error": {"message": "Authentication required", "code": "AUTHENTICATION_REQUIRED"}},
                    status=401
                )
            
            # Parse JSON body
            body = json.loads(request.body)
            
            # Override user_id from token (security: user can only move their own todos)
            body['user_id'] = user_id
            
            # Create request DTO
            move_request = kanban_management_interface.MoveTodoRequest(**body)
            
            # Call usecase service
            kanban_service = bootstrapper.get_kanban_management_service()
            response = kanban_service.move_todo(move_request)
            
            # Return JSON response
            return JsonResponse(response.model_dump(), status=200)
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
class CreateColumnView(View):
    """View for creating a kanban column."""
    
    def post(self, request):
        try:
            # Parse JSON body
            body = json.loads(request.body)
            
            # Create request DTO
            create_request = kanban_management_interface.CreateColumnRequest(**body)
            
            # Call usecase service
            kanban_service = bootstrapper.get_kanban_management_service()
            response = kanban_service.create_column(create_request)
            
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
class DeleteColumnView(View):
    """View for deleting a kanban column."""
    
    def delete(self, request, column_id):
        try:
            # Get user_id from query params (TODO: should come from authentication)
            user_id = int(request.GET.get('user_id', 0))
            
            # Create request DTO
            delete_request = kanban_management_interface.DeleteColumnRequest(
                column_id=int(column_id),
                user_id=user_id
            )
            
            # Call usecase service
            kanban_service = bootstrapper.get_kanban_management_service()
            response = kanban_service.delete_column(delete_request)
            
            # Return JSON response
            return JsonResponse(response.model_dump(), status=200)
        except ValueError:
            return JsonResponse(
                {"error": {"message": "Invalid column_id or user_id", "code": "INVALID_ID"}},
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
class ReorderColumnsView(View):
    """View for reordering kanban columns."""
    
    def post(self, request):
        try:
            # Parse JSON body
            body = json.loads(request.body)
            
            # Create request DTO
            reorder_request = kanban_management_interface.ReorderColumnsRequest(**body)
            
            # Call usecase service
            kanban_service = bootstrapper.get_kanban_management_service()
            response = kanban_service.reorder_columns(reorder_request)
            
            # Return JSON response
            return JsonResponse(response.model_dump(), status=200)
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

