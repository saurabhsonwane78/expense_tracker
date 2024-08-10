# forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Category, Loan, Refunds
from django.contrib.auth.forms import AuthenticationForm

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['description', 'borrower', 'amount', 'category', 'location', 'payment_mode']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['borrower'].queryset = User.objects.exclude(id=user.id)
        self.fields['borrower'].required = True

class RefundForm(forms.ModelForm):
    class Meta:
        model = Refunds
        fields = ['loan', 'amount', 'payment_mode']

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']