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
from usecase.user_management import interface as user_management_interface
from lib.exceptions import BaseRootException

# Internal - from same module
# (none needed)

logger = logging.getLogger(__name__)


def handle_exception(exception: Exception) -> JsonResponse:
    """Convert exceptions to appropriate JSON responses."""
    if isinstance(exception, BaseRootException):
        # Map exception types to HTTP status codes
        if isinstance(exception, user_management_interface.UserRegistrationEmailExistsException):
            status = 400
        elif isinstance(exception, user_management_interface.UserLoginInvalidCredentialsException):
            status = 401
        elif isinstance(exception, user_management_interface.UserLoginInactiveAccountException):
            status = 403
        elif isinstance(exception, user_management_interface.UserProfileNotFoundException):
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
class RegisterView(View):
    """View for user registration."""
    
    def post(self, request):
        try:
            # Parse JSON body
            body = json.loads(request.body)
            
            # Create request DTO
            register_request = user_management_interface.RegisterUserRequest(**body)
            
            # Call usecase service
            user_service = bootstrapper.get_user_management_service()
            response = user_service.register_user(register_request)
            
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
class LoginView(View):
    """View for user login."""
    
    def post(self, request):
        try:
            # Parse JSON body
            body = json.loads(request.body)
            
            # Create request DTO
            login_request = user_management_interface.LoginRequest(**body)
            
            # Call usecase service
            user_service = bootstrapper.get_user_management_service()
            response = user_service.login(login_request)
            
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
class PasswordRecoveryView(View):
    """View for password recovery."""
    
    def post(self, request):
        try:
            # Parse JSON body
            body = json.loads(request.body)
            
            # Create request DTO
            recovery_request = user_management_interface.PasswordRecoveryRequest(**body)
            
            # Call usecase service
            user_service = bootstrapper.get_user_management_service()
            response = user_service.password_recovery(recovery_request)
            
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
class UpdateProfileView(View):
    """View for updating user profile."""
    
    def put(self, request):
        try:
            # Parse JSON body
            body = json.loads(request.body)
            
            # Create request DTO
            update_request = user_management_interface.UpdateProfileRequest(**body)
            
            # Call usecase service
            user_service = bootstrapper.get_user_management_service()
            response = user_service.update_profile(update_request)
            
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


