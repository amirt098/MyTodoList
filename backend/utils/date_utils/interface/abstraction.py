# Standard library
from abc import ABC, abstractmethod

# Third-party
# (none needed)

# Internal - from same interface module (direct import, no interface. prefix needed)
from .dataclasses import (
    TimestampDTO,
    DateTimeDTO,
    JalaliDateDTO,
    DateTimeParseRequest,
    DateTimeFormatRequest,
    DateTimeAddRequest
)


class AbstractDateTimeService(ABC):
    """Interface for datetime operations and timestamp generation."""
    
    @abstractmethod
    def now(self) -> TimestampDTO:
        """
        Get current datetime as timestamp in milliseconds.
        
        Returns:
            TimestampDTO with current timestamp in milliseconds
        """
        pass
    
    @abstractmethod
    def now_detailed(self) -> DateTimeDTO:
        """
        Get current datetime as structured DTO.
        
        Returns:
            DateTimeDTO with year, month, day, hour, minute, second, etc.
        """
        pass
    
    @abstractmethod
    def now_jalali(self) -> JalaliDateDTO:
        """
        Get current datetime as Jalali (Persian) date DTO.
        
        Returns:
            JalaliDateDTO with Jalali calendar information
        """
        pass
    
    @abstractmethod
    def from_timestamp_ms(self, timestamp_ms: int) -> DateTimeDTO:
        """
        Convert Unix timestamp in milliseconds to DateTimeDTO.
        
        Args:
            timestamp_ms: Unix timestamp in milliseconds
            
        Returns:
            DateTimeDTO with structured datetime information
        """
        pass
    
    @abstractmethod
    def from_timestamp_ms_jalali(self, timestamp_ms: int) -> JalaliDateDTO:
        """
        Convert Unix timestamp in milliseconds to JalaliDateDTO.
        
        Args:
            timestamp_ms: Unix timestamp in milliseconds
            
        Returns:
            JalaliDateDTO with Jalali calendar information
        """
        pass
    
    @abstractmethod
    def to_timestamp_ms(self, year: int, month: int, day: int, hour: int = 0, minute: int = 0, second: int = 0) -> int:
        """
        Convert date components to Unix timestamp in milliseconds.
        
        Args:
            year: Year (Gregorian)
            month: Month (1-12)
            day: Day (1-31)
            hour: Hour (0-23)
            minute: Minute (0-59)
            second: Second (0-59)
            
        Returns:
            Unix timestamp in milliseconds
        """
        pass
    
    @abstractmethod
    def to_timestamp_ms_jalali(self, year: int, month: int, day: int, hour: int = 0, minute: int = 0, second: int = 0) -> int:
        """
        Convert Jalali date components to Unix timestamp in milliseconds.
        
        Args:
            year: Year (Jalali)
            month: Month (1-12)
            day: Day (1-31)
            hour: Hour (0-23)
            minute: Minute (0-59)
            second: Second (0-59)
            
        Returns:
            Unix timestamp in milliseconds
        """
        pass
    
    @abstractmethod
    def format_datetime(self, request: DateTimeFormatRequest) -> str:
        """
        Format timestamp to string.
        
        Args:
            request: DateTimeFormatRequest with timestamp_ms and format_str
            
        Returns:
            Formatted datetime string
        """
        pass
    
    @abstractmethod
    def parse_datetime(self, request: DateTimeParseRequest) -> TimestampDTO:
        """
        Parse datetime string to timestamp.
        
        Args:
            request: DateTimeParseRequest with date_string and format_str
            
        Returns:
            TimestampDTO with parsed timestamp in milliseconds
        """
        pass
    
    @abstractmethod
    def add_time(self, request: DateTimeAddRequest) -> TimestampDTO:
        """
        Add time (days, hours, minutes) to a timestamp.
        
        Args:
            request: DateTimeAddRequest with timestamp_ms and time components
            
        Returns:
            TimestampDTO with new timestamp in milliseconds
        """
        pass
    
    @abstractmethod
    def difference_ms(self, timestamp_ms1: int, timestamp_ms2: int) -> int:
        """
        Calculate difference between two timestamps in milliseconds.
        
        Args:
            timestamp_ms1: First timestamp in milliseconds
            timestamp_ms2: Second timestamp in milliseconds
            
        Returns:
            Difference in milliseconds (positive if timestamp_ms1 > timestamp_ms2)
        """
        pass
    
    @abstractmethod
    def is_before(self, timestamp_ms1: int, timestamp_ms2: int) -> bool:
        """
        Check if timestamp_ms1 is before timestamp_ms2.
        
        Args:
            timestamp_ms1: First timestamp in milliseconds
            timestamp_ms2: Second timestamp in milliseconds
            
        Returns:
            True if timestamp_ms1 is before timestamp_ms2
        """
        pass
    
    @abstractmethod
    def is_after(self, timestamp_ms1: int, timestamp_ms2: int) -> bool:
        """
        Check if timestamp_ms1 is after timestamp_ms2.
        
        Args:
            timestamp_ms1: First timestamp in milliseconds
            timestamp_ms2: Second timestamp in milliseconds
            
        Returns:
            True if timestamp_ms1 is after timestamp_ms2
        """
        pass
