from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):

    def _create_user(self, phone_number, password, is_staff, is_superuser, **extra_fields):
        if not phone_number:
            raise ValueError(_('Unikal telefon_raqami talab qilinadi'))
        user = self.model(
            phone_number=phone_number,
            is_active=True,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, password, **extra_fields):
        return self._create_user(phone_number, password, False, False, **extra_fields)

    def create_superuser(self, phone_number, password, **extra_fields):
        user = self._create_user(phone_number, password, True, True, **extra_fields)
        user.save(using=self._db)
        return user
