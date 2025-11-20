# Standard library
# (none needed)

# Third-party
from django.db import models

# Internal
# (none needed)


class SavedFilter(models.Model):
    """SavedFilter model - saved filter configurations for users."""
    
    # Basic fields
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    # Filter criteria (stored as JSON)
    filter_criteria = models.JSONField(default=dict)  # Stores all filter parameters
    
    # Relationships (as IntegerField, not ForeignKey)
    user_id = models.IntegerField(db_index=True)  # Not ForeignKey to User
    
    # Timestamps (provided by usecase layer)
    created_at = models.BigIntegerField()
    updated_at = models.BigIntegerField()
    
    # Flags
    is_default = models.BooleanField(default=False)  # True for default filters
    
    class Meta:
        db_table = 'saved_filters'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user_id', 'is_default']),
            models.Index(fields=['user_id', 'created_at']),
        ]
    
    def __str__(self) -> str:
        return f"{self.name} (User: {self.user_id})"

