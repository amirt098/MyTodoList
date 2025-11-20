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
from usecase.subtask_management import interface as subtask_management_interface
from usecase.todo_dependency_management import interface as todo_dependency_management_interface
from lib.exceptions import BaseRootException

# Internal - from same module
# (none needed)

logger = logging.getLogger(__name__)


def handle_exception(exception: Exception) -> JsonResponse:
    """Convert exceptions to appropriate JSON responses."""
    if isinstance(exception, BaseRootException):
        # Map exception types to HTTP status codes
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


# ==================== Subtask Views ====================

@method_decorator(csrf_exempt, name='dispatch')
class AddSubtaskView(View):
    """View for adding a subtask to a todo."""
    
    def post(self, request):
        try:
            # Parse JSON body
            body = json.loads(request.body)
            
            # Create request DTO
            add_request = subtask_management_interface.AddSubtaskRequest(**body)
            
            # Call usecase service
            subtask_service = bootstrapper.get_subtask_management_service()
            response = subtask_service.add_subtask(add_request)
            
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
class UpdateSubtaskView(View):
    """View for updating a subtask."""
    
    def put(self, request, subtask_id):
        try:
            # Parse JSON body
            body = json.loads(request.body)
            body['subtask_id'] = int(subtask_id)
            
            # Create request DTO
            update_request = subtask_management_interface.UpdateSubtaskRequest(**body)
            
            # Call usecase service
            subtask_service = bootstrapper.get_subtask_management_service()
            response = subtask_service.update_subtask(update_request)
            
            # Return JSON response
            return JsonResponse(response.model_dump(), status=200)
        except json.JSONDecodeError:
            return JsonResponse(
                {"error": {"message": "Invalid JSON", "code": "INVALID_JSON"}},
                status=400
            )
        except ValueError:
            return JsonResponse(
                {"error": {"message": "Invalid subtask_id", "code": "INVALID_ID"}},
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
class DeleteSubtaskView(View):
    """View for deleting a subtask."""
    
    def delete(self, request, subtask_id):
        try:
            # Get user_id and todo_id from query params (TODO: should come from authentication)
            user_id = int(request.GET.get('user_id', 0))
            todo_id = int(request.GET.get('todo_id', 0))
            
            # Create request DTO
            delete_request = subtask_management_interface.DeleteSubtaskRequest(
                subtask_id=int(subtask_id),
                todo_id=todo_id,
                user_id=user_id
            )
            
            # Call usecase service
            subtask_service = bootstrapper.get_subtask_management_service()
            response = subtask_service.delete_subtask(delete_request)
            
            # Return JSON response
            return JsonResponse(response.model_dump(), status=200)
        except ValueError:
            return JsonResponse(
                {"error": {"message": "Invalid subtask_id, todo_id, or user_id", "code": "INVALID_ID"}},
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
class MarkSubtaskDoneView(View):
    """View for marking a subtask as done or undone."""
    
    def post(self, request, subtask_id):
        try:
            # Parse JSON body
            body = json.loads(request.body)
            body['subtask_id'] = int(subtask_id)
            
            # Create request DTO
            mark_request = subtask_management_interface.MarkSubtaskDoneRequest(**body)
            
            # Call usecase service
            subtask_service = bootstrapper.get_subtask_management_service()
            response = subtask_service.mark_subtask_done(mark_request)
            
            # Return JSON response
            return JsonResponse(response.model_dump(), status=200)
        except json.JSONDecodeError:
            return JsonResponse(
                {"error": {"message": "Invalid JSON", "code": "INVALID_JSON"}},
                status=400
            )
        except ValueError:
            return JsonResponse(
                {"error": {"message": "Invalid subtask_id", "code": "INVALID_ID"}},
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
class GetSubtasksView(View):
    """View for getting subtasks for a todo."""
    
    def get(self, request, todo_id):
        try:
            # Get user_id from query params (TODO: should come from authentication)
            user_id = int(request.GET.get('user_id', 0))
            status = request.GET.get('status')  # Optional filter
            
            # Create request DTO
            get_request = subtask_management_interface.GetSubtasksRequest(
                todo_id=int(todo_id),
                user_id=user_id,
                status=status
            )
            
            # Call usecase service
            subtask_service = bootstrapper.get_subtask_management_service()
            response = subtask_service.get_subtasks(get_request)
            
            # Convert response to dict
            response_dict = {
                "subtasks": [st.model_dump() for st in response.subtasks],
                "total": response.total,
                "progress": response.progress
            }
            
            # Return JSON response
            return JsonResponse(response_dict, status=200)
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


# ==================== Dependency Views ====================

@method_decorator(csrf_exempt, name='dispatch')
class SetDependencyView(View):
    """View for setting a todo dependency."""
    
    def post(self, request):
        try:
            # Parse JSON body
            body = json.loads(request.body)
            
            # Create request DTO
            set_request = todo_dependency_management_interface.SetDependencyRequest(**body)
            
            # Call usecase service
            dependency_service = bootstrapper.get_todo_dependency_management_service()
            response = dependency_service.set_dependency(set_request)
            
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
class RemoveDependencyView(View):
    """View for removing a todo dependency."""
    
    def delete(self, request, todo_id):
        try:
            # Get user_id and dependency_type from query params (TODO: should come from authentication)
            user_id = int(request.GET.get('user_id', 0))
            dependency_type = request.GET.get('dependency_type', 'previous')
            
            # Create request DTO
            remove_request = todo_dependency_management_interface.RemoveDependencyRequest(
                todo_id=int(todo_id),
                dependency_type=dependency_type,
                user_id=user_id
            )
            
            # Call usecase service
            dependency_service = bootstrapper.get_todo_dependency_management_service()
            response = dependency_service.remove_dependency(remove_request)
            
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
class ValidateDependencyView(View):
    """View for validating a todo dependency chain."""
    
    def get(self, request, todo_id):
        try:
            # Get user_id from query params (TODO: should come from authentication)
            user_id = int(request.GET.get('user_id', 0))
            
            # Create request DTO
            validate_request = todo_dependency_management_interface.ValidateDependencyRequest(
                todo_id=int(todo_id),
                user_id=user_id
            )
            
            # Call usecase service
            dependency_service = bootstrapper.get_todo_dependency_management_service()
            response = dependency_service.validate_dependency(validate_request)
            
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
class GetDependencyChainView(View):
    """View for getting a todo dependency chain."""
    
    def get(self, request, todo_id):
        try:
            # Get user_id and direction from query params (TODO: should come from authentication)
            user_id = int(request.GET.get('user_id', 0))
            direction = request.GET.get('direction', 'both')
            
            # Create request DTO
            get_request = todo_dependency_management_interface.GetDependencyChainRequest(
                todo_id=int(todo_id),
                user_id=user_id,
                direction=direction
            )
            
            # Call usecase service
            dependency_service = bootstrapper.get_todo_dependency_management_service()
            response = dependency_service.get_dependency_chain(get_request)
            
            # Convert response to dict
            response_dict = {
                "todo_id": response.todo_id,
                "chain": [node.model_dump() for node in response.chain],
                "total_todos": response.total_todos
            }
            
            # Return JSON response
            return JsonResponse(response_dict, status=200)
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

