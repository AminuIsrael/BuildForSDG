# Generated by Django 2.2.10 on 2020-05-26 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_usertrasactionhistory_coin_mined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertrasactionhistory',
            name='coin_mined',
            field=models.FloatField(verbose_name='Coinmined'),
        ),
    ]
