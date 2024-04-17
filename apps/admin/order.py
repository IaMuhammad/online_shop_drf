from django.contrib import admin
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from parler.admin import TranslatableAdmin

from apps.inline.like import LikeTranslatableTabularInline
from apps.models.seller import Flow, Order
from apps.models.shop import Like
from apps.models.user import Region

# from apps.models.user import Region

csrf_protect_m = method_decorator(csrf_protect)
sensitive_post_parameters_m = method_decorator(sensitive_post_parameters())


@admin.register(Flow)
class FlowAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'product', 'is_active')
    readonly_fields = ('clicks',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'customer', 'status', 'flow_name', 'quantity')
    search_fields = ('product__translate__name',)
    list_filter = ('customer', 'status', 'flow')
    list_per_page = 20

    # readonly_fields = ('flow',)

    def flow_name(self, obj: Order):
        flow = obj.flow if obj.flow else None
        if flow:
            return format_html(f'''
            <a href={reverse('admin:apps_flow_change', args=(flow.pk,))}> {flow.name} </a>
            ''')
        return format_html(f'-')

    flow_name.admin_order_field = 'flow__name'
    flow_name.short_description = _('Flow Name')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product_quantity')
    list_display_links = list_display
    inlines = [LikeTranslatableTabularInline]
    readonly_fields = ('products',)

    def product_quantity(self, obj):
        return obj.products.count()


@admin.register(Region)
class RegionAdmin(TranslatableAdmin):
    list_display = ('id', 'name')
