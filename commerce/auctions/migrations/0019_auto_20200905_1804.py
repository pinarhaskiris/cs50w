# Generated by Django 3.1 on 2020-09-05 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0018_listing_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='imgUrl',
            field=models.CharField(max_length=512, null=True),
        ),
    ]
