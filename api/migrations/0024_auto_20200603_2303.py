# Generated by Django 2.2.10 on 2020-06-03 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_otp_otp_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='otp',
            name='validated',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='otp',
            name='otp_code',
            field=models.TextField(max_length=20, verbose_name='OTP CODE'),
        ),
    ]
