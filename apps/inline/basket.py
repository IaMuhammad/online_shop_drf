from django.contrib.admin import TabularInline
from parler.admin import TranslatableTabularInline

from apps.models.shop import BasketProduct, Basket


class BasketProductTranslatableTabularInline(TabularInline):
    model = Basket.products.through
