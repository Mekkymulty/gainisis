# Generated by Django 4.1.7 on 2023-05-11 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gainapp', '0056_alter_crypto_crypto_scan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crypto',
            name='crypto_scan',
            field=models.ImageField(blank=True, null=True, upload_to='crypto'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='network_image',
            field=models.CharField(blank=True, max_length=225, null=True),
        ),
    ]
