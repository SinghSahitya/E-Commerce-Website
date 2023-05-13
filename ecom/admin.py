from django.contrib import admin
from .models import User, Customer, Vendor, Item, Orders, Review, Wishlist, OrderItem, Cart, CartItem
from import_export.admin import ImportExportModelAdmin
# Register your models here.

admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Vendor)
admin.site.register(Item)
admin.site.register(Review)
admin.site.register(Wishlist)
admin.site.register(Cart)
admin.site.register(CartItem)



@admin.register(Orders)
class OrdersAdmin(ImportExportModelAdmin):
    pass



@admin.register(OrderItem)
class OrderItemAdmin(ImportExportModelAdmin):
    pass


