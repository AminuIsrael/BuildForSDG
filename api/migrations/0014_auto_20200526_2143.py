# Generated by Django 2.2.10 on 2020-05-26 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_auto_20200526_2141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertrasactionhistory',
            name='coin_mined',
            field=models.FloatField(default=0, verbose_name='Coinmined'),
        ),
    ]
