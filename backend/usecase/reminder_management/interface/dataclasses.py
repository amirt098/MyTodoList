# Standard library
from typing import Optional, List

# Third-party
# (none needed)

# Internal - from other modules
from lib.base_models import BaseRequest, BaseResponse

# Internal - from same interface module
# (none needed)


class ReminderDTO(BaseResponse):
    """Pydantic DTO for Reminder."""
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


class CreateReminderRequest(BaseRequest):
    """Request DTO for creating a reminder."""
    title: str
    message: Optional[str] = None
    reminder_time: int  # Timestamp when reminder should be sent
    notification_channels: List[str] = ['Email']
    todo_id: Optional[int] = None
    user_id: int
    reminder_type: str = 'Manual'


class CreateReminderResponse(BaseResponse):
    """Response DTO for creating a reminder."""
    reminder_id: int
    title: str
    reminder_time: int
    status: str
    created_at: int


class UpdateReminderRequest(BaseRequest):
    """Request DTO for updating a reminder."""
    reminder_id: int
    user_id: int  # For access control
    title: Optional[str] = None
    message: Optional[str] = None
    reminder_time: Optional[int] = None
    notification_channels: Optional[List[str]] = None
    status: Optional[str] = None


class UpdateReminderResponse(BaseResponse):
    """Response DTO for updating a reminder."""
    reminder_id: int
    title: str
    reminder_time: int
    status: str
    updated_at: int


class DeleteReminderRequest(BaseRequest):
    """Request DTO for deleting a reminder."""
    reminder_id: int
    user_id: int  # For access control


class DeleteReminderResponse(BaseResponse):
    """Response DTO for deleting a reminder."""
    success: bool
    message: str


class ProcessRemindersRequest(BaseRequest):
    """Request DTO for processing reminders (scheduled task)."""
    current_time: int  # Current timestamp
    max_reminders: Optional[int] = 100  # Limit number of reminders to process


class ProcessRemindersResponse(BaseResponse):
    """Response DTO for processing reminders."""
    processed_count: int
    sent_count: int
    failed_count: int
    message: str


class GetRemindersRequest(BaseRequest):
    """Request DTO for getting reminders."""
    user_id: int
    todo_id: Optional[int] = None
    status: Optional[str] = None
    reminder_type: Optional[str] = None


class GetRemindersResponse(BaseResponse):
    """Response DTO for getting reminders."""
    reminders: List[ReminderDTO]
    total: int

