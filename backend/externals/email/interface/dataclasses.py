# Standard library
from typing import Optional, List

# Third-party
# (none needed)

# Internal - from other modules
from lib.base_models import BaseRequest, BaseResponse

# Internal - from same interface module
# (none needed)


class SendEmailRequest(BaseRequest):
    """Request DTO for sending an email."""
    to_email: str
    subject: str
    body: str
    html_body: Optional[str] = None
    from_email: Optional[str] = None  # Default from settings


class SendEmailResponse(BaseResponse):
    """Response DTO for sending an email."""
    success: bool
    message_id: Optional[str] = None
    message: str

