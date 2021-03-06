# Generated by Django 2.2.10 on 2020-06-03 20:20

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_auto_20200601_0107'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_name', models.TextField(max_length=150, unique=True, verbose_name='Account Name')),
                ('account_number', models.TextField(max_length=150, unique=True, verbose_name='Account Number')),
                ('bank_name', models.TextField(max_length=150, verbose_name='Bank Name')),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.User')),
            ],
            options={
                'db_table': 'Account Details',
            },
        ),
    ]
