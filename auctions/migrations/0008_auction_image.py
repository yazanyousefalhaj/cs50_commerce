# Generated by Django 3.2 on 2021-04-24 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auto_20210424_1434'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='image',
            field=models.URLField(null=True),
        ),
    ]
