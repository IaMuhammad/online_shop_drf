from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.

class Flow(models.Model):
    name = models.CharField(verbose_name=_('name'), max_length=255, null=False, blank=False)
    user = models.ForeignKey('apps.User', verbose_name=_('user'), on_delete=models.CASCADE)
    product = models.ForeignKey('apps.Product', verbose_name=_('product'), on_delete=models.CASCADE)
    clicks = models.PositiveIntegerField(default=0, verbose_name=_('clicks'), )
    is_active = models.BooleanField(default=True, verbose_name=_('is_active'), )

    class Meta:
        verbose_name = _('Flow')
        verbose_name_plural = _('Flows')

    @property
    def get_new(self):
        return self.order_set.filter(status=Order.Status.NEW).count()

    @property
    def get_accepted(self):
        return self.order_set.filter(status=Order.Status.ACCEPTED).count()

    @property
    def get_delivering(self):
        return self.order_set.filter(status=Order.Status.DELIVERING).count()

    @property
    def get_completed(self):
        return self.order_set.filter(status=Order.Status.COMPLETED).count()

    @property
    def get_recall(self):
        return self.order_set.filter(status=Order.Status.RECALL).count()

    @property
    def get_spam(self):
        return self.order_set.filter(status=Order.Status.SPAM).count()

    @property
    def get_canceled(self):
        return self.order_set.filter(status=Order.Status.CANCELED).count()

    @property
    def get_hold(self):
        return self.order_set.filter(status=Order.Status.HOLD).count()

    @property
    def get_archived(self):
        return self.order_set.filter(status=Order.Status.ARCHIVED).count()

    def __str__(self):
        return f"{self.user} -> {self.name}"


class Order(models.Model):
    class Status(models.TextChoices):
        NEW = 'new', _('Yangi')
        ACCEPTED = 'accepted', _('Qabul qilindi')
        DELIVERING = 'delivering', _('Yetkazilmoqda')
        COMPLETED = 'completed', _('Yetkazib berildi')
        RECALL = 'recall', _('Qayta qo`ngiroq')
        SPAM = 'spam', _('Spam')
        CANCELED = 'canceled', _('Qaytib keldi')
        HOLD = 'hold', _('Hold')
        ARCHIVED = 'archived', _('Arxivlandi')

    status = models.CharField(verbose_name=_('status'), max_length=30, choices=Status.choices, default=Status.NEW)
    product = models.ForeignKey('apps.Product', verbose_name=_('product'), on_delete=models.CASCADE)
    color = models.ForeignKey('apps.ProductAttribute', verbose_name=_('color'), on_delete=models.PROTECT,
                              related_name='order_color')
    size = models.ForeignKey('apps.ProductAttribute', verbose_name=_('size'), on_delete=models.PROTECT,
                             related_name='order_size')
    flow = models.ForeignKey('apps.Flow', verbose_name=_('flow'), on_delete=models.PROTECT, null=True, blank=True)
    region = models.ForeignKey('apps.Region', verbose_name=_('region'), on_delete=models.CASCADE, default=1)
    customer = models.ForeignKey('apps.User', verbose_name=_('customer'), on_delete=models.CASCADE)
    customer_number = models.CharField(verbose_name=_('customer_number'), max_length=20, null=False, blank=False)
    customer_name = models.CharField(verbose_name=_('customer_name'), max_length=50, null=False, blank=False)
    customer_address = models.CharField(verbose_name=_('customer_address'), default='', max_length=255, null=True,
                                        blank=True)
    quantity = models.IntegerField(verbose_name=_('quantity'), default=1, null=False, blank=False)
    price = models.DecimalField(verbose_name=_('price'), max_digits=99, decimal_places=2, default=Decimal(0))
    created_at = models.DateTimeField(verbose_name=_('created_at'), auto_now_add=True)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
