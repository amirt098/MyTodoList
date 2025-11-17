# Standard library
# (none needed)

# Third-party
from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Internal
# (none needed)


class User(models.Model):
    """User model - no cross-module relationships."""
    
    email = models.EmailField(unique=True, db_index=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    
    class Meta:
        db_table = 'users'
        ordering = ['-created_at']
    
    def set_password(self, raw_password: str) -> None:
        """Hash and set password."""
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password: str) -> bool:
        """Check if provided password matches."""
        return check_password(raw_password, self.password)
    
    def __str__(self) -> str:
        return self.email

