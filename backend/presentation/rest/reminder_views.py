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
from usecase.reminder_management import interface as reminder_management_interface
from lib.exceptions import BaseRootException

# Internal - from same module
# (none needed)

logger = logging.getLogger(__name__)


def handle_exception(exception: Exception) -> JsonResponse:
    """Convert exceptions to appropriate JSON responses."""
    if isinstance(exception, BaseRootException):
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
class CreateReminderView(View):
    """View for creating a reminder."""
    
    def post(self, request):
        try:
            body = json.loads(request.body)
            create_request = reminder_management_interface.CreateReminderRequest(**body)
            reminder_service = bootstrapper.get_reminder_management_service()
            response = reminder_service.create_reminder(create_request)
            return JsonResponse(response.model_dump(), status=201)
        except json.JSONDecodeError:
            return JsonResponse(
                {"error": {"message": "Invalid JSON", "code": "INVALID_JSON"}},
                status=400
            )
        except Exception as e:
            if isinstance(e, BaseRootException):
                return handle_exception(e)
            if hasattr(e, 'errors'):
                return JsonResponse(
                    {"error": {"message": "Validation error", "code": "VALIDATION_ERROR", "details": e.errors()}},
                    status=400
                )
            return handle_exception(e)


@method_decorator(csrf_exempt, name='dispatch')
class UpdateReminderView(View):
    """View for updating a reminder."""
    
    def put(self, request, reminder_id):
        try:
            body = json.loads(request.body)
            body['reminder_id'] = int(reminder_id)
            update_request = reminder_management_interface.UpdateReminderRequest(**body)
            reminder_service = bootstrapper.get_reminder_management_service()
            response = reminder_service.update_reminder(update_request)
            return JsonResponse(response.model_dump(), status=200)
        except (json.JSONDecodeError, ValueError):
            return JsonResponse(
                {"error": {"message": "Invalid JSON or reminder_id", "code": "INVALID_INPUT"}},
                status=400
            )
        except Exception as e:
            if isinstance(e, BaseRootException):
                return handle_exception(e)
            if hasattr(e, 'errors'):
                return JsonResponse(
                    {"error": {"message": "Validation error", "code": "VALIDATION_ERROR", "details": e.errors()}},
                    status=400
                )
            return handle_exception(e)


@method_decorator(csrf_exempt, name='dispatch')
class DeleteReminderView(View):
    """View for deleting a reminder."""
    
    def delete(self, request, reminder_id):
        try:
            user_id = int(request.GET.get('user_id', 0))
            delete_request = reminder_management_interface.DeleteReminderRequest(
                reminder_id=int(reminder_id),
                user_id=user_id
            )
            reminder_service = bootstrapper.get_reminder_management_service()
            response = reminder_service.delete_reminder(delete_request)
            return JsonResponse(response.model_dump(), status=200)
        except ValueError:
            return JsonResponse(
                {"error": {"message": "Invalid reminder_id or user_id", "code": "INVALID_ID"}},
                status=400
            )
        except Exception as e:
            if isinstance(e, BaseRootException):
                return handle_exception(e)
            return handle_exception(e)


@method_decorator(csrf_exempt, name='dispatch')
class GetRemindersView(View):
    """View for getting reminders."""
    
    def get(self, request):
        try:
            user_id = int(request.GET.get('user_id', 0))
            todo_id = int(request.GET.get('todo_id')) if request.GET.get('todo_id') else None
            status = request.GET.get('status')
            reminder_type = request.GET.get('reminder_type')
            
            get_request = reminder_management_interface.GetRemindersRequest(
                user_id=user_id,
                todo_id=todo_id,
                status=status,
                reminder_type=reminder_type
            )
            reminder_service = bootstrapper.get_reminder_management_service()
            response = reminder_service.get_reminders(get_request)
            
            response_dict = {
                "reminders": [r.model_dump() for r in response.reminders],
                "total": response.total
            }
            return JsonResponse(response_dict, status=200)
        except ValueError:
            return JsonResponse(
                {"error": {"message": "Invalid user_id or filter parameters", "code": "INVALID_PARAMETERS"}},
                status=400
            )
        except Exception as e:
            if isinstance(e, BaseRootException):
                return handle_exception(e)
            return handle_exception(e)


@method_decorator(csrf_exempt, name='dispatch')
class ProcessRemindersView(View):
    """View for processing reminders (scheduled task endpoint)."""
    
    def post(self, request):
        try:
            body = json.loads(request.body) if request.body else {}
            # Get current time from request or use current timestamp
            from utils.date_utils.service import DateTimeService
            date_time_service = DateTimeService()
            current_time_dto = date_time_service.now()
            
            process_request = reminder_management_interface.ProcessRemindersRequest(
                current_time=body.get('current_time', current_time_dto.timestamp_ms),
                max_reminders=body.get('max_reminders', 100)
            )
            reminder_service = bootstrapper.get_reminder_management_service()
            response = reminder_service.process_reminders(process_request)
            return JsonResponse(response.model_dump(), status=200)
        except json.JSONDecodeError:
            return JsonResponse(
                {"error": {"message": "Invalid JSON", "code": "INVALID_JSON"}},
                status=400
            )
        except Exception as e:
            if isinstance(e, BaseRootException):
                return handle_exception(e)
            return handle_exception(e)

