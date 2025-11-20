# Standard library
import logging

# Third-party
# (none needed)

# Internal - from other modules
from repository.reminder import interface as reminder_repository_interface
from repository.user import interface as user_repository_interface
from externals.email import interface as email_interface
from externals.sms import interface as sms_interface
from utils.date_utils import interface as date_utils_interface

# Internal - from same module
from . import interface

logger = logging.getLogger(__name__)


def _repo_dto_to_usecase_dto(repo_dto: reminder_repository_interface.ReminderDTO) -> interface.ReminderDTO:
    """Simple converter: Repository ReminderDTO to UseCase ReminderDTO."""
    return interface.ReminderDTO(
        reminder_id=repo_dto.reminder_id,
        title=repo_dto.title,
        message=repo_dto.message,
        reminder_time=repo_dto.reminder_time,
        sent_at=repo_dto.sent_at,
        notification_channels=repo_dto.notification_channels,
        todo_id=repo_dto.todo_id,
        user_id=repo_dto.user_id,
        reminder_type=repo_dto.reminder_type,
        status=repo_dto.status,
        created_at=repo_dto.created_at,
        updated_at=repo_dto.updated_at
    )


class ReminderManagementService(interface.AbstractReminderManagementService):
    """Service for managing reminder operations."""
    
    def __init__(
        self,
        reminder_repo: reminder_repository_interface.AbstractReminderRepository,
        user_repo: user_repository_interface.AbstractUserRepository,
        email_service: email_interface.AbstractEmailService,
        sms_service: sms_interface.AbstractSMSService,
        date_time_service: date_utils_interface.AbstractDateTimeService,
    ):
        self.reminder_repo = reminder_repo
        self.user_repo = user_repo
        self.email_service = email_service
        self.sms_service = sms_service
        self.date_time_service = date_time_service
    
    def create_reminder(self, request: interface.CreateReminderRequest) -> interface.CreateReminderResponse:
        logger.info(f"Creating reminder: {request.title}", extra={"input": request.model_dump()})
        
        if not request.title:
            logger.warning("Reminder creation failed - title is required")
            raise interface.ReminderTitleRequiredException()
        
        # Calculate timestamps
        now_dto = self.date_time_service.now()
        
        # Create reminder
        reminder_create_request = reminder_repository_interface.ReminderCreateRequest(
            title=request.title,
            message=request.message or "",
            reminder_time=request.reminder_time,
            notification_channels=request.notification_channels or ['Email'],
            todo_id=request.todo_id,
            user_id=request.user_id,
            reminder_type=request.reminder_type,
            status='Pending',
            created_at=now_dto.timestamp_ms,
            updated_at=now_dto.timestamp_ms,
            sent_at=None
        )
        
        reminder_dto = self.reminder_repo.create(reminder_create_request)
        
        response = interface.CreateReminderResponse(
            reminder_id=reminder_dto.reminder_id,
            title=reminder_dto.title,
            reminder_time=reminder_dto.reminder_time,
            status=reminder_dto.status,
            created_at=reminder_dto.created_at
        )
        
        logger.info(f"Reminder created successfully: {response.reminder_id}", extra={"output": response.model_dump()})
        return response
    
    def update_reminder(self, request: interface.UpdateReminderRequest) -> interface.UpdateReminderResponse:
        logger.info(f"Updating reminder: {request.reminder_id}", extra={"input": request.model_dump()})
        
        # Verify reminder exists and user has access
        reminder_dto = self.reminder_repo.get_by_id(request.reminder_id)
        if not reminder_dto:
            logger.warning(f"Reminder not found: {request.reminder_id}")
            raise interface.ReminderNotFoundByIdException(request.reminder_id)
        
        if reminder_dto.user_id != request.user_id:
            logger.warning(f"Access denied - user {request.user_id} tried to update reminder {request.reminder_id}")
            raise interface.ReminderAccessDeniedException(request.reminder_id, request.user_id)
        
        # Calculate timestamps
        now_dto = self.date_time_service.now()
        
        # Update reminder
        reminder_update_request = reminder_repository_interface.ReminderUpdateRequest(
            title=request.title,
            message=request.message,
            reminder_time=request.reminder_time,
            notification_channels=request.notification_channels,
            status=request.status,
            updated_at=now_dto.timestamp_ms
        )
        
        updated_reminder_dto = self.reminder_repo.update(request.reminder_id, reminder_update_request)
        
        response = interface.UpdateReminderResponse(
            reminder_id=updated_reminder_dto.reminder_id,
            title=updated_reminder_dto.title,
            reminder_time=updated_reminder_dto.reminder_time,
            status=updated_reminder_dto.status,
            updated_at=updated_reminder_dto.updated_at
        )
        
        logger.info(f"Reminder updated successfully: {request.reminder_id}", extra={"output": response.model_dump()})
        return response
    
    def delete_reminder(self, request: interface.DeleteReminderRequest) -> interface.DeleteReminderResponse:
        logger.info(f"Deleting reminder: {request.reminder_id}", extra={"input": request.model_dump()})
        
        # Verify reminder exists and user has access
        reminder_dto = self.reminder_repo.get_by_id(request.reminder_id)
        if not reminder_dto:
            logger.warning(f"Reminder not found: {request.reminder_id}")
            raise interface.ReminderNotFoundByIdException(request.reminder_id)
        
        if reminder_dto.user_id != request.user_id:
            logger.warning(f"Access denied - user {request.user_id} tried to delete reminder {request.reminder_id}")
            raise interface.ReminderAccessDeniedException(request.reminder_id, request.user_id)
        
        # Delete reminder
        self.reminder_repo.delete(request.reminder_id)
        
        response = interface.DeleteReminderResponse(
            success=True,
            message=f"Reminder {request.reminder_id} deleted successfully"
        )
        
        logger.info(f"Reminder deleted successfully: {request.reminder_id}", extra={"output": response.model_dump()})
        return response
    
    def process_reminders(self, request: interface.ProcessRemindersRequest) -> interface.ProcessRemindersResponse:
        logger.info(f"Processing reminders at time: {request.current_time}", extra={"input": request.model_dump()})
        
        # Find pending reminders that should be sent
        reminder_filter = reminder_repository_interface.ReminderFilter(
            status='Pending',
            reminder_time__lte=request.current_time,
            limit=request.max_reminders,
            order_by='reminder_time'
        )
        
        reminders = self.reminder_repo.get_reminders(reminder_filter)
        
        sent_count = 0
        failed_count = 0
        
        now_dto = self.date_time_service.now()
        
        for reminder_dto in reminders:
            try:
                # Get user for notification
                user_dto = self.user_repo.get_by_id(reminder_dto.user_id)
                if not user_dto:
                    logger.warning(f"User not found for reminder {reminder_dto.reminder_id}")
                    failed_count += 1
                    continue
                
                # Send notifications via requested channels
                success = False
                for channel in reminder_dto.notification_channels:
                    try:
                        if channel == 'Email' and user_dto.email:
                            email_request = email_interface.SendEmailRequest(
                                to_email=user_dto.email,
                                subject=reminder_dto.title,
                                body=reminder_dto.message
                            )
                            self.email_service.send_email(email_request)
                            success = True
                        elif channel == 'SMS' and user_dto.phone:
                            sms_request = sms_interface.SendSMSRequest(
                                to_phone=user_dto.phone,
                                message=f"{reminder_dto.title}: {reminder_dto.message}"
                            )
                            self.sms_service.send_sms(sms_request)
                            success = True
                        # TODO: Add Telegram, Bale, Eitaa channels
                    except Exception as e:
                        logger.exception(f"Failed to send {channel} notification for reminder {reminder_dto.reminder_id}")
                
                if success:
                    # Update reminder status
                    reminder_update_request = reminder_repository_interface.ReminderUpdateRequest(
                        status='Sent',
                        sent_at=now_dto.timestamp_ms,
                        updated_at=now_dto.timestamp_ms
                    )
                    self.reminder_repo.update(reminder_dto.reminder_id, reminder_update_request)
                    sent_count += 1
                else:
                    # Mark as failed if no channels succeeded
                    reminder_update_request = reminder_repository_interface.ReminderUpdateRequest(
                        status='Failed',
                        updated_at=now_dto.timestamp_ms
                    )
                    self.reminder_repo.update(reminder_dto.reminder_id, reminder_update_request)
                    failed_count += 1
                    
            except Exception as e:
                logger.exception(f"Error processing reminder {reminder_dto.reminder_id}")
                failed_count += 1
        
        response = interface.ProcessRemindersResponse(
            processed_count=len(reminders),
            sent_count=sent_count,
            failed_count=failed_count,
            message=f"Processed {len(reminders)} reminders: {sent_count} sent, {failed_count} failed"
        )
        
        logger.info(f"Reminder processing completed: {sent_count} sent, {failed_count} failed", 
                   extra={"output": response.model_dump()})
        return response
    
    def get_reminders(self, request: interface.GetRemindersRequest) -> interface.GetRemindersResponse:
        logger.info(f"Getting reminders for user: {request.user_id}", extra={"input": request.model_dump()})
        
        # Get reminders
        reminder_filter = reminder_repository_interface.ReminderFilter(
            user_id=request.user_id,
            todo_id=request.todo_id,
            status=request.status,
            reminder_type=request.reminder_type,
            order_by='reminder_time'
        )
        reminder_dtos = self.reminder_repo.get_reminders(reminder_filter)
        
        # Convert to usecase DTOs
        reminders = [_repo_dto_to_usecase_dto(dto) for dto in reminder_dtos]
        
        response = interface.GetRemindersResponse(
            reminders=reminders,
            total=len(reminders)
        )
        
        logger.info(f"Found {len(reminders)} reminders for user: {request.user_id}", 
                   extra={"output": {"count": len(reminders)}})
        return response

