from django.contrib import admin
from .models import User, Customer, Vendor, Item, Orders
# Register your models here.

admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Vendor)
admin.site.register(Item)
admin.site.register(Orders)