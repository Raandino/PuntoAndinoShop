from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from django import forms
from taggit.forms import TagWidget
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
        fields = ['name', 'phone', 'email', 'profile_pic']
        widgets = {
            'name': forms.TextInput(attrs = {'class': 'form-control'}),
            'phone': forms.TextInput(attrs = {'class': 'form-control'}),
            'email': forms.TextInput(attrs = {'class': 'form-control'}),
            'profile_pic': forms.FileInput(attrs = {'class': 'custom-file-input'}),
        }

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

class CouponForm(ModelForm):
    class Meta:
        model = Coupon
        fields = ['code']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cupon de Descuento'})
        }

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs = {'class': 'form-control'})
        }

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'slug', 'category', 'brand', 'description', 'original_price', 'disccount', 'dis', 'tags', 'image', 'quantity_available', 'alta']
        widgets = {
            'name': forms.TextInput(attrs = {'class': 'form-control'}),
            'slug': forms.TextInput(attrs = {'class': 'form-control'}),
            'category': forms.Select(attrs = {'class': 'form-control'}),
            'brand': forms.Select(attrs = {'class': 'form-control'}),
            'description': forms.Textarea(attrs = {'class': 'form-control'}),
            'original_price': forms.TextInput(attrs = {'class': 'form-control'}),
            'dis': forms.NumberInput(attrs = {'class': 'form-control'}),
            'tags': TagWidget(attrs = {'class': 'form-control'}),
            'quantity_available': forms.NumberInput(attrs = {'class': 'form-control'}),
        }

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['parent', 'title', 'slug', 'ordering', 'alta']
        widgets = {
            'parent': forms.Select(attrs= {'class': 'form-control'}),
            'title': forms.TextInput(attrs= {'class': 'form-control'}),
            'slug': forms.TextInput(attrs= {'class': 'form-control'}),
            'ordering': forms.NumberInput(attrs= {'class': 'form-control'}),
        }

class BrandForm(ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'slug']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
        }