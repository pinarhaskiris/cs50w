# Generated by Django 3.1 on 2020-08-29 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20200829_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='imgUrl',
            field=models.CharField(default='https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/600px-No_image_available.svg.png', max_length=512),
        ),
    ]
