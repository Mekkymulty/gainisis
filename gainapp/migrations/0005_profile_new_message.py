# Generated by Django 4.1.7 on 2023-05-17 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gainapp', '0004_alter_profile_crypto_value_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='new_message',
            field=models.BooleanField(default=False),
        ),
    ]
