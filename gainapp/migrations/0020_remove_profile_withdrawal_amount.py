# Generated by Django 4.1.7 on 2023-05-09 20:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gainapp', '0019_rename_trans_network_transaction_network'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='withdrawal_amount',
        ),
    ]
