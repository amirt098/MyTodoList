# Standard library
from datetime import datetime, timezone

# Third-party
import jdatetime

# Internal - from same module
from . import interface


class DateTimeService(interface.AbstractDateTimeService):
    """Service for datetime operations and timestamp generation."""
    
    # Jalali month names in Persian
    JALALI_MONTHS = [
        "فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
        "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"
    ]
    
    # Jalali weekday names in Persian
    JALALI_WEEKDAYS = [
        "شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه"
    ]
    
    def now(self) -> interface.TimestampDTO:
        """Get current datetime as timestamp in milliseconds."""
        timestamp_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
        return interface.TimestampDTO(timestamp_ms=timestamp_ms)
    
    def now_detailed(self) -> interface.DateTimeDTO:
        """Get current datetime as structured DTO."""
        now = datetime.now(timezone.utc)
        timestamp_ms = int(now.timestamp() * 1000)
        return interface.DateTimeDTO(
            year=now.year,
            month=now.month,
            day=now.day,
            hour=now.hour,
            minute=now.minute,
            second=now.second,
            microsecond=now.microsecond,
            timestamp_ms=timestamp_ms,
            timezone="UTC"
        )
    
    def now_jalali(self) -> interface.JalaliDateDTO:
        """Get current datetime as Jalali (Persian) date DTO."""
        now = datetime.now(timezone.utc)
        jalali_date = jdatetime.datetime.fromgregorian(datetime=now)
        timestamp_ms = int(now.timestamp() * 1000)
        
        return interface.JalaliDateDTO(
            year=jalali_date.year,
            month=jalali_date.month,
            day=jalali_date.day,
            hour=jalali_date.hour,
            minute=jalali_date.minute,
            second=jalali_date.second,
            microsecond=jalali_date.microsecond,
            timestamp_ms=timestamp_ms,
            weekday=self.JALALI_WEEKDAYS[jalali_date.weekday()],
            month_name=self.JALALI_MONTHS[jalali_date.month - 1]
        )
    
    def from_timestamp_ms(self, timestamp_ms: int) -> interface.DateTimeDTO:
        """Convert Unix timestamp in milliseconds to DateTimeDTO."""
        dt = datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc)
        return interface.DateTimeDTO(
            year=dt.year,
            month=dt.month,
            day=dt.day,
            hour=dt.hour,
            minute=dt.minute,
            second=dt.second,
            microsecond=dt.microsecond,
            timestamp_ms=timestamp_ms,
            timezone="UTC"
        )
    
    def from_timestamp_ms_jalali(self, timestamp_ms: int) -> interface.JalaliDateDTO:
        """Convert Unix timestamp in milliseconds to JalaliDateDTO."""
        dt = datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc)
        jalali_date = jdatetime.datetime.fromgregorian(datetime=dt)
        
        return interface.JalaliDateDTO(
            year=jalali_date.year,
            month=jalali_date.month,
            day=jalali_date.day,
            hour=jalali_date.hour,
            minute=jalali_date.minute,
            second=jalali_date.second,
            microsecond=jalali_date.microsecond,
            timestamp_ms=timestamp_ms,
            weekday=self.JALALI_WEEKDAYS[jalali_date.weekday()],
            month_name=self.JALALI_MONTHS[jalali_date.month - 1]
        )
    
    def to_timestamp_ms(self, year: int, month: int, day: int, hour: int = 0, minute: int = 0, second: int = 0) -> int:
        """Convert date components to Unix timestamp in milliseconds."""
        dt = datetime(year, month, day, hour, minute, second, tzinfo=timezone.utc)
        return int(dt.timestamp() * 1000)
    
    def to_timestamp_ms_jalali(self, year: int, month: int, day: int, hour: int = 0, minute: int = 0, second: int = 0) -> int:
        """Convert Jalali date components to Unix timestamp in milliseconds."""
        jalali_dt = jdatetime.datetime(year, month, day, hour, minute, second)
        gregorian_dt = jalali_dt.togregorian()
        dt = datetime(
            gregorian_dt.year,
            gregorian_dt.month,
            gregorian_dt.day,
            gregorian_dt.hour,
            gregorian_dt.minute,
            gregorian_dt.second,
            tzinfo=timezone.utc
        )
        return int(dt.timestamp() * 1000)
    
    def format_datetime(self, request: interface.DateTimeFormatRequest) -> str:
        """Format timestamp to string."""
        dt = datetime.fromtimestamp(request.timestamp_ms / 1000, tz=timezone.utc)
        return dt.strftime(request.format_str)
    
    def parse_datetime(self, request: interface.DateTimeParseRequest) -> interface.TimestampDTO:
        """Parse datetime string to timestamp."""
        dt = datetime.strptime(request.date_string, request.format_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        timestamp_ms = int(dt.timestamp() * 1000)
        return interface.TimestampDTO(timestamp_ms=timestamp_ms)
    
    def add_time(self, request: interface.DateTimeAddRequest) -> interface.TimestampDTO:
        """Add time (days, hours, minutes) to a timestamp."""
        from datetime import timedelta
        
        dt = datetime.fromtimestamp(request.timestamp_ms / 1000, tz=timezone.utc)
        delta = timedelta(days=request.days, hours=request.hours, minutes=request.minutes)
        new_dt = dt + delta
        new_timestamp_ms = int(new_dt.timestamp() * 1000)
        return interface.TimestampDTO(timestamp_ms=new_timestamp_ms)
    
    def difference_ms(self, timestamp_ms1: int, timestamp_ms2: int) -> int:
        """Calculate difference between two timestamps in milliseconds."""
        return timestamp_ms1 - timestamp_ms2
    
    def is_before(self, timestamp_ms1: int, timestamp_ms2: int) -> bool:
        """Check if timestamp_ms1 is before timestamp_ms2."""
        return timestamp_ms1 < timestamp_ms2
    
    def is_after(self, timestamp_ms1: int, timestamp_ms2: int) -> bool:
        """Check if timestamp_ms1 is after timestamp_ms2."""
        return timestamp_ms1 > timestamp_ms2


# Global instance for easy access
datetime_service = DateTimeService()
