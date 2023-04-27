from django.urls import path , include
from . import views
from django.conf import settings  
from django.conf.urls.static import static  

urlpatterns = [
    path('', views.All_ItemList.as_view(), name='item_list'),
    path('dashboard/', views.dashboard_view, name='vendor_dashboard'),
    path('logout', views.logout_view, name='logout'),
    path('cart/', views.cart, name='cart'),
    path('register/', views.register, name='register'),
    path('customer_signup/', views.customer_signup, name='customer_signup'),
    path('vendor_signup/', views.vendor_singup, name='vendor_signup'),
    path('item/new/', views.ItemFormView.as_view(), name='new_item'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('vendors/<int:vendor_id>/', views.vendor_item_list, name='vendor_items'),
    path('customer_profile/', views.CustomerDetailView.as_view(), name='customer_detail'),
    path('customer_updateinfo/', views.CustomerUpdateInfoView.as_view(), name='customer_updateinfo'),
    path('item/<int:pk>/delete/', views.delete_item,name='delete_item'),
  
    
]

if settings.DEBUG:  
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  