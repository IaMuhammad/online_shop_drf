from django.contrib.admin import TabularInline

from apps.models.shop import Like


class LikeTranslatableTabularInline(TabularInline):
    model = Like.products.through
