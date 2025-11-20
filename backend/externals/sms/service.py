# Standard library
import logging

# Third-party
# (none needed)

# Internal - from other modules
# (none needed)

# Internal - from same module
from . import interface

logger = logging.getLogger(__name__)


class SMSService(interface.AbstractSMSService):
    """Basic SMS service implementation (placeholder - can be integrated with SMS gateway)."""
    
    def send_sms(self, request: interface.SendSMSRequest) -> interface.SendSMSResponse:
        logger.info(f"Sending SMS to: {request.to_phone}", extra={"input": request.model_dump()})
        
        try:
            # TODO: Integrate with actual SMS gateway (Twilio, AWS SNS, etc.)
            # For now, just log the SMS
            logger.info(f"SMS would be sent: To={request.to_phone}, Message={request.message[:50]}...")
            
            # In a real implementation, you would:
            # 1. Call SMS gateway API
            # 2. Handle errors
            # 3. Return actual message ID
            
            response = interface.SendSMSResponse(
                success=True,
                message_id=f"sms_{request.to_phone}",
                message="SMS logged (SMS gateway not configured)"
            )
            
            logger.info(f"SMS logged successfully", extra={"output": response.model_dump()})
            return response
            
        except Exception as e:
            logger.exception(f"Failed to send SMS to {request.to_phone}")
            raise interface.SMSSendFailedException(str(e))

