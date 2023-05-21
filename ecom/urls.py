from django.urls import path , include
from . import views
from django.conf import settings  
from django.conf.urls.static import static  

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('', views.All_ItemList.as_view(), name='item_list'),
    path('logout', views.logout_view, name='logout'),
    path('cart/', views.cart, name='cart'),
    path('customer_signup/', views.customer_signup, name='customer_signup'),
    path('vendor_signup/', views.vendor_singup, name='vendor_signup'),
    path('item/new/', views.ItemFormView.as_view(), name='new_item'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('accounts/login/', views.UserLoginView.as_view(), name='account_login'),
    path('vendor_profile', views.vendor_profile, name='vendor_profile'),
    path('vendor_items/', views.vendor_item_list, name='vendor_items'),
    path('customer_profile/', views.CustomerDetailView.as_view(), name='customer_detail'),
    path('customer_updateinfo/', views.CustomerUpdateInfoView.as_view(), name='customer_updateinfo'),
    path('item/<int:pk>/update/', views.ItemUpdateView.as_view(), name='item_update'),
    path('place_order/', views.place_order, name='place_order'),
    path('order_success/', views.order_success_view, name='order_success'),
    path('previous_order/', views.orders, name='orders'),
    path('vendor_order/<int:item_id>/', views.vendor_order_view, name='vendor_order'),
    path('customer/<int:item_id>/review/', views.write_review, name='write_review'),
    path('detail/<int:item_id>/', views.item_detail, name='item_detail'),
    path('delete_item/<int:item_id>/', views.delete_item, name='delete_item'),
    path('download_report/', views.download_report, name='download_report'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('add_to_wishlist/<int:item_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('add_to_cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('apply-coupon/', views.apply_coupon, name='apply_coupon'),
    path('create-coupon/', views.create_coupon, name='create_coupon'),
    path('view_coupons/', views.view_coupons, name='view_coupons'),
    path('remove_coupon/<int:coupon_id>/', views.remove_coupon, name='remove_coupon'),
    
    

]
    
  
    


if settings.DEBUG:  
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  