from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.managers import UserManager


# Create your models here.

class User(AbstractUser):
    username = None
    phone_number = models.CharField(_("Phone number"), max_length=14, unique=True)

    USERNAME_FIELD = 'phone_number'
    objects = UserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

# class UserFlow(User):
#     class Meta:
#         proxy = True
#         verbose_name = _('User Flow')
#         verbose_name_plural = _('User Flows')
