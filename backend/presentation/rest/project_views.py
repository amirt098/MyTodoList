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
from usecase.project_management import interface as project_management_interface
from lib.exceptions import BaseRootException

# Internal - from same module
# (none needed)

logger = logging.getLogger(__name__)


def handle_exception(exception: Exception) -> JsonResponse:
    """Convert exceptions to appropriate JSON responses."""
    if isinstance(exception, BaseRootException):
        # Map exception types to HTTP status codes
        if isinstance(exception, project_management_interface.ProjectNameRequiredException):
            status = 400
        elif isinstance(exception, project_management_interface.ProjectAccessDeniedException):
            status = 403
        elif isinstance(exception, project_management_interface.ProjectNotFoundByIdException):
            status = 404
        elif isinstance(exception, project_management_interface.ProjectMemberAlreadyExistsException):
            status = 400
        elif isinstance(exception, project_management_interface.ProjectMemberNotFoundException):
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
class CreateProjectView(View):
    """View for creating a project."""
    
    def post(self, request):
        try:
            # Parse JSON body
            body = json.loads(request.body)
            
            # Create request DTO
            create_request = project_management_interface.CreateProjectRequest(**body)
            
            # Call usecase service
            project_service = bootstrapper.get_project_management_service()
            response = project_service.create_project(create_request)
            
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
class GetProjectView(View):
    """View for getting a single project."""
    
    def get(self, request, project_id):
        try:
            # Get user_id from query params (TODO: should come from authentication)
            user_id = int(request.GET.get('user_id', 0))
            
            # Create request DTO
            get_request = project_management_interface.GetProjectRequest(
                project_id=int(project_id),
                user_id=user_id
            )
            
            # Call usecase service
            project_service = bootstrapper.get_project_management_service()
            response = project_service.get_project_by_id(get_request)
            
            # Return JSON response
            return JsonResponse(response.model_dump(), status=200)
        except ValueError:
            return JsonResponse(
                {"error": {"message": "Invalid project_id or user_id", "code": "INVALID_ID"}},
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
class GetProjectsView(View):
    """View for getting projects with filters."""
    
    def get(self, request):
        try:
            # Get user_id from query params (TODO: should come from authentication)
            user_id = int(request.GET.get('user_id', 0))
            
            # Build request from query params
            request_data = {
                "user_id": user_id,
                "is_private": request.GET.get('is_private') == 'true' if request.GET.get('is_private') else None,
                "search": request.GET.get('search'),
                "order_by": request.GET.get('order_by', '-created_at'),
                "limit": int(request.GET.get('limit')) if request.GET.get('limit') else None,
                "offset": int(request.GET.get('offset')) if request.GET.get('offset') else None,
            }
            # Remove None values
            request_data = {k: v for k, v in request_data.items() if v is not None}
            
            # Create request DTO (ProjectFilter)
            project_filter = project_management_interface.ProjectFilter(**request_data)
            
            # Call usecase service
            project_service = bootstrapper.get_project_management_service()
            response = project_service.get_projects(project_filter)
            
            # Convert response to dict
            response_dict = {
                "projects": [project.model_dump() for project in response.projects],
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
class UpdateProjectView(View):
    """View for updating a project."""
    
    def put(self, request, project_id):
        try:
            # Parse JSON body
            body = json.loads(request.body)
            body['project_id'] = int(project_id)
            
            # Create request DTO
            update_request = project_management_interface.UpdateProjectRequest(**body)
            
            # Call usecase service
            project_service = bootstrapper.get_project_management_service()
            response = project_service.update_project(update_request)
            
            # Return JSON response
            return JsonResponse(response.model_dump(), status=200)
        except json.JSONDecodeError:
            return JsonResponse(
                {"error": {"message": "Invalid JSON", "code": "INVALID_JSON"}},
                status=400
            )
        except ValueError:
            return JsonResponse(
                {"error": {"message": "Invalid project_id", "code": "INVALID_ID"}},
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
class DeleteProjectView(View):
    """View for deleting a project."""
    
    def delete(self, request, project_id):
        try:
            # Get user_id from query params (TODO: should come from authentication)
            user_id = int(request.GET.get('user_id', 0))
            
            # Create request DTO
            delete_request = project_management_interface.DeleteProjectRequest(
                project_id=int(project_id),
                user_id=user_id
            )
            
            # Call usecase service
            project_service = bootstrapper.get_project_management_service()
            response = project_service.delete_project(delete_request)
            
            # Return JSON response
            return JsonResponse(response.model_dump(), status=200)
        except ValueError:
            return JsonResponse(
                {"error": {"message": "Invalid project_id or user_id", "code": "INVALID_ID"}},
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
class AddMemberView(View):
    """View for adding a member to a project."""
    
    def post(self, request, project_id):
        try:
            # Parse JSON body
            body = json.loads(request.body)
            body['project_id'] = int(project_id)
            
            # Create request DTO
            add_request = project_management_interface.AddMemberRequest(**body)
            
            # Call usecase service
            project_service = bootstrapper.get_project_management_service()
            response = project_service.add_member(add_request)
            
            # Return JSON response
            return JsonResponse(response.model_dump(), status=201)
        except json.JSONDecodeError:
            return JsonResponse(
                {"error": {"message": "Invalid JSON", "code": "INVALID_JSON"}},
                status=400
            )
        except ValueError:
            return JsonResponse(
                {"error": {"message": "Invalid project_id", "code": "INVALID_ID"}},
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
class RemoveMemberView(View):
    """View for removing a member from a project."""
    
    def delete(self, request, project_id):
        try:
            # Parse JSON body or get from query params
            if request.body:
                body = json.loads(request.body)
            else:
                body = {}
            body['project_id'] = int(project_id)
            
            # Get remove_user_id from body or query params
            if 'remove_user_id' not in body:
                body['remove_user_id'] = int(request.GET.get('remove_user_id', 0))
            
            # Create request DTO
            remove_request = project_management_interface.RemoveMemberRequest(**body)
            
            # Call usecase service
            project_service = bootstrapper.get_project_management_service()
            response = project_service.remove_member(remove_request)
            
            # Return JSON response
            return JsonResponse(response.model_dump(), status=200)
        except json.JSONDecodeError:
            return JsonResponse(
                {"error": {"message": "Invalid JSON", "code": "INVALID_JSON"}},
                status=400
            )
        except ValueError:
            return JsonResponse(
                {"error": {"message": "Invalid project_id or remove_user_id", "code": "INVALID_ID"}},
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
class UpdateMemberRoleView(View):
    """View for updating a member's role in a project."""
    
    def put(self, request, project_id):
        try:
            # Parse JSON body
            body = json.loads(request.body)
            body['project_id'] = int(project_id)
            
            # Create request DTO
            update_request = project_management_interface.UpdateMemberRoleRequest(**body)
            
            # Call usecase service
            project_service = bootstrapper.get_project_management_service()
            response = project_service.update_member_role(update_request)
            
            # Return JSON response
            return JsonResponse(response.model_dump(), status=200)
        except json.JSONDecodeError:
            return JsonResponse(
                {"error": {"message": "Invalid JSON", "code": "INVALID_JSON"}},
                status=400
            )
        except ValueError:
            return JsonResponse(
                {"error": {"message": "Invalid project_id", "code": "INVALID_ID"}},
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

