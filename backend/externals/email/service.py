# Standard library
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Third-party
# (none needed)

# Internal - from other modules
from django.conf import settings

# Internal - from same module
from . import interface

logger = logging.getLogger(__name__)


class EmailService(interface.AbstractEmailService):
    """Basic email service implementation using SMTP."""
    
    def __init__(self):
        # Email configuration (can be moved to settings)
        self.smtp_host = getattr(settings, 'EMAIL_HOST', 'smtp.gmail.com')
        self.smtp_port = getattr(settings, 'EMAIL_PORT', 587)
        self.smtp_user = getattr(settings, 'EMAIL_HOST_USER', '')
        self.smtp_password = getattr(settings, 'EMAIL_HOST_PASSWORD', '')
        self.from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', self.smtp_user)
        self.use_tls = getattr(settings, 'EMAIL_USE_TLS', True)
    
    def send_email(self, request: interface.SendEmailRequest) -> interface.SendEmailResponse:
        logger.info(f"Sending email to: {request.to_email}", extra={"input": request.model_dump()})
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = request.subject
            msg['From'] = request.from_email or self.from_email
            msg['To'] = request.to_email
            
            # Add text and HTML parts
            text_part = MIMEText(request.body, 'plain')
            msg.attach(text_part)
            
            if request.html_body:
                html_part = MIMEText(request.html_body, 'html')
                msg.attach(html_part)
            
            # Send email via SMTP
            if not self.smtp_user or not self.smtp_password:
                logger.warning("Email credentials not configured, skipping email send")
                # In development, just log the email
                logger.info(f"Email would be sent: To={request.to_email}, Subject={request.subject}")
                response = interface.SendEmailResponse(
                    success=True,
                    message_id="dev_mode",
                    message="Email logged (SMTP not configured)"
                )
                logger.info(f"Email logged successfully", extra={"output": response.model_dump()})
                return response
            
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            response = interface.SendEmailResponse(
                success=True,
                message_id=f"email_{request.to_email}",
                message="Email sent successfully"
            )
            
            logger.info(f"Email sent successfully to: {request.to_email}", extra={"output": response.model_dump()})
            return response
            
        except Exception as e:
            logger.exception(f"Failed to send email to {request.to_email}")
            raise interface.EmailSendFailedException(str(e))

