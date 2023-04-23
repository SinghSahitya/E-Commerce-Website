from django.urls import path , include
from . import views
from django.conf import settings  
from django.conf.urls.static import static  

urlpatterns = [
    path('', views.home, name='customer_home'),
    path('register/', views.register, name='register'),
    path('customer_signup/', views.customer_signup, name='customer_signup'),
    path('vendor_signup/', views.vendor_singup, name='vendor_signup'),
    path('item/new/', views.ItemFormView.as_view(), name='new_item'),
    path('login/customer/', views.CustomerLoginView.as_view(), name='customer_login'),
    path('login/vendor/', views.VendorLoginView.as_view(), name='vendor_login')

    
]

if settings.DEBUG:  
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  