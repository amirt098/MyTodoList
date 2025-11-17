# Timestamp Handling Architecture

[← Back to Architecture Index](./ARCHITECTURE.md)

---

## Timestamp Management

Timestamps (`created_at`, `updated_at`) are **NOT** automatically generated in the repository layer. Instead, they are:

1. **Calculated in the UseCase layer** - UseCase determines when timestamps should be set
2. **Passed to Repository** - Timestamps are included in data transfer objects
3. **Stored by Repository** - Repository simply stores the provided timestamps

## Why This Approach?

- **Business Logic Control**: UseCase layer controls when timestamps are set, allowing for business rules (e.g., backdating, timezone handling)
- **Testability**: Timestamps can be easily mocked or controlled in tests
- **Consistency**: All timestamp logic is centralized in the UseCase layer
- **Flexibility**: Allows for custom timestamp logic (e.g., preserving original created_at on updates)

## Implementation

### 1. Model Definition

Django models should **NOT** use `auto_now_add` or `auto_now`:

```python
# repository/user/models.py
class User(models.Model):
    email = models.EmailField(unique=True)
    # ❌ BAD: created_at = models.DateTimeField(auto_now_add=True)
    # ❌ BAD: updated_at = models.DateTimeField(auto_now=True)
    
    # ✅ GOOD: Timestamps without auto-generation
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
```

### 2. Data Transfer Objects

Include timestamps in data classes:

```python
# repository/user/interface/dataclasses.py
from datetime import datetime
from typing import Optional

class UserData:
    def __init__(
        self,
        email: str,
        password: str,
        # ... other fields ...
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.email = email
        self.password = password
        # ... other fields ...
        self.created_at = created_at
        self.updated_at = updated_at
```

### 3. UseCase Layer - Calculate Timestamps

Use the `DateTimeService` from `utils.date_utils` for all datetime operations. The service returns DTOs, not datetime objects:

```python
# usecase/user_management/service.py
from datetime import datetime, timezone
from utils.date_utils import datetime_service

def register_user(self, request: RegisterUserRequest) -> RegisterUserResponse:
    # Calculate timestamps in usecase layer using DateTimeService
    now_dto = datetime_service.now()  # Returns TimestampDTO with timestamp_ms
    # Convert to datetime for repository (if needed)
    created_at = datetime.fromtimestamp(now_dto.timestamp_ms / 1000, tz=timezone.utc)
    updated_at = datetime.fromtimestamp(now_dto.timestamp_ms / 1000, tz=timezone.utc)
    
    # Pass timestamps to repository
    user_data = request.to_user_data(created_at, updated_at)
    user_dto = self.user_repo.create(user_data)
    # ...
```

### 4. Repository Layer - Store Timestamps

```python
# repository/user/service.py
def create(self, user_data: UserData) -> UserDTO:
    user = User()
    user.email = user_data.email
    # ... set other fields ...
    
    # Timestamps are provided by usecase layer
    if user_data.created_at:
        user.created_at = user_data.created_at
    if user_data.updated_at:
        user.updated_at = user_data.updated_at
    
    user.save()
    # ...
```

### 5. Update Operations

For updates, only `updated_at` is recalculated:

```python
# usecase/user_management/service.py
from datetime import datetime, timezone
from utils.date_utils import datetime_service

def update_profile(self, request: UpdateProfileRequest) -> UpdateProfileResponse:
    # Calculate updated timestamp in usecase layer using DateTimeService
    now_dto = datetime_service.now()  # Returns TimestampDTO
    updated_at = datetime.fromtimestamp(now_dto.timestamp_ms / 1000, tz=timezone.utc)
    
    # Pass updated timestamp to repository
    user_data = request.to_user_data(updated_at)
    updated_user_dto = self.user_repo.update(request.user_id, user_data)
    # ...
```

## Best Practices

1. **Always calculate timestamps in UseCase** - Never rely on database auto-generation
2. **Use `DateTimeService` from `utils.date_utils`** - Centralized datetime operations ensure consistency
   - Use `datetime_service.now()` for UTC timestamps
   - Use `datetime_service.now_local()` for local timezone (if needed)
3. **Document timestamp requirements** - In abstract class docstrings, mention that timestamps are provided by UseCase
4. **Handle timezone consistently** - Use UTC by default via `DateTimeService.now()`
5. **Preserve `created_at` on updates** - Never update `created_at` when updating records
6. **Use DateTimeService for all datetime operations** - Conversion, formatting, calculations should go through the service

## Example: Complete Flow

```python
# 1. UseCase calculates timestamps using DateTimeService
from utils.date_utils import datetime_service

now = datetime_service.now()  # UTC datetime
created_at = now
updated_at = now

# 2. UseCase creates UserData with timestamps
user_data = UserData(
    email="user@example.com",
    password="hashed_password",
    created_at=created_at,
    updated_at=updated_at
)

# 3. Repository receives and stores timestamps
user = User()
user.email = user_data.email
user.created_at = user_data.created_at  # From UseCase (UTC)
user.updated_at = user_data.updated_at  # From UseCase (UTC)
user.save()
```

## DateTimeService Utilities

The `DateTimeService` in `utils/date_utils/service.py` returns DTOs, not datetime objects:

### DTOs

- **`TimestampDTO`** - Simple timestamp in milliseconds
  ```python
  timestamp_dto = datetime_service.now()
  # timestamp_dto.timestamp_ms
  ```

- **`DateTimeDTO`** - Structured datetime with year, month, day, hour, minute, second
  ```python
  dt_dto = datetime_service.now_detailed()
  # dt_dto.year, dt_dto.month, dt_dto.day, etc.
  ```

- **`JalaliDateDTO`** - Jalali (Persian) calendar date
  ```python
  jalali_dto = datetime_service.now_jalali()
  # jalali_dto.year (Jalali), jalali_dto.month_name (Persian), jalali_dto.weekday (Persian)
  ```

### Methods

- `now()` - Returns `TimestampDTO` with current timestamp in milliseconds
- `now_detailed()` - Returns `DateTimeDTO` with structured date/time
- `now_jalali()` - Returns `JalaliDateDTO` with Jalali calendar information
- `from_timestamp_ms()` - Convert timestamp to `DateTimeDTO`
- `from_timestamp_ms_jalali()` - Convert timestamp to `JalaliDateDTO`
- `to_timestamp_ms()` - Convert date components to timestamp (Gregorian)
- `to_timestamp_ms_jalali()` - Convert Jalali date components to timestamp
- `format_datetime()` - Format timestamp to string
- `parse_datetime()` - Parse string to `TimestampDTO`
- `add_time()` - Add days/hours/minutes to timestamp
- `difference_ms()` - Calculate difference in milliseconds
- `is_before()`, `is_after()` - Compare timestamps

### Jalali Date Support

The service fully supports Jalali (Persian) calendar:
- Convert Gregorian to Jalali
- Convert Jalali to Gregorian
- Get Jalali month names and weekdays in Persian
- All operations work with both calendars

Always use `DateTimeService` instead of direct `datetime` operations for consistency, testability, and Jalali date support.

---

[← Back to Architecture Index](./ARCHITECTURE.md) | [Previous: Exception Handling →](./ARCHITECTURE_EXCEPTIONS.md)

