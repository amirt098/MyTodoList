# Standard library
from typing import Optional

# Third-party
from pydantic import BaseModel, ConfigDict, field_validator, model_validator
from pydantic_core import PydanticCustomError
from pydantic import FieldValidationInfo

# Internal
# (none needed)


class BaseRequest(BaseModel):
    """Base class for all request DTOs."""
    
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True
    )


class BaseResponse(BaseModel):
    """Base class for all response DTOs."""
    
    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True
    )


class BaseFilter(BaseModel):
    """Base class for all filter DTOs with pagination and ordering support."""
    
    order_by: str = '-id'
    limit: Optional[int] = None
    offset: Optional[int] = None
    
    @field_validator('limit')
    def limit_must_be_gt_one(cls, value, info: FieldValidationInfo):
        if value is not None and value < 1:
            raise PydanticCustomError('value_error', 'Limit should be greater than 1')
        return value
    
    @field_validator('offset')
    def offset_must_be_positive(cls, value, info: FieldValidationInfo):
        if value is not None and value < 0:
            raise PydanticCustomError('value_error', 'Offset should be positive')
        return value
    
    @model_validator(mode='after')
    def check_limit_offset_default(cls, filter_obj: 'BaseFilter'):
        if filter_obj.limit is None or filter_obj.offset is None:
            filter_obj.limit = 20
            filter_obj.offset = 0
        return filter_obj
    
    def as_dict(self):
        """Return filter fields as dict, excluding pagination fields."""
        return {k: v for (k, v) in self.model_dump().items() 
                if v is not None and k not in ['limit', 'offset', 'order_by']}

