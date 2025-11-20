# Standard library
# (none needed)

# Third-party
from django.db import models

# Internal
# (none needed)


class KanbanColumn(models.Model):
    """KanbanColumn model - custom columns for projects (project_id as IntegerField)."""
    
    # Basic fields
    name = models.CharField(max_length=100)
    status_value = models.CharField(max_length=20, blank=True)  # Maps to Todo.status or custom value
    color = models.CharField(max_length=20, blank=True, default='#6B7280')  # Column color
    
    # Relationships (as IntegerField, not ForeignKey)
    project_id = models.IntegerField(db_index=True, null=True, blank=True)  # null = default columns
    user_id = models.IntegerField(db_index=True, null=True, blank=True)  # For user-specific columns
    
    # Ordering
    order = models.IntegerField(default=0)
    
    # Timestamps (provided by usecase layer)
    created_at = models.BigIntegerField()
    updated_at = models.BigIntegerField()
    
    # Flags
    is_default = models.BooleanField(default=False)  # True for default columns (ToDo, In Progress, Done)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'kanban_columns'
        ordering = ['order', 'created_at']
        indexes = [
            models.Index(fields=['project_id', 'is_active']),
            models.Index(fields=['user_id', 'is_active']),
            models.Index(fields=['project_id', 'order']),
        ]
    
    def __str__(self) -> str:
        return f"{self.name} (Project: {self.project_id or 'Default'})"

