# Generated by Django 4.2.3 on 2024-04-17 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0016_remove_region_name_regiontranslation'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='add_flow',
            field=models.BooleanField(default=True, verbose_name='add_flow'),
        ),
    ]
