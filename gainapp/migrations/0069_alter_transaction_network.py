# Generated by Django 4.1.7 on 2023-05-11 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gainapp', '0068_alter_team_team_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='network',
            field=models.CharField(choices=[('Btc', 'Btc'), ('Eth', 'Eth'), ('Dodge', 'Dodge'), ('LTC', 'Lite')], max_length=255),
        ),
    ]
