from django.contrib import admin

from apps.models.shop import Image


class ImageTabularInline(admin.TabularInline):
    model = Image
