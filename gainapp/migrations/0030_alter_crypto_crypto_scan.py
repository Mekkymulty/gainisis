# Generated by Django 4.1.7 on 2023-05-10 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gainapp', '0029_crypto_crypto_scan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crypto',
            name='crypto_scan',
            field=models.ImageField(null=True, upload_to='crypto'),
        ),
    ]
