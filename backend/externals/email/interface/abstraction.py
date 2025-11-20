# Standard library
from abc import ABC, abstractmethod

# Internal - from same interface module (direct import, no interface. prefix needed)
from .dataclasses import SendEmailRequest, SendEmailResponse


class AbstractEmailService(ABC):
    """Interface for email service operations."""
    
    @abstractmethod
    def send_email(self, request: SendEmailRequest) -> SendEmailResponse:
        """
        Send an email.
        
        Args:
            request: SendEmailRequest with recipient, subject, and body
            
        Returns:
            SendEmailResponse with success status and message ID
            
        Raises:
            EmailSendFailedException: If email sending fails
        """
        pass

