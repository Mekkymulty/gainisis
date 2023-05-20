from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# # Profiles
USER_CHOICES = [("1", "Bitcoin"), ("2", "Ethereum"), ("3", "Dogecoin"), ("4", "Litecoin")]
PLAN_CHOICES = [("Bronze Plan", "Bronze"), ("Silver Plan", "Silver"), ("Gold Plan", "Gold"), ("Platinum Plan", "Platinum"), ("Sapphire Plan", "Sapphire"), ("Diamond Plan", "Diamond")]
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    profile_pic = models.ImageField(upload_to='profile', null=True, blank=True)
    referral = models.CharField(max_length=255, null=True, blank=True)
    user_wal_btc = models.CharField(max_length=255, null=True, blank=True)
    user_wal_eth = models.CharField(max_length=255, null=True, blank=True)
    user_wal_doge = models.CharField(max_length=255, null=True, blank=True)
    user_wal_lite = models.CharField(max_length=255, null=True, blank=True)
    user_balance = models.CharField(max_length=255, default='0', null=True, blank=True)
    
    selected_network = models.CharField(max_length=255, choices=USER_CHOICES, null=True, blank=True)
    selected_wallet = models.CharField(max_length=255, choices=USER_CHOICES, null=True, blank=True)
    selected_code = models.CharField(max_length=255, choices=USER_CHOICES, null=True, blank=True)
    invested_amount = models.CharField(max_length=255, null=True, blank=True)
    crypto_value = models.DecimalField(max_digits=24, decimal_places=7, default=0)
    selected_plan = models.CharField(max_length=255, choices=PLAN_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.username
    
# # Cryptos
class Crypto(models.Model):
    crypto_network = models.CharField(max_length=255, null=True)
    market_value = models.CharField(max_length=1000, null=True, default=0)
    crypto_code = models.CharField(max_length=255, null=True)
    crypto_scan = models.ImageField(upload_to='crypto', null=True, blank=True)

    def __str__(self):
        return self.crypto_network
    

# # Plans
PLAN_CHOICES = [("Bronze", "Bronze"), ("Silver", "Silver"), ("Gold", "Gold"), ("Platinum", "Platinum"), ("Sapphire", "Sapphire"), ("Diamond", "Diamond"),]
class Plan(models.Model):
    plan_title = models.CharField(max_length=255, choices=PLAN_CHOICES, null=True)
    plan_image = models.ImageField(upload_to='plans', null=True)

    prize = models.CharField(max_length=255, null=True)
    duration = models.CharField(max_length=255, null=True)
    interest = models.DecimalField(max_digits=9, decimal_places=1, default=0)
    interest_duation = models.CharField(max_length=225, null=True, default='weekly')
    referral = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.plan_title

# # Transactions
TYPE_CHOICES = [("Investment", "Investment"), ("Withdrawal", "Withdrawal")]
NETWORK_CHOICES = [("BTC", "Btc"), ("ETH", "Eth"), ("DOGE", "Doge"), ("LTC", "Lite")]
STATUS_CHOICES = [("Successful", "Successful"), ("Pending", "Pending"), ("Failed", "Failed")]
class Transaction(models.Model):
    investor = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    trans_type = models.CharField(max_length=255, choices=TYPE_CHOICES, default='Investment')
    network = models.CharField(max_length=255, choices=NETWORK_CHOICES)
    created_at = models.DateField(auto_now_add=True)
    created_time = models.TimeField(auto_now_add=True, null=True)
    trans_status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='Successful')
    trans_amount = models.CharField(max_length=255)
    crypto_val = models.DecimalField(max_digits=24, decimal_places=7, default=0)

    def __str__(self):
        return f'{str(self.created_at)}____-____{self.investor}____({self.trans_type} ({self.network}) - ${str(self.trans_amount)})____//____{str(self.trans_status)}'


# # Our Team
class Team(models.Model):
    team_picture = models.ImageField(upload_to='team', null=True)
    team_name = models.CharField(max_length=255, null=True)
    team_comment = models.TextField(max_length=900, null=True)

    def __str__(self):
        return self.team_name
    

