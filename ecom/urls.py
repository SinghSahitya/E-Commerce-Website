from django.urls import path , include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sign_up/', views.signup, name='signup'),

]