# Generated by Django 4.2.5 on 2023-10-18 12:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('send_gmail', '0024_alter_trade_request_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trade_request',
            old_name='id',
            new_name='obj_user',
        ),
    ]