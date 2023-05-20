from django import forms
from django.contrib.auth.models import User
from . models import Profile


# # Profile
class CreateProfile(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}),label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}),label='Confirm Password')
    referral = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),label='Referral (optional)',required=False)
    class Meta:
        model = Profile
        fields = ['username', 'email', 'password', 'password2', 'referral']
        
class UpdateUser(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ['username', 'email']

class UpdateProfile(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = Profile
        fields = ['username', 'email', 'profile_pic']
        widgets = {
            'profile_pic':forms.FileInput(attrs={'class':'form-control'}),
        }


# # Dashboard
class UpdateBTCWal(forms.ModelForm):
    user_wal_btc = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = Profile
        fields = ['user_wal_btc',]
class UpdateETHWal(forms.ModelForm):
    user_wal_eth = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = Profile
        fields = ['user_wal_eth',]
class UpdateDGEWal(forms.ModelForm):
    user_wal_doge = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = Profile
        fields = ['user_wal_doge',]
class UpdateLTEWal(forms.ModelForm):
    user_wal_lite = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = Profile
        fields = ['user_wal_lite',]


# # Investment
class selectNetwork(forms.ModelForm):
    CHOICES = [("1", "Bitcoin"), ("2", "Ethereum"), ("3", "Dogecoin"), ("4", "Litecoin")]
    selected_network = forms.ChoiceField(widget=forms.RadioSelect(), choices=CHOICES)
    invested_amount = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control', 'id':'ivstnetwork'}), label='Deposit amount - (minimum of $50)')
    class Meta:
        model = Profile
        fields = ['selected_network', 'invested_amount']


# # Withdrawal
WITHDRAW_CHOICES = [("BTC", "Bitcoin"), ("ETH", "Ethereum"), ("DOGE", "Dogecoin"), ("LTC", "Litecoin")]
class withdrawForm(forms.ModelForm):
    network = forms.ChoiceField(widget=forms.RadioSelect(), choices=WITHDRAW_CHOICES, label='Choose Network')
    withdrawal_amount = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    class Meta:
        model = Profile
        fields = ['network', 'withdrawal_amount']



# # PLANS
# # PLANS

# Bronze
class bronze_form(forms.ModelForm):
    CHOICES = [("1", "Bitcoin"), ("2", "Ethereum"), ("3", "Dogecoin"), ("4", "Litecoin")]
    selected_network = forms.ChoiceField(widget=forms.RadioSelect(), choices=CHOICES)
    invested_amount = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control', 'id':'bronzeform'}), label='Deposit amount')
    class Meta:
        model = Profile
        fields = ['selected_network', 'invested_amount']

# Silver
class silver_form(forms.ModelForm):
    CHOICES = [("1", "Bitcoin"), ("2", "Ethereum"), ("3", "Dogecoin"), ("4", "Litecoin")]
    selected_network = forms.ChoiceField(widget=forms.RadioSelect(), choices=CHOICES)
    invested_amount = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control', 'id':'silverform'}), label='Deposit amount')
    class Meta:
        model = Profile
        fields = ['selected_network', 'invested_amount']

# Gold
class gold_form(forms.ModelForm):
    CHOICES = [("1", "Bitcoin"), ("2", "Ethereum"), ("3", "Dogecoin"), ("4", "Litecoin")]
    selected_network = forms.ChoiceField(widget=forms.RadioSelect(), choices=CHOICES)
    invested_amount = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control', 'id':'goldform'}), label='Deposit amount')
    class Meta:
        model = Profile
        fields = ['selected_network', 'invested_amount']

# Platinum
class platinum_form(forms.ModelForm):
    CHOICES = [("1", "Bitcoin"), ("2", "Ethereum"), ("3", "Dogecoin"), ("4", "Litecoin")]
    selected_network = forms.ChoiceField(widget=forms.RadioSelect(), choices=CHOICES)
    invested_amount = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control', 'id':'platinumform'}), label='Deposit amount')
    class Meta:
        model = Profile
        fields = ['selected_network', 'invested_amount']

# Sapphire
class sapphire_form(forms.ModelForm):
    CHOICES = [("1", "Bitcoin"), ("2", "Ethereum"), ("3", "Dogecoin"), ("4", "Litecoin")]
    selected_network = forms.ChoiceField(widget=forms.RadioSelect(), choices=CHOICES)
    invested_amount = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control', 'id':'sapphireform'}), label='Deposit amount')
    class Meta:
        model = Profile
        fields = ['selected_network', 'invested_amount']

# Diamond
class diamond_form(forms.ModelForm):
    CHOICES = [("1", "Bitcoin"), ("2", "Ethereum"), ("3", "Dogecoin"), ("4", "Litecoin")]
    selected_network = forms.ChoiceField(widget=forms.RadioSelect(), choices=CHOICES)
    invested_amount = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control', 'id':'diamondform'}), label='Deposit amount')
    class Meta:
        model = Profile
        fields = ['selected_network', 'invested_amount']



