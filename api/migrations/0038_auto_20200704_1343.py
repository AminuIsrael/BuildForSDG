# Generated by Django 2.2.10 on 2020-07-04 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0037_auto_20200704_1338'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_LGA',
            field=models.TextField(default='', max_length=200, verbose_name='LGA'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_state',
            field=models.TextField(default='', max_length=200, verbose_name='State'),
        ),
    ]