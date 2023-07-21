# Generated by Django 4.2.3 on 2023-07-21 05:32

from django.conf import settings
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('WebApp', '0009_remove_item_product_review_remove_item_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemreview',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='itemreview',
            unique_together={('item', 'user')},
        ),
    ]