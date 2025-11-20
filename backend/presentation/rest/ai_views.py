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
from usecase.smart_todo_management import interface as smart_todo_management_interface
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
class AnalyzeTextView(View):
    """View for analyzing free text."""
    
    def post(self, request):
        try:
            body = json.loads(request.body)
            analyze_request = smart_todo_management_interface.AnalyzeFreeTextRequest(**body)
            smart_service = bootstrapper.get_smart_todo_management_service()
            response = smart_service.analyze_free_text(analyze_request)
            
            response_dict = {
                "suggestions": [s.model_dump() for s in response.suggestions],
                "detected_intent": response.detected_intent,
                "confidence": response.confidence
            }
            return JsonResponse(response_dict, status=200)
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
class CreateSmartTodoView(View):
    """View for creating a smart todo from AI suggestion."""
    
    def post(self, request):
        try:
            body = json.loads(request.body)
            create_request = smart_todo_management_interface.CreateSmartTodoRequest(**body)
            smart_service = bootstrapper.get_smart_todo_management_service()
            response = smart_service.create_smart_todo(create_request)
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
class AutoCategorizeView(View):
    """View for auto-categorizing a todo."""
    
    def post(self, request):
        try:
            body = json.loads(request.body)
            categorize_request = smart_todo_management_interface.AutoCategorizeRequest(**body)
            smart_service = bootstrapper.get_smart_todo_management_service()
            response = smart_service.auto_categorize(categorize_request)
            return JsonResponse(response.model_dump(), status=200)
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
class SuggestSubtasksView(View):
    """View for suggesting subtasks."""
    
    def post(self, request):
        try:
            body = json.loads(request.body)
            suggest_request = smart_todo_management_interface.SuggestSubtasksRequest(**body)
            smart_service = bootstrapper.get_smart_todo_management_service()
            response = smart_service.suggest_subtasks(suggest_request)
            return JsonResponse(response.model_dump(), status=200)
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
class SuggestNextActionView(View):
    """View for suggesting next action."""
    
    def post(self, request):
        try:
            body = json.loads(request.body)
            suggest_request = smart_todo_management_interface.SuggestNextActionRequest(**body)
            smart_service = bootstrapper.get_smart_todo_management_service()
            response = smart_service.suggest_next_action(suggest_request)
            return JsonResponse(response.model_dump(), status=200)
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
class ConversationalQueryView(View):
    """View for conversational queries."""
    
    def post(self, request):
        try:
            body = json.loads(request.body)
            query_request = smart_todo_management_interface.ConversationalQueryRequest(**body)
            smart_service = bootstrapper.get_smart_todo_management_service()
            response = smart_service.conversational_query(query_request)
            
            response_dict = {
                "response": response.response,
                "suggestions": [s.model_dump() for s in response.suggestions],
                "detected_intent": response.detected_intent,
                "confidence": response.confidence
            }
            return JsonResponse(response_dict, status=200)
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

