# Standard library
# (none needed)

# Third-party
from django.db import models

# Internal
# (none needed)


class Reminder(models.Model):
    """Reminder model - reminders for todos (todo_id as IntegerField)."""
    
    # Basic fields
    title = models.CharField(max_length=255)
    message = models.TextField(blank=True)
    
    # Reminder timing
    reminder_time = models.BigIntegerField()  # Timestamp when reminder should be sent
    sent_at = models.BigIntegerField(null=True, blank=True)  # Timestamp when reminder was sent
    
    # Notification channels
    NOTIFICATION_CHANNEL_CHOICES = [
        ('Email', 'Email'),
        ('SMS', 'SMS'),
        ('Telegram', 'Telegram'),
        ('Bale', 'Bale'),
        ('Eitaa', 'Eitaa'),
    ]
    notification_channels = models.JSONField(default=list)  # Array of channel names
    
    # Relationships (as IntegerField, not ForeignKey)
    todo_id = models.IntegerField(db_index=True, null=True, blank=True)  # Not ForeignKey to Todo
    user_id = models.IntegerField(db_index=True)  # Not ForeignKey to User
    
    # Reminder type
    REMINDER_TYPE_CHOICES = [
        ('Manual', 'Manual'),
        ('Deadline_Proximity', 'Deadline Proximity'),
        ('Overdue', 'Overdue'),
        ('Smart', 'Smart'),
    ]
    reminder_type = models.CharField(max_length=20, choices=REMINDER_TYPE_CHOICES, default='Manual')
    
    # Status
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Sent', 'Sent'),
        ('Failed', 'Failed'),
        ('Cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    
    # Timestamps (provided by usecase layer)
    created_at = models.BigIntegerField()
    updated_at = models.BigIntegerField()
    
    class Meta:
        db_table = 'reminders'
        ordering = ['reminder_time']
        indexes = [
            models.Index(fields=['user_id', 'status']),
            models.Index(fields=['reminder_time', 'status']),
            models.Index(fields=['todo_id', 'status']),
            models.Index(fields=['user_id', 'reminder_time']),
        ]
    
    def __str__(self) -> str:
        return f"{self.title} (User: {self.user_id}, Time: {self.reminder_time})"

