# Generated by Django 4.1.7 on 2023-05-20 17:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gainapp', '0006_remove_profile_new_message_support_new_message'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Support',
        ),
    ]
