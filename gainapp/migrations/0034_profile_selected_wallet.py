# Generated by Django 4.1.7 on 2023-05-10 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gainapp', '0033_profile_selected_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='selected_wallet',
            field=models.CharField(blank=True, choices=[('1', 'Bitcoin'), ('2', 'Ethereum'), ('3', 'Dodgecoin'), ('4', 'Litecoin')], max_length=255, null=True),
        ),
    ]
