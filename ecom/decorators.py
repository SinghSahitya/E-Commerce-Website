from django.contrib.auth.decorators import user_passes_test
from .models import Customer, Vendor
from django.shortcuts import redirect

def customer_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_customer:
            try:
                customer = request.user.customer
            except Customer.DoesNotExist:
                return redirect('customer_home')
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')
    return user_passes_test(lambda u: u.is_authenticated and u.is_customer, login_url='login')(wrapped_view)


def vendor_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_vendor:
            try:
                vendor = request.user.vendor
            except Vendor.DoesNotExist:
                return redirect('vendor_dashboard')
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')
    return user_passes_test(lambda u: u.is_authenticated and u.is_vendor, login_url='login')(wrapped_view)
