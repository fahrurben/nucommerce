from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

from nucommerce.managers import CustomUserManager

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)

    class UserRoles(models.TextChoices):
        ADMIN = 'admin', _('Administrator')
        USER = 'staff', _('User')

    role = models.CharField(
        max_length=11,
        choices=UserRoles.choices,
        default=UserRoles.USER,
    )
    verified_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name', 'role')


    objects = CustomUserManager()

    def __str__(self):
        return self.email
