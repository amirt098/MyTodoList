# Standard library
from typing import Optional

# Third-party
# (none needed)

# Internal - from other modules
from lib.base_models import BaseRequest, BaseResponse

# Internal - from same interface module
# (none needed)


class SendSMSRequest(BaseRequest):
    """Request DTO for sending an SMS."""
    to_phone: str
    message: str
    from_phone: Optional[str] = None  # Default from settings


class SendSMSResponse(BaseResponse):
    """Response DTO for sending an SMS."""
    success: bool
    message_id: Optional[str] = None
    message: str

