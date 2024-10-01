from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django import forms
from .models import Product, User, Listed

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']  # Include password field


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2','role']

class EditUserForm(ModelForm):

    class Meta:
        model = User
        fields = ['avatar', 'name','username','email', 'bio']


class ListedForm(forms.ModelForm):
    class Meta:
        model = Listed
        fields = ['product']

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'