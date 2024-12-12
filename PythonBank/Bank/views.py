from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import BankAccount
from django.db import IntegrityError
from django.db import models
from decimal import Decimal
# for generating unique account numbers
from uuid import uuid4 

# Create a view to register users using djagno's UserCreationForm

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('login')
            except IntegrityError as e:
                return render(request,'bank/register.html',{
                    'form':form,
                    'error':'A user with this username already exits'
                })
    else:
        form = UserCreationForm()
    return render(request, 'bank/register.html',{'form': form})

@login_required
def dashboard(request):
    try:
        # attepmt to get or create the bank account
        account, created = BankAccount.objects.get_or_create(user=request.user)
        if created:
            # generate a unique account number if crearting a new account
            account.account_number = str(uuid4())[:10]
            account.save()
    except IntegrityError:
        return render(request,'bank/dashboard.html',{
            'error':'Account creation failed due to duplicate data.'
        })
    
    context = {
        'account': account,
    }
    
    return render(request, 'bank/dashboard.html', context)


# Deposit Money
@login_required
def deposit(request):
    # get or create an account for current user
    account, created = BankAccount.objects.get_or_create(user=request.user)
    if created:
        account.account_number = str(uuid4())[:10]
        account.save()
    # process to the deposit
    if request.method == "POST":
        try:
            amount = request.POST.get('amount')
            amount = float(amount)
            if amount > 0:
                account.balance += Decimal(amount)
                account.balance = float(account.balance)
                account.save()
                return redirect('dashboard')
            else: 
                return render(request, 'bank/deposit.html')
        except ValueError:
            return render(request,'bank/deposit.html',{
                'error':'Invalid amount entered'
            })
    return render(request,'bank/deposit.html',{
        'account':account
    })

# Withdraw Money
@login_required
def withdraw(request):
    account, created = BankAccount.objects.get_or_create(user=request.user)
    if request.method == "POST":
        amount = request.POST.get('amount')
        amount = float(amount)
        account = request.user.bankaccount
        if 0 < amount <= account.balance:
            amount = Decimal(amount)
            account.balance -= amount
            account.save()
            return redirect('dashboard')
        else:
            return render(request, 'bank/withdraw.html',{'error': 'Insufficient balance'})
        # return redirect('dashboard')
    return render(request, 'bank/withdraw.html',{
        'account': account
    })

# check balance
@login_required
def check_balance(request):
    account, created = BankAccount.objects.get_or_create(user=request.user)
    account = request.user.bankaccount
    return render(request, 'bank/check_balance.html', {'balance': account.balance})

# logout
@login_required
def logout(request):
    return redirect('login')


        