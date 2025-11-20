# Standard library
from abc import ABC, abstractmethod

# Internal - from same interface module (direct import, no interface. prefix needed)
from .dataclasses import (
    CreateReminderRequest, CreateReminderResponse,
    UpdateReminderRequest, UpdateReminderResponse,
    DeleteReminderRequest, DeleteReminderResponse,
    ProcessRemindersRequest, ProcessRemindersResponse,
    GetRemindersRequest, GetRemindersResponse
)


class AbstractReminderManagementService(ABC):
    """Interface for reminder management operations."""
    
    @abstractmethod
    def create_reminder(self, request: CreateReminderRequest) -> CreateReminderResponse:
        """
        Create a reminder.
        
        Args:
            request: CreateReminderRequest with reminder information
            
        Returns:
            CreateReminderResponse with created reminder information
            
        Raises:
            ReminderTitleRequiredException: If title is missing
        """
        pass
    
    @abstractmethod
    def update_reminder(self, request: UpdateReminderRequest) -> UpdateReminderResponse:
        """
        Update an existing reminder.
        
        Args:
            request: UpdateReminderRequest with reminder_id, user_id, and fields to update
            
        Returns:
            UpdateReminderResponse with updated reminder information
            
        Raises:
            ReminderNotFoundByIdException: If reminder doesn't exist
            ReminderAccessDeniedException: If user doesn't have access
        """
        pass
    
    @abstractmethod
    def delete_reminder(self, request: DeleteReminderRequest) -> DeleteReminderResponse:
        """
        Delete a reminder.
        
        Args:
            request: DeleteReminderRequest with reminder_id and user_id
            
        Returns:
            DeleteReminderResponse with success status
            
        Raises:
            ReminderNotFoundByIdException: If reminder doesn't exist
            ReminderAccessDeniedException: If user doesn't have access
        """
        pass
    
    @abstractmethod
    def process_reminders(self, request: ProcessRemindersRequest) -> ProcessRemindersResponse:
        """
        Process scheduled reminders (called by scheduled task).
        
        Finds reminders that should be sent and sends notifications.
        
        Args:
            request: ProcessRemindersRequest with current_time and optional max_reminders
            
        Returns:
            ProcessRemindersResponse with processing results
        """
        pass
    
    @abstractmethod
    def get_reminders(self, request: GetRemindersRequest) -> GetRemindersResponse:
        """
        Get reminders for a user.
        
        Args:
            request: GetRemindersRequest with user_id and optional filters
            
        Returns:
            GetRemindersResponse with list of reminders
        """
        pass

