# Standard library
from abc import ABC, abstractmethod

# Internal - from same interface module (direct import, no interface. prefix needed)
from .dataclasses import SendSMSRequest, SendSMSResponse


class AbstractSMSService(ABC):
    """Interface for SMS service operations."""
    
    @abstractmethod
    def send_sms(self, request: SendSMSRequest) -> SendSMSResponse:
        """
        Send an SMS.
        
        Args:
            request: SendSMSRequest with recipient phone number and message
            
        Returns:
            SendSMSResponse with success status and message ID
            
        Raises:
            SMSSendFailedException: If SMS sending fails
        """
        pass

