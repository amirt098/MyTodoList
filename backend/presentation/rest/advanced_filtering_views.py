# Standard library
import json
import logging

# Third-party
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Internal - from other modules
from runner.bootstrap import bootstrapper
from usecase.todo_management import interface as todo_management_interface
from usecase.filter_management import interface as filter_management_interface
from usecase.bulk_operations import interface as bulk_operations_interface
from usecase.export_management import interface as export_management_interface
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


# ==================== Unified View ====================

@method_decorator(csrf_exempt, name='dispatch')
class GetAllMyTodosView(View):
    """View for getting all my todos (unified view)."""
    
    def get(self, request):
        try:
            # Get user_id from query params (TODO: should come from authentication)
            user_id = int(request.GET.get('user_id', 0))
            
            # Get optional filters from query params
            status = request.GET.get('status')
            priority = request.GET.get('priority')
            category = request.GET.get('category')
            label = request.GET.get('label')
            deadline_after__gte = int(request.GET.get('deadline_after__gte')) if request.GET.get('deadline_after__gte') else None
            deadline_after__lte = int(request.GET.get('deadline_after__lte')) if request.GET.get('deadline_after__lte') else None
            search = request.GET.get('search')
            order_by = request.GET.get('order_by', '-created_at')
            limit = int(request.GET.get('limit')) if request.GET.get('limit') else None
            offset = int(request.GET.get('offset')) if request.GET.get('offset') else None
            
            # Create request DTO
            get_request = todo_management_interface.GetAllMyTodosRequest(
                user_id=user_id,
                status=status,
                priority=priority,
                category=category,
                label=label,
                deadline_after__gte=deadline_after__gte,
                deadline_after__lte=deadline_after__lte,
                search=search,
                order_by=order_by,
                limit=limit,
                offset=offset
            )
            
            # Call usecase service
            todo_service = bootstrapper.get_todo_management_service()
            response = todo_service.get_all_my_todos(get_request)
            
            # Convert response to dict
            response_dict = {
                "todos": [todo.model_dump() for todo in response.todos],
                "total": response.total
            }
            
            # Return JSON response
            return JsonResponse(response_dict, status=200)
        except ValueError:
            return JsonResponse(
                {"error": {"message": "Invalid user_id or filter parameters", "code": "INVALID_PARAMETERS"}},
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


# ==================== Saved Filters ====================

@method_decorator(csrf_exempt, name='dispatch')
class SaveFilterView(View):
    """View for saving a filter."""
    
    def post(self, request):
        try:
            # Parse JSON body
            body = json.loads(request.body)
            
            # Create request DTO
            save_request = filter_management_interface.SaveFilterRequest(**body)
            
            # Call usecase service
            filter_service = bootstrapper.get_filter_management_service()
            response = filter_service.save_filter(save_request)
            
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
class GetSavedFiltersView(View):
    """View for getting saved filters."""
    
    def get(self, request):
        try:
            # Get user_id from query params (TODO: should come from authentication)
            user_id = int(request.GET.get('user_id', 0))
            is_default = request.GET.get('is_default')
            is_default_bool = None if is_default is None else is_default.lower() == 'true'
            
            # Create request DTO
            get_request = filter_management_interface.GetSavedFiltersRequest(
                user_id=user_id,
                is_default=is_default_bool
            )
            
            # Call usecase service
            filter_service = bootstrapper.get_filter_management_service()
            response = filter_service.get_saved_filters(get_request)
            
            # Convert response to dict
            response_dict = {
                "filters": [f.model_dump() for f in response.filters],
                "total": response.total
            }
            
            # Return JSON response
            return JsonResponse(response_dict, status=200)
        except ValueError:
            return JsonResponse(
                {"error": {"message": "Invalid user_id", "code": "INVALID_ID"}},
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
class DeleteSavedFilterView(View):
    """View for deleting a saved filter."""
    
    def delete(self, request, filter_id):
        try:
            # Get user_id from query params (TODO: should come from authentication)
            user_id = int(request.GET.get('user_id', 0))
            
            # Create request DTO
            delete_request = filter_management_interface.DeleteSavedFilterRequest(
                filter_id=int(filter_id),
                user_id=user_id
            )
            
            # Call usecase service
            filter_service = bootstrapper.get_filter_management_service()
            response = filter_service.delete_saved_filter(delete_request)
            
            # Return JSON response
            return JsonResponse(response.model_dump(), status=200)
        except ValueError:
            return JsonResponse(
                {"error": {"message": "Invalid filter_id or user_id", "code": "INVALID_ID"}},
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


# ==================== Bulk Operations ====================

@method_decorator(csrf_exempt, name='dispatch')
class BulkUpdateView(View):
    """View for bulk updating todos."""
    
    def post(self, request):
        try:
            # Parse JSON body
            body = json.loads(request.body)
            
            # Create request DTO
            bulk_request = bulk_operations_interface.BulkUpdateRequest(**body)
            
            # Call usecase service
            bulk_service = bootstrapper.get_bulk_operations_service()
            response = bulk_service.bulk_update(bulk_request)
            
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
class BulkDeleteView(View):
    """View for bulk deleting todos."""
    
    def post(self, request):
        try:
            # Parse JSON body
            body = json.loads(request.body)
            
            # Create request DTO
            bulk_request = bulk_operations_interface.BulkDeleteRequest(**body)
            
            # Call usecase service
            bulk_service = bootstrapper.get_bulk_operations_service()
            response = bulk_service.bulk_delete(bulk_request)
            
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


# ==================== Export ====================

@method_decorator(csrf_exempt, name='dispatch')
class ExportTodosView(View):
    """View for exporting todos."""
    
    def get(self, request):
        try:
            # Get user_id and format from query params (TODO: should come from authentication)
            user_id = int(request.GET.get('user_id', 0))
            format_type = request.GET.get('format', 'json')
            
            # Get optional filters from query params
            project_id = int(request.GET.get('project_id')) if request.GET.get('project_id') else None
            status = request.GET.get('status')
            priority = request.GET.get('priority')
            category = request.GET.get('category')
            label = request.GET.get('label')
            
            # Create request DTO
            export_request = export_management_interface.ExportTodosRequest(
                user_id=user_id,
                format=format_type,
                project_id=project_id,
                status=status,
                priority=priority,
                category=category,
                label=label
            )
            
            # Call usecase service
            export_service = bootstrapper.get_export_management_service()
            response = export_service.export_todos(export_request)
            
            # Return file response
            if format_type == 'json':
                http_response = HttpResponse(response.content, content_type='application/json')
            else:  # csv
                http_response = HttpResponse(response.content, content_type='text/csv')
            
            http_response['Content-Disposition'] = f'attachment; filename="{response.filename}"'
            return http_response
        except ValueError:
            return JsonResponse(
                {"error": {"message": "Invalid user_id or filter parameters", "code": "INVALID_PARAMETERS"}},
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

