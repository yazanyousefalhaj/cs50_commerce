# Generated by Django 3.2 on 2021-04-23 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_remove_auction_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
