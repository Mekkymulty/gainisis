# Generated by Django 4.1.7 on 2023-05-09 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gainapp', '0025_remove_profile_select_network'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='select_network',
            field=models.CharField(choices=[('1', 'Bitcoin'), ('2', 'Ethereum'), ('3', 'Dodgecoin')], default='1', max_length=255),
        ),
    ]
