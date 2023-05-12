from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.contrib.auth.models import User

from . models import *
from . forms import *


def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    form = CreateProfile()

    if request.method == 'POST':
        forms = CreateProfile(request.POST)

        if forms.is_valid():
            username = forms.cleaned_data.get('username')
            email = forms.cleaned_data.get('email')
            password = forms.cleaned_data.get('password')
            password2 = forms.cleaned_data.get('password2')

            if User.objects.filter(username = username).exists():
                messages.warning(request, 'Username already exist.')
                return redirect('register')
            if User.objects.filter(email = email).exists():
                messages.warning(request, 'Email already exist.')
                return redirect('register')
            if password != password2:
                messages.warning(request, 'Password does not match.')
                return redirect('register')

            user = User.objects.create_user(username, email, password)
            forms = forms.save(commit=False)
            forms.user = user
            forms.save()

            login(request, user)
            messages.success(request, 'Welcome to Gainisis.')
            
            return redirect('index')

    context={
        'form':form
    }
    return render(request, 'gainisis/authentication/register.html', context)


def loginuser(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('lgnuname')
        password = request.POST.get('loginpsw')

        user = authenticate(username = username, password = password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('index')
        else:
            messages.warning(request, 'Username or password is incorrect')
            return redirect('login')

    return render(request, 'gainisis/authentication/login.html')


@login_required(login_url=('login'))
def update_profile(request):
    Profile = request.user.profile
    form = UpdateProfile(instance=Profile)

    if request.method == 'POST':
        user_forms = UpdateUser(request.POST, instance=request.user)
        forms = UpdateProfile(request.POST, request.FILES, instance=Profile)

        if forms.is_valid():
            user_forms.save()
            forms.save()
            messages.success(request, 'Account updated.')
            return redirect('account')

    context={
        'form':form,
    }
    return render(request, 'gainisis/authentication/update_user.html', context)


def logoutuser(request):
    logout(request)
    return redirect('index')





def index(request):
    if request.user.is_authenticated:
        user = request.user.profile
    else:
        user = request.user
    
    team = Team.objects.all()
    
    context = {
        'profile':user,
        'team':team,
    }
    return render(request, 'gainisis/index.html', context)


@login_required(login_url=('login'))
def account(request):
    user = request.user.profile
    crypto = Crypto.objects.all()
    btc_crypto = Crypto.objects.all().filter(crypto_network='Bitcoin')
    eth_crypto = Crypto.objects.all().filter(crypto_network='Ethereum')
    lte_crypto = Crypto.objects.all().filter(crypto_network='Litecoin')
    dge_crypto = Crypto.objects.all().filter(crypto_network='Dogecoin')

    formbtc = UpdateBTCWal(instance=user)
    formeth = UpdateETHWal(instance=user)
    formlte = UpdateLTEWal(instance=user)
    formdge = UpdateDGEWal(instance=user)

    transact = Transaction.objects.all().filter(investor=user).order_by('created_at')[::-1][:5]

    if request.method == 'POST':
        forms_btc = UpdateBTCWal(request.POST, instance=user)
        forms_eth = UpdateETHWal(request.POST, instance=user)
        forms_lte = UpdateLTEWal(request.POST, instance=user)
        forms_dge = UpdateDGEWal(request.POST, instance=user)

        if forms_btc.is_valid():
            forms_btc.save()
            return redirect('account')
        if forms_eth.is_valid():
            forms_eth.save()
            return redirect('account')
        if forms_lte.is_valid():
            forms_lte.save()
            return redirect('account')
        if forms_dge.is_valid():
            forms_dge.save()
            return redirect('account')

    context={
        'profile':user,
        'crypto':crypto,

        'btc_crypto':btc_crypto,
        'eth_crypto':eth_crypto,
        'lte_crypto':lte_crypto,
        'dge_crypto':dge_crypto,

        'formbtc':formbtc,
        'formeth':formeth,
        'formlte':formlte,
        'formdge':formdge,

        'transactions':transact,
    }
    return render(request, 'gainisis/account.html', context)


@login_required(login_url=('login'))
def invest(request):
    user = request.user.profile
    ntw_form = selectNetwork(instance=user)

    scan_bitcoin = Crypto.objects.filter(crypto_network='Bitcoin')
    scan_ethereum = Crypto.objects.filter(crypto_network='Ethereum')
    scan_dogecoin = Crypto.objects.filter(crypto_network='Dogecoin')
    scan_litecoin = Crypto.objects.filter(crypto_network='Litecoin')
        
    if request.method == 'POST':
        forms = selectNetwork(request.POST, instance=user)
        
        if forms.is_valid():
            invt_network = forms.cleaned_data.get('select_network')

            if invt_network == '1':
                if user.user_wal_btc is None:
                    messages.warning(request, 'You have no Bitcoin wallet in your account.')
                    return redirect('invest')
                else:
                    user.selected_wallet = Crypto.objects.filter(crypto_network='Bitcoin').values_list('crypto_network')
                    user.selected_code = Crypto.objects.filter(crypto_network='Bitcoin').values_list('crypto_code')
                    forms.save()
                    return redirect('invest')
            if invt_network == '2':
                if user.user_wal_eth is None:
                    messages.warning(request, 'You have no Ethereum wallet in your account.')
                    return redirect('invest')
                else:
                    user.selected_wallet = Crypto.objects.filter(crypto_network='Ethereum').values_list('crypto_network')
                    user.selected_code = Crypto.objects.filter(crypto_network='Ethereum').values_list('crypto_code')
                    forms.save()
                    return redirect('invest')
            if invt_network == '3':
                if user.user_wal_doge is None:
                    messages.warning(request, 'You have no Dogecoin wallet in your account.')
                    return redirect('invest')
                else:
                    user.selected_wallet = Crypto.objects.filter(crypto_network='Dogecoin').values_list('crypto_network')
                    user.selected_code = Crypto.objects.filter(crypto_network='Dogecoin').values_list('crypto_code')
                    forms.save()
                    return redirect('invest')
            if invt_network == '4':
                if user.user_wal_lite is None:
                    messages.warning(request, 'You have no Litecoin wallet in your account.')
                    return redirect('invest')
                else:
                    user.selected_wallet = Crypto.objects.filter(crypto_network='Litecoin').values_list('crypto_network')
                    user.selected_code = Crypto.objects.filter(crypto_network='Litecoin').values_list('crypto_code')
                    forms.save()
                    return redirect('invest')
                
    context={
        'profile':user,
        'form':ntw_form,

        'scan_bitcoin':scan_bitcoin,
        'scan_ethereum':scan_ethereum,
        'scan_dogecoin':scan_dogecoin,
        'scan_litecoin':scan_litecoin,
    }
    return render(request, 'gainisis/invest.html', context)


@login_required(login_url=('login'))
def withdraw(request):
    user = request.user.profile
    form = withdrawForm()

    if request.method == 'POST':
        forms = withdrawForm(request.POST, instance=user)
        if forms.is_valid():
            wd_network = forms.cleaned_data.get('network')
            wd_form = forms.cleaned_data.get('withdrawal_amount')
            wd_balance = user.user_balance
            if wd_balance == None:
                wd_balance = 0

            int_form = int(wd_form)
            int_bal = int(wd_balance)
            bal_wdw = int_bal - int_form

            if int_bal == 0:
                messages.warning(request, 'Your wallet is empty, invest to gain more profits.')
                return redirect('invest')
            elif int_form > int_bal:
                messages.warning(request, 'Amount is greater than your balance.')
                return redirect('withdraw')
            else:
                user.user_balance = bal_wdw

                if wd_network == 'BTC':
                    if user.user_wal_btc is None:
                        messages.warning(request, f'You have no Bitcoin wallet in your account.')
                        return redirect('withdraw')
                    else:
                        trans = Transaction.objects.create(investor=user, trans_type='Withdrawal', network='BTC', trans_status='Pending', trans_amount=int_form)
                        forms.user = trans
                        messages.success(request, f'Your withdrawal request of ${wd_form} was submitted. Your balance is ${bal_wdw}')
                        forms.save()
                        return redirect('account')
                if wd_network == 'ETH':
                    if user.user_wal_eth is None:
                        messages.warning(request, f'You have no Ethereum wallet in your account.')
                        return redirect('withdraw')
                    else:
                        trans = Transaction.objects.create(investor=user, trans_type='Withdrawal', network='ETH', trans_status='Pending', trans_amount=int_form)
                        forms.user = trans
                        messages.success(request, f'Your withdrawal request of ${wd_form} was submitted. Your balance is ${bal_wdw}')
                        forms.save()
                        return redirect('account')
                if wd_network == 'DOGE':
                    if user.user_wal_doge is None:
                        messages.warning(request, f'You have no Dogecoin wallet in your account.')
                        return redirect('withdraw')
                    else:
                        trans = Transaction.objects.create(investor=user, trans_type='Withdrawal', network='DOGE', trans_status='Pending', trans_amount=int_form)
                        forms.user = trans
                        messages.success(request, f'Your withdrawal request of ${wd_form} was submitted. Your balance is ${bal_wdw}')
                        forms.save()
                        return redirect('account')
                if wd_network == 'LTC':
                    if user.user_wal_lite is None:
                        messages.warning(request, f'You have no Litecoin wallet in your account.')
                        return redirect('withdraw')
                    else:
                        trans = Transaction.objects.create(investor=user, trans_type='Withdrawal', network='LTC', trans_status='Pending', trans_amount=int_form)
                        forms.user = trans
                        messages.success(request, f'Your withdrawal request of ${wd_form} was submitted. Your balance is ${bal_wdw}')
                        forms.save()
                        return redirect('account')

    context={
        'profile':user,
        'form':form,
    }
    return render(request, 'gainisis/withdraw.html', context)


def transactions(request):
    return render(request, 'gainisis/transactions.html')


def plans(request):
    return render(request, 'gainisis/plans.html')




def how(request):
    return render(request, 'gainisis/how.html')

def terms(request):
    return render(request, 'gainisis/terms.html')

def about(request):
    return render(request, 'gainisis/about.html')



