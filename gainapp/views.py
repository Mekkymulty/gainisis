
# import date
# named_tuple = time.localtime()
# time_string = time.strftime("%H:%M:%S", named_tuple)# import time
# from itertools import count
# from multiprocessing import Process

from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.contrib.auth.models import User

from . models import *
from . forms import *

import re




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
    
    plans = Plan.objects.all()
    team = Team.objects.all()

    # notify = Support.objects.all().filter(chat_profile=user).values_list('new_message').last()
    # if notify is True:
    #     messages.warning(request, 'True')
    # else:
    #     messages.warning(request, 'False')
    
    context = {
        'profile':user,
        'plans':plans,
        'team':team,
    }
    return render(request, 'gainisis/index.html', context)

@login_required(login_url=('login'))
def account(request):
    user = request.user.profile
    crypto = Crypto.objects.all()

    formbtc = UpdateBTCWal(instance=user)
    formeth = UpdateETHWal(instance=user)
    formlte = UpdateLTEWal(instance=user)
    formdge = UpdateDGEWal(instance=user)

    btc_crypto = Crypto.objects.all().filter(crypto_network='Bitcoin')
    eth_crypto = Crypto.objects.all().filter(crypto_network='Ethereum')
    lte_crypto = Crypto.objects.all().filter(crypto_network='Litecoin')
    dge_crypto = Crypto.objects.all().filter(crypto_network='Dogecoin')

    transact = Transaction.objects.all().filter(investor=user).order_by('created_at')[::-1][:5]
    gt_tr = len(Transaction.objects.all().filter(investor=user))

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

        'formbtc':formbtc,
        'formeth':formeth,
        'formlte':formlte,
        'formdge':formdge,

        'btc_crypto':btc_crypto,
        'eth_crypto':eth_crypto,
        'lte_crypto':lte_crypto,
        'dge_crypto':dge_crypto,

        'transactions':transact,
        'gt_tr':gt_tr,
    }
    return render(request, 'gainisis/account.html', context)

@login_required(login_url=('login'))
def invest(request):
    user = request.user.profile
    user.invested_amount = None
    instance_ntw_form = selectNetwork(instance=user)
    
        
    if request.method == 'POST':
        forms = selectNetwork(request.POST, instance=user)
        
        if forms.is_valid():
            invt_network = forms.cleaned_data.get('selected_network')
            dr_form = forms.cleaned_data.get('invested_amount')
            
            user.selected_plan = None

            if invt_network == '1':
                if user.user_wal_btc is None:
                    messages.warning(request, 'You have no Bitcoin wallet in your account.')
                    return redirect('invest')
                else:
                    BTC_market = Crypto.objects.filter(crypto_network='Bitcoin').values_list('market_value')
                    x = re.findall(r'\d+\.\d+', str(BTC_market))
                    BTC_value = int(dr_form) / float(x[0])

                    user.crypto_value = BTC_value
                    trans = Transaction.objects.create(investor=user, trans_type='Investment', network='BTC', trans_status='Pending', trans_amount=dr_form, crypto_val=BTC_value)
                    
                    user.selected_wallet = Crypto.objects.filter(crypto_network='Bitcoin').values_list('crypto_network')
                    user.selected_code = Crypto.objects.filter(crypto_network='Bitcoin').values_list('crypto_code')

                    forms.user = trans
                    forms.save()
                    return redirect('bitcoin')
                
            if invt_network == '2':
                if user.user_wal_eth is None:
                    messages.warning(request, 'You have no Ethereum wallet in your account.')
                    return redirect('invest')
                else:
                    ETH_market = Crypto.objects.filter(crypto_network='Ethereum').values_list('market_value')
                    x = re.findall(r'\d+\.\d+', str(ETH_market))
                    ETH_value = int(dr_form) / float(x[0])

                    user.crypto_value = ETH_value
                    trans = Transaction.objects.create(investor=user, trans_type='Investment', network='ETH', trans_status='Pending', trans_amount=dr_form, crypto_val=ETH_value)

                    user.selected_wallet = Crypto.objects.filter(crypto_network='Ethereum').values_list('crypto_network')
                    user.selected_code = Crypto.objects.filter(crypto_network='Ethereum').values_list('crypto_code')
                    
                    forms.user = trans
                    forms.save()
                    return redirect('ethereum')
                
            if invt_network == '3':
                if user.user_wal_doge is None:
                    messages.warning(request, 'You have no Dogecoin wallet in your account.')
                    return redirect('invest')
                else:
                    DOGE_market = Crypto.objects.filter(crypto_network='Dogecoin').values_list('market_value')
                    x = re.findall(r'\d+\.\d+', str(DOGE_market))
                    DOGE_value = int(dr_form) / float(x[0])

                    user.crypto_value = DOGE_value
                    trans = Transaction.objects.create(investor=user, trans_type='Investment', network='DOGE', trans_status='Pending', trans_amount=dr_form, crypto_val=DOGE_value)

                    user.selected_wallet = Crypto.objects.filter(crypto_network='Dogecoin').values_list('crypto_network')
                    user.selected_code = Crypto.objects.filter(crypto_network='Dogecoin').values_list('crypto_code')

                    forms.user = trans
                    forms.save()
                    return redirect('dogecoin')
                
            if invt_network == '4':
                if user.user_wal_lite is None:
                    messages.warning(request, 'You have no Litecoin wallet in your account.')
                    return redirect('invest')
                else:
                    LTC_market = Crypto.objects.filter(crypto_network='Litecoin').values_list('market_value')
                    x = re.findall(r'\d+\.\d+', str(LTC_market))
                    LTC_value = int(dr_form) / float(x[0])

                    user.crypto_value = LTC_value
                    trans = Transaction.objects.create(investor=user, trans_type='Investment', network='LTC', trans_status='Pending', trans_amount=dr_form, crypto_val=LTC_value)
                    
                    user.selected_wallet = Crypto.objects.filter(crypto_network='Litecoin').values_list('crypto_network')
                    user.selected_code = Crypto.objects.filter(crypto_network='Litecoin').values_list('crypto_code')

                    forms.user = trans
                    forms.save()
                    return redirect('litecoin')
                
    context={
        'profile':user,
        'form_instance':instance_ntw_form,
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
                        BTC_market = Crypto.objects.filter(crypto_network='Bitcoin').values_list('market_value')
                        x = re.findall(r'\d+\.\d+', str(BTC_market))
                        BTC_value = int(wd_form) / float(x[0])

                        user.crypto_value = BTC_value
                        trans = Transaction.objects.create(investor=user, trans_type='Withdrawal', network='BTC', trans_status='Pending', trans_amount=int_form, crypto_val=BTC_value)
                        
                        forms.user = trans
                        messages.success(request, f'Your withdrawal request of ${wd_form} was submitted. Your balance is ${bal_wdw}')
                        forms.save()
                        return redirect('account')
                if wd_network == 'ETH':
                    if user.user_wal_eth is None:
                        messages.warning(request, f'You have no Ethereum wallet in your account.')
                        return redirect('withdraw')
                    else:
                        ETH_market = Crypto.objects.filter(crypto_network='Ethereum').values_list('market_value')
                        x = re.findall(r'\d+\.\d+', str(ETH_market))
                        ETH_value = int(wd_form) / float(x[0])

                        user.crypto_value = ETH_value
                        trans = Transaction.objects.create(investor=user, trans_type='Withdrawal', network='ETH', trans_status='Pending', trans_amount=int_form, crypto_val=ETH_value)

                        forms.user = trans
                        messages.success(request, f'Your withdrawal request of ${wd_form} was submitted. Your balance is ${bal_wdw}')
                        forms.save()
                        return redirect('account')
                if wd_network == 'DOGE':
                    if user.user_wal_doge is None:
                        messages.warning(request, f'You have no Dogecoin wallet in your account.')
                        return redirect('withdraw')
                    else:
                        DOGE_market = Crypto.objects.filter(crypto_network='Dogecoin').values_list('market_value')
                        x = re.findall(r'\d+\.\d+', str(DOGE_market))
                        DOGE_value = int(wd_form) / float(x[0])

                        user.crypto_value = DOGE_value
                        trans = Transaction.objects.create(investor=user, trans_type='Withdrawal', network='DOGE', trans_status='Pending', trans_amount=int_form, crypto_val=DOGE_value)

                        forms.user = trans
                        messages.success(request, f'Your withdrawal request of ${wd_form} was submitted. Your balance is ${bal_wdw}')
                        forms.save()
                        return redirect('account')
                if wd_network == 'LTC':
                    if user.user_wal_lite is None:
                        messages.warning(request, f'You have no Litecoin wallet in your account.')
                        return redirect('withdraw')
                    else:
                        LTC_market = Crypto.objects.filter(crypto_network='Litecoin').values_list('market_value')
                        x = re.findall(r'\d+\.\d+', str(LTC_market))
                        LTC_value = int(wd_form) / float(x[0])

                        user.crypto_value = LTC_value
                        trans = Transaction.objects.create(investor=user, trans_type='Withdrawal', network='LTC', trans_status='Pending', trans_amount=int_form, crypto_val=LTC_value)

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
    user = request.user.profile

    transact = Transaction.objects.all().filter(investor=user).order_by('created_at')[::-1]
    
    context={
        'transact':transact,
    }
    return render(request, 'gainisis/transactions.html', context)


def plans(request):
    plan_id = Plan.objects.all()

    context = {
        'plan_id':plan_id,
    }
    return render(request, 'gainisis/plans.html', context)


@login_required(login_url=('login'))
def bronze(request):
    user = request.user.profile
    user.invested_amount = None
    plan_form = bronze_form(instance=user)

    plan_id = Plan.objects.all().filter(plan_title='Bronze')
    
    if request.method == 'POST':
        forms = bronze_form(request.POST, instance=user)
        if forms.is_valid():
            invt_network = forms.cleaned_data.get('selected_network')
            dr_form = forms.cleaned_data.get('invested_amount')

            user_plan = Plan.objects.filter(plan_title='Bronze').values_list('plan_title')
            user.selected_plan = user_plan
            
            if invt_network == '1':
                if user.user_wal_btc is None:
                    messages.warning(request, 'You have no Bitcoin wallet in your account.')
                    return redirect('bronze')
                else:
                    BTC_market = Crypto.objects.filter(crypto_network='Bitcoin').values_list('market_value')
                    x = re.findall(r'\d+\.\d+', str(BTC_market))
                    BTC_value = int(dr_form) / float(x[0])

                    user.crypto_value = BTC_value
                    trans = Transaction.objects.create(investor=user, trans_type='Investment', network='BTC', trans_status='Pending', trans_amount=dr_form, crypto_val=BTC_value)
                    
                    user.selected_wallet = Crypto.objects.filter(crypto_network='Bitcoin').values_list('crypto_network')
                    user.selected_code = Crypto.objects.filter(crypto_network='Bitcoin').values_list('crypto_code')

                    forms.user = trans
                    forms.save()
                    return redirect('bitcoin')
                
            if invt_network == '2':
                if user.user_wal_eth is None:
                    messages.warning(request, 'You have no Ethereum wallet in your account.')
                    return redirect('bronze')
                else:
                    ETH_market = Crypto.objects.filter(crypto_network='Ethereum').values_list('market_value')
                    x = re.findall(r'\d+\.\d+', str(ETH_market))
                    ETH_value = int(dr_form) / float(x[0])

                    user.crypto_value = ETH_value
                    trans = Transaction.objects.create(investor=user, trans_type='Investment', network='ETH', trans_status='Pending', trans_amount=dr_form, crypto_val=ETH_value)

                    user.selected_wallet = Crypto.objects.filter(crypto_network='Ethereum').values_list('crypto_network')
                    user.selected_code = Crypto.objects.filter(crypto_network='Ethereum').values_list('crypto_code')
                    
                    forms.user = trans
                    forms.save()
                    return redirect('ethereum')
                
            if invt_network == '3':
                if user.user_wal_doge is None:
                    messages.warning(request, 'You have no Dogecoin wallet in your account.')
                    return redirect('bronze')
                else:
                    DOGE_market = Crypto.objects.filter(crypto_network='Dogecoin').values_list('market_value')
                    x = re.findall(r'\d+\.\d+', str(DOGE_market))
                    DOGE_value = int(dr_form) / float(x[0])

                    user.crypto_value = DOGE_value
                    trans = Transaction.objects.create(investor=user, trans_type='Investment', network='DOGE', trans_status='Pending', trans_amount=dr_form, crypto_val=DOGE_value)
                    
                    user.selected_wallet = Crypto.objects.filter(crypto_network='Dogecoin').values_list('crypto_network')
                    user.selected_code = Crypto.objects.filter(crypto_network='Dogecoin').values_list('crypto_code')

                    forms.user = trans
                    forms.save()
                    return redirect('dogecoin')
                
            if invt_network == '4':
                if user.user_wal_lite is None:
                    messages.warning(request, 'You have no Litecoin wallet in your account.')
                    return redirect('bronze')
                else:
                    LTC_market = Crypto.objects.filter(crypto_network='Litecoin').values_list('market_value')
                    x = re.findall(r'\d+\.\d+', str(LTC_market))
                    LTC_value = int(dr_form) / float(x[0])

                    user.crypto_value = LTC_value
                    trans = Transaction.objects.create(investor=user, trans_type='Investment', network='LTC', trans_status='Pending', trans_amount=dr_form, crypto_val=LTC_value)
                    
                    user.selected_wallet = Crypto.objects.filter(crypto_network='Litecoin').values_list('crypto_network')
                    user.selected_code = Crypto.objects.filter(crypto_network='Litecoin').values_list('crypto_code')

                    forms.user = trans
                    forms.save()
                    return redirect('litecoin')
                

    context = {
        'plan_form':plan_form,
        'plan_id':plan_id,
    }
    return render(request, 'gainisis/plans/bronze.html', context)

@login_required(login_url=('login'))
def silver(request):
    user = request.user.profile
    user.invested_amount = None
    plan_form = silver_form(instance=user)

    plan_id = Plan.objects.all().filter(plan_title='Silver')
    
    if request.method == 'POST':
        forms = silver_form(request.POST, instance=user)
        if forms.is_valid():
            invt_network = forms.cleaned_data.get('selected_network')
            dr_form = forms.cleaned_data.get('invested_amount')

            user_plan = Plan.objects.filter(plan_title='Silver').values_list('plan_title')
            user.selected_plan = user_plan

            if invt_network == '1':
                if user.user_wal_btc is None:
                    messages.warning(request, 'You have no Bitcoin wallet in your account.')
                    return redirect('silver')
                else:
                    BTC_market = Crypto.objects.filter(crypto_network='Bitcoin').values_list('market_value')
                    x = re.findall(r'\d+\.\d+', str(BTC_market))
                    BTC_value = int(dr_form) / float(x[0])

                    user.crypto_value = BTC_value
                    trans = Transaction.objects.create(investor=user, trans_type='Investment', network='BTC', trans_status='Pending', trans_amount=dr_form, crypto_val=BTC_value)
                    
                    user.selected_wallet = Crypto.objects.filter(crypto_network='Bitcoin').values_list('crypto_network')
                    user.selected_code = Crypto.objects.filter(crypto_network='Bitcoin').values_list('crypto_code')

                    forms.user = trans
                    forms.save()
                    return redirect('bitcoin')
                
            if invt_network == '2':
                if user.user_wal_eth is None:
                    messages.warning(request, 'You have no Ethereum wallet in your account.')
                    return redirect('silver')
                else:
                    ETH_market = Crypto.objects.filter(crypto_network='Ethereum').values_list('market_value')
                    x = re.findall(r'\d+\.\d+', str(ETH_market))
                    ETH_value = int(dr_form) / float(x[0])

                    user.crypto_value = ETH_value
                    trans = Transaction.objects.create(investor=user, trans_type='Investment', network='ETH', trans_status='Pending', trans_amount=dr_form, crypto_val=ETH_value)

                    user.selected_wallet = Crypto.objects.filter(crypto_network='Ethereum').values_list('crypto_network')
                    user.selected_code = Crypto.objects.filter(crypto_network='Ethereum').values_list('crypto_code')
                    
                    forms.user = trans
                    forms.save()
                    return redirect('ethereum')
                
            if invt_network == '3':
                if user.user_wal_doge is None:
                    messages.warning(request, 'You have no Dogecoin wallet in your account.')
                    return redirect('silver')
                else:
                    DOGE_market = Crypto.objects.filter(crypto_network='Dogecoin').values_list('market_value')
                    x = re.findall(r'\d+\.\d+', str(DOGE_market))
                    DOGE_value = int(dr_form) / float(x[0])

                    user.crypto_value = DOGE_value
                    trans = Transaction.objects.create(investor=user, trans_type='Investment', network='DOGE', trans_status='Pending', trans_amount=dr_form, crypto_val=DOGE_value)
                    
                    user.selected_wallet = Crypto.objects.filter(crypto_network='Dogecoin').values_list('crypto_network')
                    user.selected_code = Crypto.objects.filter(crypto_network='Dogecoin').values_list('crypto_code')

                    forms.user = trans
                    forms.save()
                    return redirect('dogecoin')
                
            if invt_network == '4':
                if user.user_wal_lite is None:
                    messages.warning(request, 'You have no Litecoin wallet in your account.')
                    return redirect('silver')
                else:
                    LTC_market = Crypto.objects.filter(crypto_network='Litecoin').values_list('market_value')
                    x = re.findall(r'\d+\.\d+', str(LTC_market))
                    LTC_value = int(dr_form) / float(x[0])

                    user.crypto_value = LTC_value
                    trans = Transaction.objects.create(investor=user, trans_type='Investment', network='LTC', trans_status='Pending', trans_amount=dr_form, crypto_val=LTC_value)
                    
                    user.selected_wallet = Crypto.objects.filter(crypto_network='Litecoin').values_list('crypto_network')
                    user.selected_code = Crypto.objects.filter(crypto_network='Litecoin').values_list('crypto_code')

                    forms.user = trans
                    forms.save()
                    return redirect('litecoin')
                

    context = {
        'plan_form':plan_form,
        'plan_id':plan_id,
    }
    return render(request, 'gainisis/plans/silver.html', context)

@login_required(login_url=('login'))
def gold(request):
    user = request.user.profile
    user.invested_amount = None
    plan_form = gold_form(instance=user)

    plan_id = Plan.objects.all().filter(plan_title='Gold')
    
    if request.method == 'POST':
        forms = gold_form(request.POST, instance=user)
        if forms.is_valid():
            invt_network = forms.cleaned_data.get('selected_network')
            dr_form = forms.cleaned_data.get('invested_amount')

            user_plan = Plan.objects.filter(plan_title='Gold').values_list('plan_title')
            user.selected_plan = user_plan

            if invt_network == '1':
                if user.user_wal_btc is None:
                    messages.warning(request, 'You have no Bitcoin wallet in your account.')
                    return redirect('gold')
                else:
                    BTC_market = Crypto.objects.filter(crypto_network='Bitcoin').values_list('market_value')
                    x = re.findall(r'\d+\.\d+', str(BTC_market))
                    BTC_value = int(dr_form) / float(x[0])

                    user.crypto_value = BTC_value
                    trans = Transaction.objects.create(investor=user, trans_type='Investment', network='BTC', trans_status='Pending', trans_amount=dr_form, crypto_val=BTC_value)
                    
                    user.selected_wallet = Crypto.objects.filter(crypto_network='Bitcoin').values_list('crypto_network')
                    user.selected_code = Crypto.objects.filter(crypto_network='Bitcoin').values_list('crypto_code')

                    forms.user = trans
                    forms.save()
                    return redirect('bitcoin')
                
            if invt_network == '2':
                if user.user_wal_eth is None:
                    messages.warning(request, 'You have no Ethereum wallet in your account.')
                    return redirect('gold')
                else:
                    ETH_market = Crypto.objects.filter(crypto_network='Ethereum').values_list('market_value')
                    x = re.findall(r'\d+\.\d+', str(ETH_market))
                    ETH_value = int(dr_form) / float(x[0])

                    user.crypto_value = ETH_value
                    trans = Transaction.objects.create(investor=user, trans_type='Investment', network='ETH', trans_status='Pending', trans_amount=dr_form, crypto_val=ETH_value)

                    user.selected_wallet = Crypto.objects.filter(crypto_network='Ethereum').values_list('crypto_network')
                    user.selected_code = Crypto.objects.filter(crypto_network='Ethereum').values_list('crypto_code')
                    
                    forms.user = trans
                    forms.save()
                    return redirect('ethereum')
                
            if invt_network == '3':
                if user.user_wal_doge is None:
                    messages.warning(request, 'You have no Dogecoin wallet in your account.')
                    return redirect('gold')
                else:
                    DOGE_market = Crypto.objects.filter(crypto_network='Dogecoin').values_list('market_value')
                    x = re.findall(r'\d+\.\d+', str(DOGE_market))
                    DOGE_value = int(dr_form) / float(x[0])

                    user.crypto_value = DOGE_value
                    trans = Transaction.objects.create(investor=user, trans_type='Investment', network='DOGE', trans_status='Pending', trans_amount=dr_form, crypto_val=DOGE_value)
                    
                    user.selected_wallet = Crypto.objects.filter(crypto_network='Dogecoin').values_list('crypto_network')
                    user.selected_code = Crypto.objects.filter(crypto_network='Dogecoin').values_list('crypto_code')

                    forms.user = trans
                    forms.save()
                    return redirect('dogecoin')
                
            if invt_network == '4':
                if user.user_wal_lite is None:
                    messages.warning(request, 'You have no Litecoin wallet in your account.')
                    return redirect('gold')
                else:
                    LTC_market = Crypto.objects.filter(crypto_network='Litecoin').values_list('market_value')
                    x = re.findall(r'\d+\.\d+', str(LTC_market))
                    LTC_value = int(dr_form) / float(x[0])

                    user.crypto_value = LTC_value
                    trans = Transaction.objects.create(investor=user, trans_type='Investment', network='LTC', trans_status='Pending', trans_amount=dr_form, crypto_val=LTC_value)
                    
                    user.selected_wallet = Crypto.objects.filter(crypto_network='Litecoin').values_list('crypto_network')
                    user.selected_code = Crypto.objects.filter(crypto_network='Litecoin').values_list('crypto_code')

                    forms.user = trans
                    forms.save()
                    return redirect('litecoin')
                

    context = {
        'plan_form':plan_form,
        'plan_id':plan_id,
    }
    return render(request, 'gainisis/plans/gold.html', context)

@login_required(login_url=('login'))
def platinum(request):
    user = request.user.profile
    user.invested_amount = None
    plan_form = platinum_form(instance=user)

    plan_id = Plan.objects.all().filter(plan_title='Platinum')
    
    if request.method == 'POST':
        forms = platinum_form(request.POST, instance=user)
        if forms.is_valid():
            invt_network = forms.cleaned_data.get('selected_network')
            dr_form = forms.cleaned_data.get('invested_amount')

            user_plan = Plan.objects.filter(plan_title='Platinum').values_list('plan_title')
            user.selected_plan = user_plan

            if invt_network == '1':
                if user.user_wal_btc is None:
                    messages.warning(request, 'You have no Bitcoin wallet in your account.')
                    return redirect('platinum')
                else:
                    BTC_market = Crypto.objects.filter(crypto_network='Bitcoin').values_list('market_value')
                    x = re.findall(r'\d+\.\d+', str(BTC_market))
                    BTC_value = int(dr_form) / float(x[0])

                    user.crypto_value = BTC_value
                    trans = Transaction.objects.create(investor=user, trans_type='Investment', network='BTC', trans_status='Pending', trans_amount=dr_form, crypto_val=BTC_value)
                    
                    user.selected_wallet = Crypto.objects.filter(crypto_network='Bitcoin').values_list('crypto_network')
                    user.selected_code = Crypto.objects.filter(crypto_network='Bitcoin').values_list('crypto_code')

                    forms.user = trans
                    forms.save()
                    return redirect('bitcoin')
                
            if invt_network == '2':
                if user.user_wal_eth is None:
                    messages.warning(request, 'You have no Ethereum wallet in your account.')
                    return redirect('platinum')
                else:
                    ETH_market = Crypto.objects.filter(crypto_network='Ethereum').values_list('market_value')
                    x = re.findall(r'\d+\.\d+', str(ETH_market))
                    ETH_value = int(dr_form) / float(x[0])

                    user.crypto_value = ETH_value
                    trans = Transaction.objects.create(investor=user, trans_type='Investment', network='ETH', trans_status='Pending', trans_amount=dr_form, crypto_val=ETH_value)

                    user.selected_wallet = Crypto.objects.filter(crypto_network='Ethereum').values_list('crypto_network')
                    user.selected_code = Crypto.objects.filter(crypto_network='Ethereum').values_list('crypto_code')
                    
                    forms.user = trans
                    forms.save()
                    return redirect('ethereum')
                
            if invt_network == '3':
                if user.user_wal_doge is None:
                    messages.warning(request, 'You have no Dogecoin wallet in your account.')
                    return redirect('platinum')
                else:
                    DOGE_market = Crypto.objects.filter(crypto_network='Dogecoin').values_list('market_value')
                    x = re.findall(r'\d+\.\d+', str(DOGE_market))
                    DOGE_value = int(dr_form) / float(x[0])

                    user.crypto_value = DOGE_value
                    trans = Transaction.objects.create(investor=user, trans_type='Investment', network='DOGE', trans_status='Pending', trans_amount=dr_form, crypto_val=DOGE_value)
                    
                    user.selected_wallet = Crypto.objects.filter(crypto_network='Dogecoin').values_list('crypto_network')
                    user.selected_code = Crypto.objects.filter(crypto_network='Dogecoin').values_list('crypto_code')

                    forms.user = trans
                    forms.save()
                    return redirect('dogecoin')
                
            if invt_network == '4':
                if user.user_wal_lite is None:
                    messages.warning(request, 'You have no Litecoin wallet in your account.')
                    return redirect('platinum')
                else:
                    LTC_market = Crypto.objects.filter(crypto_network='Litecoin').values_list('market_value')
                    x = re.findall(r'\d+\.\d+', str(LTC_market))
                    LTC_value = int(dr_form) / float(x[0])

                    user.crypto_value = LTC_value
                    trans = Transaction.objects.create(investor=user, trans_type='Investment', network='LTC', trans_status='Pending', trans_amount=dr_form, crypto_val=LTC_value)
                    
                    user.selected_wallet = Crypto.objects.filter(crypto_network='Litecoin').values_list('crypto_network')
                    user.selected_code = Crypto.objects.filter(crypto_network='Litecoin').values_list('crypto_code')

                    forms.user = trans
                    forms.save()
                    return redirect('litecoin')
                

    context = {
        'plan_form':plan_form,
        'plan_id':plan_id,
    }
    return render(request, 'gainisis/plans/platinum.html', context)

@login_required(login_url=('login'))
def sapphire(request):
    user = request.user.profile
    user.invested_amount = None
    plan_form = sapphire_form(instance=user)

    plan_id = Plan.objects.all().filter(plan_title='Sapphire')
    
    if request.method == 'POST':
        forms = sapphire_form(request.POST, instance=user)
        if forms.is_valid():
            invt_network = forms.cleaned_data.get('selected_network')
            dr_form = forms.cleaned_data.get('invested_amount')

            user_plan = Plan.objects.filter(plan_title='Sapphire').values_list('plan_title')
            user.selected_plan = user_plan

            if invt_network == '1':
                if user.user_wal_btc is None:
                    messages.warning(request, 'You have no Bitcoin wallet in your account.')
                    return redirect('sapphire')
                else:
                    BTC_market = Crypto.objects.filter(crypto_network='Bitcoin').values_list('market_value')
                    x = re.findall(r'\d+\.\d+', str(BTC_market))
                    BTC_value = int(dr_form) / float(x[0])

                    user.crypto_value = BTC_value
                    trans = Transaction.objects.create(investor=user, trans_type='Investment', network='BTC', trans_status='Pending', trans_amount=dr_form, crypto_val=BTC_value)
                    
                    user.selected_wallet = Crypto.objects.filter(crypto_network='Bitcoin').values_list('crypto_network')
                    user.selected_code = Crypto.objects.filter(crypto_network='Bitcoin').values_list('crypto_code')

                    forms.user = trans
                    forms.save()
                    return redirect('bitcoin')
                
            if invt_network == '2':
                if user.user_wal_eth is None:
                    messages.warning(request, 'You have no Ethereum wallet in your account.')
                    return redirect('sapphire')
                else:
                    ETH_market = Crypto.objects.filter(crypto_network='Ethereum').values_list('market_value')
                    x = re.findall(r'\d+\.\d+', str(ETH_market))
                    ETH_value = int(dr_form) / float(x[0])

                    user.crypto_value = ETH_value
                    trans = Transaction.objects.create(investor=user, trans_type='Investment', network='ETH', trans_status='Pending', trans_amount=dr_form, crypto_val=ETH_value)

                    user.selected_wallet = Crypto.objects.filter(crypto_network='Ethereum').values_list('crypto_network')
                    user.selected_code = Crypto.objects.filter(crypto_network='Ethereum').values_list('crypto_code')
                    
                    forms.user = trans
                    forms.save()
                    return redirect('ethereum')
                
            if invt_network == '3':
                if user.user_wal_doge is None:
                    messages.warning(request, 'You have no Dogecoin wallet in your account.')
                    return redirect('sapphire')
                else:
                    DOGE_market = Crypto.objects.filter(crypto_network='Dogecoin').values_list('market_value')
                    x = re.findall(r'\d+\.\d+', str(DOGE_market))
                    DOGE_value = int(dr_form) / float(x[0])

                    user.crypto_value = DOGE_value
                    trans = Transaction.objects.create(investor=user, trans_type='Investment', network='DOGE', trans_status='Pending', trans_amount=dr_form, crypto_val=DOGE_value)
                    
                    user.selected_wallet = Crypto.objects.filter(crypto_network='Dogecoin').values_list('crypto_network')
                    user.selected_code = Crypto.objects.filter(crypto_network='Dogecoin').values_list('crypto_code')

                    forms.user = trans
                    forms.save()
                    return redirect('dogecoin')
                
            if invt_network == '4':
                if user.user_wal_lite is None:
                    messages.warning(request, 'You have no Litecoin wallet in your account.')
                    return redirect('sapphire')
                else:
                    LTC_market = Crypto.objects.filter(crypto_network='Litecoin').values_list('market_value')
                    x = re.findall(r'\d+\.\d+', str(LTC_market))
                    LTC_value = int(dr_form) / float(x[0])

                    user.crypto_value = LTC_value
                    trans = Transaction.objects.create(investor=user, trans_type='Investment', network='LTC', trans_status='Pending', trans_amount=dr_form, crypto_val=LTC_value)
                    
                    user.selected_wallet = Crypto.objects.filter(crypto_network='Litecoin').values_list('crypto_network')
                    user.selected_code = Crypto.objects.filter(crypto_network='Litecoin').values_list('crypto_code')

                    forms.user = trans
                    forms.save()
                    return redirect('litecoin')
                

    context = {
        'plan_form':plan_form,
        'plan_id':plan_id,
    }
    return render(request, 'gainisis/plans/sapphire.html', context)

@login_required(login_url=('login'))
def diamond(request):
    user = request.user.profile
    user.invested_amount = None
    plan_form = diamond_form(instance=user)

    plan_id = Plan.objects.all().filter(plan_title='Diamond')
    
    if request.method == 'POST':
        forms = diamond_form(request.POST, instance=user)
        if forms.is_valid():
            invt_network = forms.cleaned_data.get('selected_network')
            dr_form = forms.cleaned_data.get('invested_amount')

            user_plan = Plan.objects.filter(plan_title='Diamond').values_list('plan_title')
            user.selected_plan = user_plan

            if invt_network == '1':
                if user.user_wal_btc is None:
                    messages.warning(request, 'You have no Bitcoin wallet in your account.')
                    return redirect('diamond')
                else:
                    BTC_market = Crypto.objects.filter(crypto_network='Bitcoin').values_list('market_value')
                    x = re.findall(r'\d+\.\d+', str(BTC_market))
                    BTC_value = int(dr_form) / float(x[0])

                    user.crypto_value = BTC_value
                    trans = Transaction.objects.create(investor=user, trans_type='Investment', network='BTC', trans_status='Pending', trans_amount=dr_form, crypto_val=BTC_value)
                    
                    user.selected_wallet = Crypto.objects.filter(crypto_network='Bitcoin').values_list('crypto_network')
                    user.selected_code = Crypto.objects.filter(crypto_network='Bitcoin').values_list('crypto_code')

                    forms.user = trans
                    forms.save()
                    return redirect('bitcoin')
                
            if invt_network == '2':
                if user.user_wal_eth is None:
                    messages.warning(request, 'You have no Ethereum wallet in your account.')
                    return redirect('diamond')
                else:
                    ETH_market = Crypto.objects.filter(crypto_network='Ethereum').values_list('market_value')
                    x = re.findall(r'\d+\.\d+', str(ETH_market))
                    ETH_value = int(dr_form) / float(x[0])

                    user.crypto_value = ETH_value
                    trans = Transaction.objects.create(investor=user, trans_type='Investment', network='ETH', trans_status='Pending', trans_amount=dr_form, crypto_val=ETH_value)

                    user.selected_wallet = Crypto.objects.filter(crypto_network='Ethereum').values_list('crypto_network')
                    user.selected_code = Crypto.objects.filter(crypto_network='Ethereum').values_list('crypto_code')
                    
                    forms.user = trans
                    forms.save()
                    return redirect('ethereum')
                
            if invt_network == '3':
                if user.user_wal_doge is None:
                    messages.warning(request, 'You have no Dogecoin wallet in your account.')
                    return redirect('diamond')
                else:
                    DOGE_market = Crypto.objects.filter(crypto_network='Dogecoin').values_list('market_value')
                    x = re.findall(r'\d+\.\d+', str(DOGE_market))
                    DOGE_value = int(dr_form) / float(x[0])

                    user.crypto_value = DOGE_value
                    trans = Transaction.objects.create(investor=user, trans_type='Investment', network='DOGE', trans_status='Pending', trans_amount=dr_form, crypto_val=DOGE_value)
                    
                    user.selected_wallet = Crypto.objects.filter(crypto_network='Dogecoin').values_list('crypto_network')
                    user.selected_code = Crypto.objects.filter(crypto_network='Dogecoin').values_list('crypto_code')

                    forms.user = trans
                    forms.save()
                    return redirect('dogecoin')
                
            if invt_network == '4':
                if user.user_wal_lite is None:
                    messages.warning(request, 'You have no Litecoin wallet in your account.')
                    return redirect('diamond')
                else:
                    LTC_market = Crypto.objects.filter(crypto_network='Litecoin').values_list('market_value')
                    x = re.findall(r'\d+\.\d+', str(LTC_market))
                    LTC_value = int(dr_form) / float(x[0])

                    user.crypto_value = LTC_value
                    trans = Transaction.objects.create(investor=user, trans_type='Investment', network='LTC', trans_status='Pending', trans_amount=dr_form, crypto_val=LTC_value)
                    
                    user.selected_wallet = Crypto.objects.filter(crypto_network='Litecoin').values_list('crypto_network')
                    user.selected_code = Crypto.objects.filter(crypto_network='Litecoin').values_list('crypto_code')

                    forms.user = trans
                    forms.save()
                    return redirect('litecoin')
                

    context = {
        'plan_form':plan_form,
        'plan_id':plan_id,
    }
    return render(request, 'gainisis/plans/diamond.html', context)




def invest_btc(request):
    user = request.user.profile
    scan_bitcoin = Crypto.objects.filter(crypto_network='Bitcoin')
    plan_invest = Plan.objects.all()

    context={
        'profile':user,
        'scan_bitcoin':scan_bitcoin,
        'plan_invest':plan_invest,
    }
    return render(request, 'gainisis/investment/bitcoin.html', context)

def invest_eth(request):
    user = request.user.profile
    scan_ethereum = Crypto.objects.filter(crypto_network='Ethereum')
    plan_invest = Plan.objects.all()

    context={
        'profile':user,
        'scan_ethereum':scan_ethereum,
        'plan_invest':plan_invest,
    }
    return render(request, 'gainisis/investment/ethereum.html', context)

def invest_doge(request):
    user = request.user.profile
    scan_dogecoin = Crypto.objects.filter(crypto_network='Dogecoin')
    plan_invest = Plan.objects.all()

    context={
        'profile':user,
        'scan_dogecoin':scan_dogecoin,
        'plan_invest':plan_invest,
    }
    return render(request, 'gainisis/investment/dogecoin.html', context)

def invest_ltc(request):
    user = request.user.profile
    scan_litecoin = Crypto.objects.filter(crypto_network='Litecoin')
    plan_invest = Plan.objects.all()
    
    context={
        'profile':user,
        'scan_litecoin':scan_litecoin,
        'plan_invest':plan_invest,
    }
    return render(request, 'gainisis/investment/litecoin.html', context)



@login_required(login_url=('login'))
def support(request):
    user = request.user.profile

    spform = Chat()
    support = Support.objects.all().filter(chat_profile=user).order_by('chated_at')
    # wedk = Support.objects.filter(chat_profile=user).first()
    
    if request.method == 'POST':
        forms = Chat(request.POST, instance=user)
        sp_msg = forms.data.get('chat_message')
        
        if forms.is_valid():
            # if first_date == 'support':
            #     messages.warning(request, 'Date not existing')
            # else:
            #     messages.warning(request, 'Date existing')

            profile_msg = Support.objects.create(chat_profile=user, chat_message=sp_msg, message_type='User')
            forms.user = profile_msg
            forms.save()
            return redirect('support')

    context = {
        'spform':spform,
        'support':support,
        # 'wedk':wedk,
    }
    return render(request, 'gainisis/support.html', context)




def about(request):
    return render(request, 'gainisis/goto/about.html')

def affiliate(request):
    return render(request, 'gainisis/goto/affiliate.html')

def faqs(request):
    return render(request, 'gainisis/goto/faqs.html')

def terms(request):
    return render(request, 'gainisis/goto/terms.html')









# # python calculus
# wyehbd = re.findall(r'\d+\.\d+', str(BTC_market))
# cvasjbhknl = list(map(int,wyehbd))
# BTC_value = int(dr_form) / int(float(cvasjbhknl))
# BTC_value = int(dr_form) / re.findall(r'\d+\.\d+', str(BTC_market))
# BTC_value = int(dr_form) / re.sub(r'[0-9]', '_', str(BTC_market))
# BTC_value = int(dr_form) / float(str(BTC_market))

# value = '9.94%'
# float(value.replace('%', ''))

# BTC_value = int(user.invested_amount) / int(user.crypto_value)
# 'BTC_value':round(BTC_value - int(BTC_value), 7)



