# Standard library
import logging

# Third-party
# (none needed)

# Internal - from other modules
# (none needed)

# Internal - from same module
from .models import Reminder
from . import interface

logger = logging.getLogger(__name__)


class ReminderRepositoryService(interface.AbstractReminderRepository):
    """Repository service for reminder data access."""
    
    def create(self, reminder_data: interface.ReminderCreateRequest) -> interface.ReminderDTO:
        logger.info(f"Creating reminder with title: {reminder_data.title}", extra={"input": reminder_data.model_dump()})
        
        if not reminder_data.title:
            logger.warning("Failed to create reminder - title is required")
            raise interface.ReminderTitleRequiredException()
        
        reminder = Reminder()
        reminder.title = reminder_data.title
        reminder.message = reminder_data.message or ""
        reminder.reminder_time = reminder_data.reminder_time
        reminder.notification_channels = reminder_data.notification_channels or ['Email']
        reminder.todo_id = reminder_data.todo_id
        reminder.user_id = reminder_data.user_id
        reminder.reminder_type = reminder_data.reminder_type
        reminder.status = reminder_data.status
        reminder.created_at = reminder_data.created_at
        reminder.updated_at = reminder_data.updated_at
        reminder.sent_at = reminder_data.sent_at
        
        reminder.save()
        
        result = interface.ReminderDTO.from_model(reminder)
        logger.info(f"Reminder created successfully: {result.reminder_id}", extra={"output": result.model_dump()})
        return result
    
    def get_by_id(self, reminder_id: int) -> interface.ReminderDTO | None:
        logger.info(f"Fetching reminder by id: {reminder_id}", extra={"input": {"reminder_id": reminder_id}})
        
        try:
            reminder = Reminder.objects.get(id=reminder_id)
            result = interface.ReminderDTO.from_model(reminder)
            logger.info(f"Reminder fetched successfully: {reminder_id}", extra={"output": result.model_dump()})
            return result
        except Reminder.DoesNotExist:
            logger.info(f"Reminder not found: {reminder_id}")
            return None
    
    def get_reminders(self, filters: interface.ReminderFilter) -> list[interface.ReminderDTO]:
        logger.info(f"Filtering reminders", extra={"input": filters.model_dump()})
        
        queryset = Reminder.objects.all()
        
        # Apply basic filters
        if filters.user_id:
            queryset = queryset.filter(user_id=filters.user_id)
        if filters.todo_id:
            queryset = queryset.filter(todo_id=filters.todo_id)
        if filters.status:
            queryset = queryset.filter(status=filters.status)
        if filters.reminder_type:
            queryset = queryset.filter(reminder_type=filters.reminder_type)
        if filters.reminder_time__gte:
            queryset = queryset.filter(reminder_time__gte=filters.reminder_time__gte)
        if filters.reminder_time__lte:
            queryset = queryset.filter(reminder_time__lte=filters.reminder_time__lte)
        
        # Apply ordering
        queryset = queryset.order_by(filters.order_by)
        
        # Apply pagination
        if filters.offset is not None and filters.limit is not None:
            queryset = queryset[filters.offset:filters.offset + filters.limit]
        
        results = [interface.ReminderDTO.from_model(reminder) for reminder in queryset]
        logger.info(f"Found {len(results)} reminders matching filter", extra={"output": {"count": len(results)}})
        return results
    
    def update(self, reminder_id: int, reminder_data: interface.ReminderUpdateRequest) -> interface.ReminderDTO:
        logger.info(f"Updating reminder: {reminder_id}", extra={"input": {"reminder_id": reminder_id}})
        
        try:
            reminder = Reminder.objects.get(id=reminder_id)
        except Reminder.DoesNotExist:
            logger.warning(f"Reminder not found for update: {reminder_id}")
            raise interface.ReminderNotFoundByIdException(reminder_id)
        
        # Update fields if provided
        if reminder_data.title is not None:
            reminder.title = reminder_data.title
        if reminder_data.message is not None:
            reminder.message = reminder_data.message
        if reminder_data.reminder_time is not None:
            reminder.reminder_time = reminder_data.reminder_time
        if reminder_data.notification_channels is not None:
            reminder.notification_channels = reminder_data.notification_channels
        if reminder_data.status is not None:
            reminder.status = reminder_data.status
        if reminder_data.sent_at is not None:
            reminder.sent_at = reminder_data.sent_at
        # Updated timestamp is provided by usecase layer
        if reminder_data.updated_at:
            reminder.updated_at = reminder_data.updated_at
        
        reminder.save()
        
        result = interface.ReminderDTO.from_model(reminder)
        logger.info(f"Reminder updated successfully: {reminder_id}", extra={"output": result.model_dump()})
        return result
    
    def delete(self, reminder_id: int) -> None:
        logger.info(f"Deleting reminder: {reminder_id}", extra={"input": {"reminder_id": reminder_id}})
        
        try:
            reminder = Reminder.objects.get(id=reminder_id)
            reminder.delete()
            logger.info(f"Reminder deleted successfully: {reminder_id}")
        except Reminder.DoesNotExist:
            logger.warning(f"Reminder not found for deletion: {reminder_id}")
            raise interface.ReminderNotFoundByIdException(reminder_id)

