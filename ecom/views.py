from django.shortcuts import render, redirect
from .forms import CustomerSignUpForm, VendorSignUpForm, ItemForm
from .models import User, Customer, Vendor, Item, Orders
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .decorators import customer_required, vendor_required
from django.contrib.auth import logout

def home(request):
    return render(request, 'ecom/home.html')

@vendor_required
def dashboard_view(request):
    return render(request, 'ecom/vendor_dashboard.html')

@customer_required
def cart(request):
    return render(request, 'ecom/cart.html')

def logout_view(request):
    logout(request)
    return redirect('customer_home')

def register(request):
    return render(request, 'registration/register.html')

def customer_signup(request):
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_customer = True
            user.save()
            customer = Customer.objects.create(user=user)
            customer.address = form.cleaned_data.get('address')
            customer.email = form.cleaned_data.get('email')
            customer.phone = form.cleaned_data.get('phone')
            customer.save()
            return redirect('/')
    else:
        form = CustomerSignUpForm()
    return render(request, 'registration/customer_signup.html', {'form': form})

def vendor_singup(request):
    if request.method == 'POST':
        form = VendorSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_vendor = True
            user.save()
            vendor = Vendor.objects.create(user=user)
            vendor.email = form.cleaned_data.get('email')
            vendor.company_name = form.cleaned_data.get('company_name')
            vendor.save()
            return redirect('/')
    else:
        form = VendorSignUpForm()
    return render(request, 'registration/vendor_signup.html', {'form': form})

class ItemFormView(CreateView):
    form_class = ItemForm
    model = Item
    
# class CustomerLoginView(LoginView):
#     template_name = 'registration/login.html'

#     def get_success_url(self):
#         return reverse_lazy('customer_home')

class UserLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        if self.request.user.is_vendor:
            return reverse_lazy('vendor_dashboard')
        elif self.request.user.is_customer:
            return reverse_lazy('customer_home')
        # else:
        #     return reverse_lazy('customer_home')