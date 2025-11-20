# Standard library
# (none needed)

# Third-party
from django.db import models

# Internal
# (none needed)


class Subtask(models.Model):
    """Subtask model - simple subtasks for todos (todo_id as IntegerField)."""
    
    # Basic fields
    title = models.CharField(max_length=255)
    
    # Status
    STATUS_CHOICES = [
        ('ToDo', 'ToDo'),
        ('Done', 'Done'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ToDo')
    
    # Relationships (as IntegerField, not ForeignKey)
    todo_id = models.IntegerField(db_index=True)  # Not ForeignKey to Todo
    
    # Ordering
    order = models.IntegerField(default=0)
    
    # Timestamps (provided by usecase layer)
    created_at = models.BigIntegerField()
    updated_at = models.BigIntegerField()
    completed_at = models.BigIntegerField(null=True, blank=True)
    
    class Meta:
        db_table = 'subtasks'
        ordering = ['order', 'created_at']
        indexes = [
            models.Index(fields=['todo_id', 'status']),
            models.Index(fields=['todo_id', 'order']),
        ]
    
    def __str__(self) -> str:
        return f"{self.title} (Todo: {self.todo_id})"

