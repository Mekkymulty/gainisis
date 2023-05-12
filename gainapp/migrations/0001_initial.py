# Generated by Django 4.1.7 on 2023-05-08 15:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Crypto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crypto_network', models.CharField(max_length=50, null=True)),
                ('crypto_code', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Withdraw',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trans_type', models.CharField(choices=[('Investment', 'Investment'), ('Withdrawal', 'Withdrawal')], max_length=255)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('created_time', models.TimeField(auto_now_add=True, null=True)),
                ('trans_status', models.CharField(choices=[('Pending', 'Pending'), ('Successful', 'Successful'), ('Failed', 'Failed')], default='Pending', max_length=255)),
                ('trans_amount', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255, unique=True)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='profile')),
                ('referral', models.CharField(blank=True, max_length=255, null=True)),
                ('user_wal', models.CharField(blank=True, max_length=255, null=True)),
                ('user_balance', models.CharField(blank=True, default='0', max_length=255, null=True)),
                ('select_network', models.CharField(choices=[('ni738', 'Bitcoin'), ('89274ygu', 'Ethereum'), ('03jisf', 'Dodgecoin')], default='ni738', max_length=255)),
                ('user_withdrawal', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
