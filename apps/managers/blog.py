from django.db.models import Manager

from parler.managers import TranslatableQuerySet


class CustomQueryset(TranslatableQuerySet):
    pass


class ActiveBannersManager(TranslatableQuerySet):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True).order_by('-id')
