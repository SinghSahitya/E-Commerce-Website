# Generated by Django 3.2.10 on 2023-05-11 17:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0011_wishlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='ordered_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
