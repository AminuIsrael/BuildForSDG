# Generated by Django 2.2.10 on 2020-06-07 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0030_agentcoins'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercoins',
            name='balance',
            field=models.FloatField(default=0, verbose_name='balance'),
        ),
    ]
