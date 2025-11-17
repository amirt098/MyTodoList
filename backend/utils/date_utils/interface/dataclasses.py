# Standard library
from typing import Optional

# Third-party
from pydantic import BaseModel

# Internal - from other modules
from lib.base_models import BaseResponse

# Internal - from same interface module
# (none needed)


class TimestampDTO(BaseResponse):
    """DTO for timestamp representation in milliseconds."""
    timestamp_ms: int


class DateTimeDTO(BaseResponse):
    """DTO for structured datetime representation."""
    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int
    microsecond: int
    timestamp_ms: int
    timezone: str  # e.g., "UTC", "Asia/Tehran"


class JalaliDateDTO(BaseResponse):
    """DTO for Jalali (Persian) date representation."""
    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int
    microsecond: int
    timestamp_ms: int
    weekday: str  # e.g., "شنبه", "یکشنبه"
    month_name: str  # e.g., "فروردین", "اردیبهشت"


class DateTimeParseRequest(BaseModel):
    """Request DTO for parsing datetime strings."""
    date_string: str
    format_str: str = "%Y-%m-%d %H:%M:%S"


class DateTimeFormatRequest(BaseModel):
    """Request DTO for formatting datetime."""
    timestamp_ms: int
    format_str: str = "%Y-%m-%d %H:%M:%S"


class DateTimeAddRequest(BaseModel):
    """Request DTO for adding time to datetime."""
    timestamp_ms: int
    days: int = 0
    hours: int = 0
    minutes: int = 0

