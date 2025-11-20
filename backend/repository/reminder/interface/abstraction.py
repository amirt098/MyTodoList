# Standard library
from abc import ABC, abstractmethod

# Internal - from same interface module (direct import, no interface. prefix needed)
from .dataclasses import ReminderDTO, ReminderFilter, ReminderCreateRequest, ReminderUpdateRequest


class AbstractReminderRepository(ABC):
    """Interface for reminder repository operations."""
    
    @abstractmethod
    def create(self, reminder_data: ReminderCreateRequest) -> ReminderDTO:
        """
        Create a new reminder in the database.
        
        Args:
            reminder_data: ReminderCreateRequest object with reminder information (including created_at and updated_at timestamps)
            
        Returns:
            ReminderDTO with created reminder information
            
        Raises:
            ReminderTitleRequiredException: If title is missing
        """
        pass
    
    @abstractmethod
    def get_by_id(self, reminder_id: int) -> ReminderDTO | None:
        """
        Get reminder by ID.
        
        Args:
            reminder_id: Reminder ID to fetch
            
        Returns:
            ReminderDTO if found, None otherwise
        """
        pass
    
    @abstractmethod
    def get_reminders(self, filters: ReminderFilter) -> list[ReminderDTO]:
        """
        Get reminders with filtering.
        
        General method for querying reminders with various filters.
        
        Args:
            filters: ReminderFilter Pydantic object extending BaseFilter from lib
            
        Returns:
            List of ReminderDTO matching the filters
        """
        pass
    
    @abstractmethod
    def update(self, reminder_id: int, reminder_data: ReminderUpdateRequest) -> ReminderDTO:
        """
        Update an existing reminder.
        
        Args:
            reminder_id: Reminder ID to update
            reminder_data: ReminderUpdateRequest with fields to update (only provided fields will be updated, including updated_at timestamp)
            
        Returns:
            ReminderDTO with updated reminder information
            
        Raises:
            ReminderNotFoundByIdException: If reminder doesn't exist
        """
        pass
    
    @abstractmethod
    def delete(self, reminder_id: int) -> None:
        """
        Delete a reminder.
        
        Args:
            reminder_id: Reminder ID to delete
            
        Raises:
            ReminderNotFoundByIdException: If reminder doesn't exist
        """
        pass

