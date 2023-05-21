from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    def __str__(self):
        return self.username

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.email

class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, default='test@gmail.com')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)

    def __str__(self):
        return self.company_name

class Item(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='items')
    image = models.ImageField(upload_to='item_images/')
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    available_units = models.IntegerField()
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)


    def __str__(self):
        return self.title
    
    
class Review(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='reviews')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='reviews')
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.user.username} reviewed {self.item.title}"
    
class Wishlist(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='wishlist')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='wishlist')

    def __str__(self):
        return f"{self.customer.user.username} added {self.item.title} to wishlist"
    
class Coupon(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='coupons')
    code = models.CharField(max_length=20, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code    

class Cart(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='cart')
    items = models.ManyToManyField(Item, through='CartItem')
    applied_coupon = models.ForeignKey(Coupon, null=True, blank=True, on_delete=models.SET_NULL)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)

class Orders(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='orders')
    items = models.ManyToManyField(Item, through='OrderItem')
    ordered_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='order_items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

