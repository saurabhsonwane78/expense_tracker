from django.shortcuts import render
from django.http import JsonResponse
from .models import Loan, Category, Refunds, BorrowerBalance
from django.contrib.auth.models import User
from .forms import UserCreationForm, CategoryForm, LoanForm, RefundForm, UserUpdateForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages

def home(request):
    users = User.objects.all()
    loans_given = Loan.objects.filter(lender=request.user.id)
    refunds = Refunds.objects.filter(loan__lender=request.user.id)
    borrwers_ids=loans_given.values_list('borrower__id', flat=True)
    total_outstanding = BorrowerBalance.objects.filter(borrower_id__in=borrwers_ids)
    context = {
        'users' : users,
        'refunds': refunds,
        'loans_given': loans_given,
        'total_outstanding': total_outstanding
    }
    return render(request, 'tracker/home.html', context)

@login_required
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category Added Successfully')
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    else:
        form = CategoryForm()
    return render(request, 'create_category.html', {'form': form})

def create_user(request):
    if request.method == 'POST' :
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    else:
        form = UserCreationForm()
    return render(request, 'create_user.html', {'form': form})

@login_required
def create_loan(request):
    if request.method == 'POST':
        form = LoanForm(request.POST, user=request.user)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.lender = request.user 
            loan.save()
            messages.success(request, 'Transaction Added Successfully')
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    else:
        form = LoanForm(user=request.user)
    return render(request, 'create_loan.html', {'form': form})

@login_required
def add_refund(request):
    if request.method == 'POST':
        form = RefundForm(request.POST)
        if form.is_valid():
            refund = form.save()
            messages.success(request, 'Refund Added Successfully')
            return JsonResponse({'status': 'success', 'message': 'Refund added successfully!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid data provided.'})

    loans = Loan.objects.filter(lender=request.user)
    form = RefundForm()
    return render(request, 'refunds.html', {'loans': loans, 'refund_form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'message': 'Invalid credentials'})
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login') 

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            messages.success(request, 'Profile Updated Successfully')
            form.save()
            return JsonResponse({'status': 'success', 'message': 'Profile updated successfully!'})
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'update_profile.html', {'form': form})