# Generated by Django 4.2.3 on 2023-07-21 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebApp', '0006_item_product_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(max_length=30),
        ),
    ]
