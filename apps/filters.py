import django_filters

from apps.models import Product, Order


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = ['category', ]


class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = ['status', 'color', 'size', 'product']
