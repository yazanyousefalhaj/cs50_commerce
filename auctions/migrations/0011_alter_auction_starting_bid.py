# Generated by Django 3.2 on 2021-04-25 19:03

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_alter_auction_starting_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='starting_bid',
            field=models.DecimalField(decimal_places=2, max_digits=20, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))]),
        ),
    ]
