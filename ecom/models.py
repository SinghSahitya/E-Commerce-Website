from django.db import models
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
    image = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    available_units = models.IntegerField()

    def __str__(self):
        return self.title
    
class Orders(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='order')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='order')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='order')
    quantity  = models.IntegerField()

    def __str__(self):
        return f"{self.customer.user.username} ordered {self.quantity} units of {self.item.title} from {self.vendor.company_name}"
    
