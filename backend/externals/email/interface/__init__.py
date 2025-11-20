# Standard library
# (none needed)

# Third-party
# (none needed)

# Internal - from same interface module
from .abstraction import AbstractEmailService
from .dataclasses import (
    SendEmailRequest,
    SendEmailResponse
)
from .exceptions import (
    EmailBadRequestException,
    EmailInternalServerErrorException,
    EmailSendFailedException
)

__all__ = [
    # Abstractions
    'AbstractEmailService',
    # Dataclasses
    'SendEmailRequest',
    'SendEmailResponse',
    # Exceptions
    'EmailBadRequestException',
    'EmailInternalServerErrorException',
    'EmailSendFailedException',
]

