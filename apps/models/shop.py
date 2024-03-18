from decimal import Decimal

from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields

from apps.managers.blog import ActiveBannersManager, CustomQueryset


class Category(TranslatableModel):
    translate = TranslatedFields(
        name=models.CharField(verbose_name=_('name'), max_length=255)
    )
    icon = models.ImageField(verbose_name=_('icon'), upload_to='category/')
    slug = models.SlugField(verbose_name=_('slug'), max_length=255, unique=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            while Category.objects.filter(slug=self.slug).exists():
                slug = Category.objects.filter(slug=self.slug).first().slug
                if '-' in slug:
                    try:
                        if slug.split('-')[-1] in self.name:
                            self.slug += '-1'
                        else:
                            self.slug = '-'.join(slug.split('-')[:-1]) + '-' + str(int(slug.split('-')[-1]) + 1)
                    except:
                        self.slug = slug + '-1'
                else:
                    self.slug += '-1'

        super().save(*args, **kwargs)


class Image(models.Model):
    image = models.ImageField(verbose_name=_('image'), upload_to='products/%Y/%m/')
    is_main = models.BooleanField(verbose_name=_('is_main'), default=False)
    product = models.ForeignKey('apps.Product', verbose_name=_('product'), on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product} -> {self.id}"


class Product(TranslatableModel):
    translate = TranslatedFields(
        name=models.CharField(max_length=255),
        delivery=models.CharField(max_length=255, null=True, blank=True),
        description=models.TextField(null=True, blank=True),
    )
    category = models.ForeignKey('apps.Category', verbose_name=_('category'), on_delete=models.PROTECT)
    price = models.DecimalField(verbose_name=_('price'), max_digits=99, decimal_places=2)
    is_discount = models.BooleanField(verbose_name=_('is_discount'), default=False)
    discount_price = models.DecimalField(verbose_name=_('discount_price'), max_digits=99, decimal_places=2,
                                         default=Decimal(0), blank=True)
    quantity = models.IntegerField(verbose_name=_('quantity'), )

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    @property
    def liked_users(self):
        return self.like_set.values_list('user_id', flat=True)

    @property
    def get_attributes(self):
        _data = {}
        for attr in self.productattribute_set.all():
            if _data.get(attr.attribute.name):
                _data[attr.attribute.name].append(attr)
            else:
                _data[attr.attribute.name] = [attr]
        return _data

    @property
    def get_images(self):
        return self.image_set.all()

    @property
    def get_image(self):
        if self.image_set.filter(is_main=True).exists():
            return self.image_set.filter(is_main=True).first()
        return self.image_set.first()

    def __str__(self):
        return self.name


class Attribute(TranslatableModel):
    translate = TranslatedFields(
        name=models.CharField(max_length=255)
    )

    class Meta:
        verbose_name = _('Attribute')
        verbose_name_plural = _('Attributes')

    def __str__(self):
        return self.name


class ProductAttribute(TranslatableModel):
    translate = TranslatedFields(
        value=models.CharField(max_length=255)
    )
    image = models.ImageField(verbose_name=_('image'), upload_to='product-attribute/%Y', null=True, blank=True)
    attribute = models.ForeignKey('apps.Attribute', verbose_name=_('attribute'), on_delete=models.CASCADE)
    product = models.ForeignKey('apps.Product', verbose_name=_('product'), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('ProductAttribute')
        verbose_name_plural = _('ProductAttributes')

    def __str__(self):
        return f"{self.attribute.name} -> {self.product.name}"


class Like(models.Model):
    user = models.ForeignKey('apps.User', verbose_name=_('user'), on_delete=models.CASCADE, unique=True)
    products = models.ManyToManyField('apps.Product', verbose_name=_('products'))

    class Meta:
        verbose_name = _('Like')
        verbose_name_plural = _('Likes')


class Banner(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(verbose_name=_('image'), upload_to='banner/%Y/%m/')
    is_active = models.BooleanField(verbose_name=_('is_active'), default=True)

    objects = CustomQueryset.as_manager()
    active = ActiveBannersManager.as_manager()

    class Meta:
        verbose_name = _('Banner')
        verbose_name_plural = _('Banners')


class Request(models.Model):
    user = models.ForeignKey('apps.User', verbose_name=_('user'), on_delete=models.CASCADE)
    card = models.PositiveIntegerField()
    money = models.PositiveIntegerField()
