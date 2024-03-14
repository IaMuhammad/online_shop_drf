from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken

from apps.managers import UserManager


# Create your models here.

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "admin", _("Admin")
        USER = "user", _("User")

    role = models.CharField(max_length=55, choices=Role.choices, default=Role.ADMIN)
    username = None
    phone_number = models.CharField(_("Phone number"), max_length=14, unique=True)
    balance = models.DecimalField(_("Balance"), max_digits=99, decimal_places=2, default=Decimal(0))
    all_balance = models.DecimalField(_("Balance"), max_digits=99, decimal_places=2, default=Decimal(0))

    USERNAME_FIELD = 'phone_number'
    objects = UserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def tokens(self):
        '''Return access and refresh tokens'''
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    def __str__(self):
        if self.first_name and self.last_name:
            return self.get_full_name()
        return self.phone_number
