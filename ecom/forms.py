from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Customer, User, Vendor, Item


class CustomerSignUpForm(UserCreationForm):
    username = forms.CharField(max_length=150, help_text='Required. Enter a username')
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    first_name = forms.CharField(max_length=30, help_text='Required. Enter your first name.')
    last_name = forms.CharField(max_length=30, help_text='Required. Enter your last name.')
    phone = forms.CharField(max_length=20, help_text='Required. Enter your phone number.')
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), help_text='Required. Enter your address.')

    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email', 'password1', 'password2')


class VendorSignUpForm(UserCreationForm):
    username = forms.CharField(max_length=150, help_text='Required. Enter a username')
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    first_name = forms.CharField(max_length=30, help_text='Required. Enter your first name.')
    last_name = forms.CharField(max_length=30, help_text='Required. Enter your last name.')
    company_name = forms.CharField(max_length=150)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = {'title',  'price', 'available_units' , 'image','description'}

        