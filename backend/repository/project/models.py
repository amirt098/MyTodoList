# Standard library
# (none needed)

# Third-party
from django.db import models

# Internal
# (none needed)


class Project(models.Model):
    """Project model - no cross-module relationships (owner_id as IntegerField)."""
    
    # Basic fields
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_private = models.BooleanField(default=True)
    
    # Relationships (as IntegerField, not ForeignKey)
    owner_id = models.IntegerField(db_index=True)  # Not ForeignKey to User
    
    # Timestamps (provided by usecase layer)
    created_at = models.BigIntegerField()
    updated_at = models.BigIntegerField()
    
    class Meta:
        db_table = 'projects'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['owner_id', 'is_private']),
            models.Index(fields=['owner_id', 'created_at']),
        ]
    
    def __str__(self) -> str:
        return self.name


class ProjectMember(models.Model):
    """ProjectMember model - relationship between Project and User (both as IntegerField)."""
    
    # Relationships (as IntegerField, not ForeignKey)
    project_id = models.IntegerField(db_index=True)  # Not ForeignKey to Project
    user_id = models.IntegerField(db_index=True)  # Not ForeignKey to User
    
    # Role
    ROLE_CHOICES = [
        ('Owner', 'Owner'),
        ('Admin', 'Admin'),
        ('Member', 'Member'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Member')
    
    # Timestamps (provided by usecase layer)
    joined_at = models.BigIntegerField()
    
    class Meta:
        db_table = 'project_members'
        unique_together = [['project_id', 'user_id']]
        indexes = [
            models.Index(fields=['project_id', 'role']),
            models.Index(fields=['user_id', 'role']),
        ]
    
    def __str__(self) -> str:
        return f"Project {self.project_id} - User {self.user_id} ({self.role})"

