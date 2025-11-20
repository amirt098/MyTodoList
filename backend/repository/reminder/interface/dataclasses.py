# Standard library
from typing import Optional, List

# Third-party
# (none needed)

# Internal - from other modules
from lib.base_models import BaseModel, BaseFilter

# Internal - from same interface module
# (none needed)


class ReminderCreateRequest(BaseModel):
    """Request for creating a reminder."""
    title: str
    message: Optional[str] = None
    reminder_time: int  # Timestamp when reminder should be sent
    notification_channels: List[str] = ['Email']  # Default to Email
    todo_id: Optional[int] = None
    user_id: int
    reminder_type: str = 'Manual'
    status: str = 'Pending'
    created_at: int | None = None
    updated_at: int | None = None
    sent_at: Optional[int] = None


class ReminderUpdateRequest(BaseModel):
    """Request for updating a reminder."""
    title: str | None = None
    message: str | None = None
    reminder_time: int | None = None
    notification_channels: List[str] | None = None
    status: str | None = None
    sent_at: Optional[int] = None
    updated_at: int | None = None


class ReminderDTO(BaseModel):
    """DTO for Reminder responses."""
    reminder_id: int
    title: str
    message: str
    reminder_time: int
    sent_at: Optional[int] = None
    notification_channels: List[str]
    todo_id: Optional[int] = None
    user_id: int
    reminder_type: str
    status: str
    created_at: int
    updated_at: int
    
    @classmethod
    def from_model(cls, reminder) -> 'ReminderDTO':
        """Create ReminderDTO from Django Reminder model."""
        return cls(
            reminder_id=reminder.id,
            title=reminder.title,
            message=reminder.message or "",
            reminder_time=reminder.reminder_time,
            sent_at=reminder.sent_at,
            notification_channels=reminder.notification_channels if reminder.notification_channels else [],
            todo_id=reminder.todo_id,
            user_id=reminder.user_id,
            reminder_type=reminder.reminder_type,
            status=reminder.status,
            created_at=reminder.created_at,
            updated_at=reminder.updated_at
        )


class ReminderFilter(BaseFilter):
    """Filter for querying reminders."""
    user_id: Optional[int] = None
    todo_id: Optional[int] = None
    status: Optional[str] = None
    reminder_type: Optional[str] = None
    reminder_time__gte: Optional[int] = None  # For finding reminders to process
    reminder_time__lte: Optional[int] = None

