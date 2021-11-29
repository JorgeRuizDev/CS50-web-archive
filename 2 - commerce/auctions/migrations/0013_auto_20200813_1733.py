# Generated by Django 3.0.8 on 2020-08-13 15:33

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_auto_20200802_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='users_watching',
            field=models.ManyToManyField(blank=True, related_name='user_watchlist', to=settings.AUTH_USER_MODEL),
        ),
    ]