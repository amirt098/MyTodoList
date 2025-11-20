# Standard library
# (none needed)

# Third-party
from django.db import models

# Internal
# (none needed)


class Todo(models.Model):
    """Todo model - no cross-module relationships (user_id and project_id as IntegerField)."""
    
    # Basic fields
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    deadline = models.BigIntegerField(null=True, blank=True)
    
    # Enums
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium')
    
    STATUS_CHOICES = [
        ('ToDo', 'ToDo'),
        ('In Progress', 'In Progress'),
        ('Waiting', 'Waiting'),
        ('Blocked', 'Blocked'),
        ('Done', 'Done'),
        ('Cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ToDo')
    
    # Organization
    category = models.CharField(max_length=100, blank=True)
    labels = models.JSONField(default=list, blank=True)  # Array of strings
    
    # Relationships (as IntegerField, not ForeignKey)
    user_id = models.IntegerField(db_index=True)  # Not ForeignKey to User
    project_id = models.IntegerField(null=True, blank=True, db_index=True)  # Not ForeignKey to Project
    
    # Dependencies (as IntegerField, not ForeignKey)
    previous_todo_id = models.IntegerField(null=True, blank=True)  # Not ForeignKey
    next_todo_id = models.IntegerField(null=True, blank=True)  # Not ForeignKey
    
    # Ordering
    order = models.IntegerField(default=0)
    
    # Timestamps (provided by usecase layer)
    created_at = models.BigIntegerField()
    updated_at = models.BigIntegerField()
    completed_at = models.BigIntegerField(null=True, blank=True)
    
    # Auto-repeat
    AUTO_REPEAT_CHOICES = [
        ('None', 'None'),
        ('Daily', 'Daily'),
        ('Weekly', 'Weekly'),
        ('Monthly', 'Monthly'),
    ]
    auto_repeat = models.CharField(max_length=10, choices=AUTO_REPEAT_CHOICES, default='None')
    
    class Meta:
        db_table = 'todos'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user_id', 'status']),
            models.Index(fields=['user_id', 'deadline']),
            models.Index(fields=['project_id', 'status']),
            models.Index(fields=['user_id', 'created_at']),
        ]
    
    def __str__(self) -> str:
        return self.title


