from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Customer, User, Vendor, Item, Review, Coupon


class CustomerSignUpForm(UserCreationForm):
    username = forms.CharField(max_length=150, help_text='Required. Enter a username', widget=forms.TextInput(attrs={'placeholder': 'Your Username'}))
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.',  widget=forms.EmailInput(attrs={'placeholder': 'Your Email'}))
    first_name = forms.CharField(max_length=30, help_text='Required. Enter your first name.', widget=forms.TextInput(attrs={'placeholder': 'Your First Name'}) )
    last_name = forms.CharField(max_length=30, help_text='Required. Enter your last name.', widget=forms.TextInput(attrs={'placeholder': 'Your Last Name'}) )
    phone = forms.CharField(max_length=20, help_text='Required. Enter your phone number.', widget=forms.TextInput(attrs={'placeholder': 'Your Phone Number'}) )
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Your Address'}), help_text='Required. Enter your address.')

    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email', 'password1', 'password2')


class VendorSignUpForm(UserCreationForm):
    username = forms.CharField(max_length=150, help_text='Required. Enter a username', widget=forms.TextInput(attrs={'placeholder': 'Your Username'}) )
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.',  widget=forms.EmailInput(attrs={'placeholder': 'Your Email'}))
    first_name = forms.CharField(max_length=30, help_text='Required. Enter your first name.', widget=forms.TextInput(attrs={'placeholder': 'Your First Name'}) )
    last_name = forms.CharField(max_length=30, help_text='Required. Enter your last name.', widget=forms.TextInput(attrs={'placeholder': 'Your Last Name'}))
    company_name = forms.CharField(max_length=150,  widget=forms.TextInput(attrs={'placeholder': 'Your Company Name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = {'title',  'price', 'available_units' , 'image','description', 'discount'}


class ReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))
    class Meta:
        model = Review
        fields = {'review'}

class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['code', 'discount_percentage']