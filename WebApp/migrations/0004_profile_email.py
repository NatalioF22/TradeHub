# Generated by Django 4.2.2 on 2023-07-20 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebApp', '0003_profile_profession'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.EmailField(blank=True, max_length=500, null=True),
        ),
    ]