# Generated by Django 3.2.10 on 2023-04-23 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0002_alter_user_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendor',
            name='address',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='phone',
        ),
        migrations.AddField(
            model_name='vendor',
            name='email',
            field=models.EmailField(default='test@gmail.com', max_length=254, unique=True),
        ),
    ]
