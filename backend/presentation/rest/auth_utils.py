# Standard library
import logging
import hashlib

# Third-party
from django.http import JsonResponse

# Internal - from other modules
from runner.bootstrap import bootstrapper

logger = logging.getLogger(__name__)

# In-memory token storage (for development)
# In production, use Redis or database
_token_storage = {}


def store_token(token: str, user_id: int):
    """Store token with user_id mapping."""
    _token_storage[token] = user_id


def get_user_from_token(request) -> int | None:
    """
    Extract user_id from Authorization token in request headers.
    
    Returns:
        user_id if token is valid, None otherwise
    """
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    
    if not auth_header.startswith('Bearer '):
        return None
    
    token = auth_header.replace('Bearer ', '').strip()
    
    if not token:
        return None
    
    # Check token storage
    user_id = _token_storage.get(token)
    if user_id:
        return user_id
    
    # If not found in storage, return None (token invalid or expired)
    return None


def require_auth(view_func):
    """
    Decorator to require authentication for a view.
    Extracts user_id from token and adds it to request.user_id
    """
    def wrapper(request, *args, **kwargs):
        user_id = get_user_from_token(request)
        
        if user_id is None:
            return JsonResponse(
                {"error": {"message": "Authentication required", "code": "AUTHENTICATION_REQUIRED"}},
                status=401
            )
        
        # Add user_id to request object
        request.user_id = user_id
        return view_func(request, *args, **kwargs)
    
    return wrapper
