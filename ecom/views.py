from typing import Any, Optional
from django.db import models
from django.db.models import Sum
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomerSignUpForm, VendorSignUpForm, ItemForm, ReviewForm
from .models import User, Customer, Vendor, Item, Orders, Review, Wishlist, OrderItem, CartItem, Cart
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from .decorators import customer_required, vendor_required
from django.contrib.auth import logout
from django.contrib import messages
import uuid, os
from ECommerce import settings
from django.core.mail import send_mail
from mailjet_rest import Client
import requests
import csv
from django.http import HttpResponse
from ECommerce import creds


def home(request):
    return render(request, 'ecom/home.html')

def logout_view(request):
    logout(request)
    return redirect('item_list')

def vendor_profile(request):
    vendor = request.user.vendor
    orders = Orders.objects.filter(vendor=vendor)
    return render(request, 'ecom/vendor_profile.html', {'orders':orders})

def order_success_view(request):
    return render(request, 'ecom/order_success.html')

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

@customer_required
def write_review(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.item = item
            review.customer = request.user.customer
            review.save()
            return redirect('item_detail', item_id=item.pk)

    else:
        form = ReviewForm()

    return render(request, 'ecom/write_review.html', {'item':item, 'form':form})



class ItemFormView(LoginRequiredMixin, CreateView):
    form_class = ItemForm
    model = Item
    success_url = reverse_lazy('vendor_items')

    def form_valid(self, form):
        form.instance.vendor = self.request.user.vendor
        image_file = self.request.FILES.get('image')
        if image_file:
            filename = f'{uuid.uuid4()}.{image_file.name.split(".")[-1]}'
            form.instance.image = filename
            with open(os.path.join(settings.MEDIA_ROOT, filename), 'wb') as f:
                f.write(image_file.read())

        messages.success(self.request,"New Item ready for sale!")
        return super().form_valid(form)
    
class UserLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        if self.request.user.is_vendor:
            return reverse_lazy('vendor_items')
        elif self.request.user.is_customer:
            return reverse_lazy('item_list')

class All_ItemList(ListView):
    model = Item
    template_name = 'ecom/item_list.html'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(num_sales=Sum('order_items__quantity'))
        queryset = queryset.order_by('-num_sales')
    
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated and self.request.user.is_customer:
            customer = self.request.user.customer
            wishlist_items = Wishlist.objects.filter(customer=customer).values_list('item', flat=True)
            context['wishlist_items'] = wishlist_items

        return context


def vendor_item_list(request):
    vendor = Vendor.objects.get(id=request.user.vendor.id)
    items = Item.objects.filter(vendor=vendor)
    context = {
        'vendor': vendor,
        'items': items,
    }
    return render(request, 'ecom/vendor_item_list.html', context)

class CustomerDetailView(DetailView):
    model = Customer

    def get_object(self, queryset=None):
        return self.request.user.customer
    
class CustomerUpdateInfoView(UpdateView):
    model = Customer
    template_name ='ecom/customer_updateinfo.html'
    fields = ['email','phone', 'address', 'balance']
    success_url = reverse_lazy('customer_detail')

    def get_object(self, queryset=None):
        return self.request.user.customer
    
class ItemUpdateView(UpdateView):
    model = Item
    template_name = 'ecom/item_update.html'
    fields = ['title', 'price', 'description', 'available_units']

    def get_success_url(self):
        messages.success(self.request, "Details updated successfully!")
        return reverse_lazy('vendor_items')
    
def vendor_order_view(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    order_items = OrderItem.objects.filter(item=item)
    return render(request, 'ecom/vendor_order.html', {'item': item, 'order_items': order_items})

def item_detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    reviews = Review.objects.filter(item=item)
    context = {
        'item': item,
        'reviews': reviews,
    }
    return render(request, 'ecom/item_detail.html', context)


def delete_item(request, item_id):
    item = Item.objects.get(id=item_id)
    item.delete()
    return redirect('vendor_items', vendor_id=request.user.vendor.pk)


def download_report(request):
    report_data = Orders.objects.filter(vendor=request.user.vendor)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Order ID', 'Customer', 'Item', 'Quantity', 'Total Cost', 'Ordered At'])  
    for order in report_data:
        for order_item in order.order_items.all():
            writer.writerow([order_item.order.id, order.customer.user.username, order_item.item.title, order_item.quantity, order_item.total_cost, order.ordered_at])

    return response

@customer_required
def add_to_wishlist(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    customer = request.user.customer

    # Check if the item already exists in the customer's wishlist
    if Wishlist.objects.filter(customer=customer, item=item).exists():
        messages.error(request, 'This item is already in your wishlist.')
    else:
        wishlist = Wishlist(customer=customer, item=item)
        wishlist.save()
        messages.success(request, f"{item.title} added to your wishlist!")
    return redirect('wishlist')
@customer_required
def wishlist_view(request):
    customer = request.user.customer
    wishlist_items = Item.objects.filter(wishlist__customer=customer)
    context = {'items': wishlist_items}
    return render(request, 'ecom/wishlist.html', context)

@customer_required
def remove_from_wishlist(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    customer = request.user.customer
    try:
        wishlist_item = Wishlist.objects.get(customer=customer, item=item)
        wishlist_item.delete()
        messages.success(request, f"{item.title} has been removed from your wishlist.")
    except Wishlist.DoesNotExist:
        messages.error(request, f"{item.title} is not in your wishlist.")
    return redirect('wishlist')

@customer_required
def add_to_cart(request, item_id):
    item = Item.objects.get(pk=item_id)
    customer = request.user.customer
    cart, created = Cart.objects.get_or_create(customer=customer)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
    try:
        cart_item.quantity = int(request.POST.get('quantity'))
    except:
        pass
    cart_item.save()
    return redirect('cart')

def remove_from_cart(request, item_id):
    item = Item.objects.get(pk=item_id)
    customer = request.user.customer
    cart = Cart.objects.get(customer=customer)
    cart_item = CartItem.objects.get(cart=cart, item=item)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
        cart.items.remove(item)

    return redirect('cart')


def cart(request):
    customer = request.user.customer
    try:
        cart = request.user.customer.cart
    except Cart.DoesNotExist:
        # Create a new cart for the customer
        customer = request.user.customer
        cart = Cart.objects.create(customer=customer)
    cart_items = cart.cart_items.all()
    return render(request, 'ecom/cart.html', {'cart_items': cart_items})

def orders(request):
    customer = request.user.customer
    orders = Orders.objects.filter(customer=customer)
    return render(request, 'ecom/customer_order_list.html', {'orders': orders})


# @customer_required
# def place_order_view(request, item_id):
#     item = get_object_or_404(Item, pk=item_id)
#     customer = request.user.customer

#     if request.method == 'POST':
#         quantity = int(request.POST.get('quantity'))
#         total_cost = quantity * item.price
#         if customer.balance >= total_cost and item.available_units >= quantity:
#             order = Orders(customer=customer, vendor=item.vendor, item=item, quantity=quantity, total_cost=total_cost)
#             order.save()
#             customer.balance -= total_cost
#             customer.save()
#             item.available_units -= quantity
#             item.save()

#             #for sending emails
#             vendor_email = item.vendor.email
#             vendor_name = item.vendor.company_name
#             customer_name = customer.user.username
#             email_subject = 'New Order Placed!'
#             email_body = f'You have a new order from {customer_name}. Item: {item.title}. Quantity: {quantity}. Total Cost: {total_cost}'
            
#             mailgun_api_key = 'b92ee73d6256b7199da0998ee4b66e58-6b161b0a-02b199da'
#             mailgun_domain = 'sandbox9ac137dada9e488b83c11c29e7d4018a.mailgun.org'
#             mailgun_base_url = 'https://api.mailgun.net/v3/sandbox9ac137dada9e488b83c11c29e7d4018a.mailgun.org'

#             # Prepare the email data
#             data = {
#                 'from': f'{settings.MAILJET_SENDER_NAME} <mailgun@sandbox9ac137dada9e488b83c11c29e7d4018a.mailgun.org>',
#                 'to': [vendor_email, "YOU@sandbox9ac137dada9e488b83c11c29e7d4018a.mailgun.org"],
#                 'subject': email_subject,
#                 'text': email_body
#             }

#             # Send the email using Mailgun API  
#             response = requests.post(
#                 f'{mailgun_base_url}/messages',
#                 auth=('api', mailgun_api_key),
#                 data=data
#             )
            

#             print(response.status_code)
#             return redirect('order_success')
#         else:
#             return redirect('item_list')
#     return render(request, 'ecom/place_order.html', {'item': item})

def send_email_to_vendor(vendor_email, customer_name, item_name):
    mailgun_url = f"https://api.mailgun.net/v3/{creds.MAILGUN_DOMAIN}/messages"
    auth = ("api", creds.MAILGUN_API_KEY)
    data = {
        "from": f"DjangoMart <mailgun@{creds.MAILGUN_DOMAIN}>",
        "to": vendor_email,
        "subject": "New Order",
        "text": f"Hello, {vendor_email}!\n\nYou have a new order from {customer_name} for the item {item_name}.",
        "html": f"<h3>Hello, {vendor_email}!</h3><p>You have a new order from {customer_name} for the item {item_name}.</p>"
    }
    response = requests.post(mailgun_url, auth=auth, data=data)
    print(response.status_code)
    return response.status_code


def place_order(request):
    customer = request.user.customer
    cart = Cart.objects.get(customer=customer)
    items = cart.cart_items.all()
    vendor_items = {}
    total_amount = 0

    for cart_item in items:
        vendor = cart_item.item.vendor
        if vendor not in vendor_items:
            vendor_items[vendor] = []
        vendor_items[vendor].append(cart_item)
        total_amount += cart_item.item.price * cart_item.quantity

    if total_amount > customer.balance:
        messages.error(request, "Insufficient balance. Cannot place order.")
        return redirect('cart')

    for vendor, cart_items in vendor_items.items():
        order = Orders.objects.create(customer=customer, vendor=vendor)
        for cart_item in cart_items:
            item = cart_item.item
            OrderItem.objects.create(order=order, item=item, quantity=cart_item.quantity, total_cost=cart_item.quantity*cart_item.item.price)
            item.available_units -= cart_item.quantity
            item.save()
            cart_item.delete()

            vendor_email = item.vendor.email
            customer_name = request.user.username
            item_name = item.title
            status_code = send_email_to_vendor(vendor_email, customer_name, item_name)
            

    customer.balance -= total_amount
    customer.save()
    messages.success(request, "Order placed successfully!")
    return redirect('orders')
    

