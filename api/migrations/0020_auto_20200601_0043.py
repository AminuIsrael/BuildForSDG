# Generated by Django 2.2.10 on 2020-06-01 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_auto_20200529_0252'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercoins',
            name='minerID',
            field=models.CharField(default=0, max_length=500, unique=True, verbose_name='miner_ID'),
        ),
        migrations.DeleteModel(
            name='LeaderBoard',
        ),
    ]
