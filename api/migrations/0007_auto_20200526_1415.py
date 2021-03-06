# Generated by Django 2.2.10 on 2020-05-26 14:15

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20200522_2301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaderboard',
            name='minedCoins',
            field=models.FloatField(default=0, verbose_name='mined_Coins'),
        ),
        migrations.AlterField(
            model_name='usercoins',
            name='allocateWasteCoin',
            field=models.FloatField(default=0, verbose_name='AllocatedWasteCoin'),
        ),
        migrations.AlterField(
            model_name='usercoins',
            name='minedCoins',
            field=models.FloatField(default=0, verbose_name='minedCoins'),
        ),
        migrations.CreateModel(
            name='UserTrasactionHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(verbose_name='CoinAmount')),
                ('transaction', models.TextField(max_length=10, verbose_name='Transactions')),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.User')),
            ],
            options={
                'db_table': 'Transaction_History',
            },
        ),
    ]
