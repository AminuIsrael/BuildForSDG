# Generated by Django 2.2.10 on 2020-06-05 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_auto_20200603_2303'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertrasactionhistory',
            name='coin_allocated_to',
            field=models.TextField(default=0, verbose_name='Miner_ID'),
        ),
    ]
