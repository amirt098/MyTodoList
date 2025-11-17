# Standard library
# (none needed)

# Third-party
from django.apps import AppConfig

# Internal
# (none needed)


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'repository.user'
    verbose_name = 'User Repository'

