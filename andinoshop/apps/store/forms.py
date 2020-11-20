from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from django import forms
from .models import *


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name' ,'password1', 'password2']
        password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control','required': 'true' }),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': 'true'} ),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'password2': forms.PasswordInput(attrs={'class': 'input', 'required': 'true'}),
        }

class CustomerForm(ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'
        exclude = ['user']

class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = ['full_name', 'address_1', 'address_2', 'city', 'phone']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control','required': 'true' }),
            'address_1': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'} ),
            'address_2': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
        }