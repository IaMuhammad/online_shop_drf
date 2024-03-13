from parler.admin import TranslatableTabularInline

from apps.models.shop import ProductAttribute


class ProductAttributeTranslatableTabularInline(TranslatableTabularInline):
    model = ProductAttribute
