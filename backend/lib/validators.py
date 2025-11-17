# Standard library
import re

# Third-party
from pydantic import field_validator
from pydantic_core import PydanticCustomError

# Internal
# (none needed)


def validate_email(email: str) -> str:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise PydanticCustomError('value_error', 'Invalid email format')
    return email


def validate_phone(phone: str) -> str:
    """Validate phone number format (basic validation)."""
    # Remove common separators
    cleaned = re.sub(r'[\s\-\(\)]', '', phone)
    # Check if it's digits only and reasonable length
    if not cleaned.isdigit() or len(cleaned) < 10 or len(cleaned) > 15:
        raise PydanticCustomError('value_error', 'Invalid phone number format')
    return phone


def validate_password_strength(password: str) -> str:
    """Validate password strength (minimum 8 characters, at least one letter and one number)."""
    if len(password) < 8:
        raise PydanticCustomError('value_error', 'Password must be at least 8 characters long')
    if not re.search(r'[a-zA-Z]', password):
        raise PydanticCustomError('value_error', 'Password must contain at least one letter')
    if not re.search(r'\d', password):
        raise PydanticCustomError('value_error', 'Password must contain at least one number')
    return password

