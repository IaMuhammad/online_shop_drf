from decimal import Decimal

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from apps.models import Product, Order


@receiver(pre_save, sender=Order)
def pre_save_order(sender, instance: Order, *args, **kwargs):
    product = instance.product
    if instance.pk:
        last_data = Order.objects.filter(id=instance.pk).first()
        delta = instance.quantity - (last_data.quantity if last_data else Decimal(0))
        product.quantity -= delta
        product.save()
    else:
        product.quantity -= instance.quantity
        product.save()
