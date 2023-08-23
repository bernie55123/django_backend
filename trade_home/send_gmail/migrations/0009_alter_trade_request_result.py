# Generated by Django 4.2.1 on 2023-08-17 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('send_gmail', '0008_rename_gmail_trade_request'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade_request',
            name='result',
            field=models.CharField(blank=True, choices=[('None', ' '), ('True', '通過'), ('False', '不通過')], default=None, max_length=10000, verbose_name='解果'),
        ),
    ]