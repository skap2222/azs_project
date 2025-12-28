from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('fuel/<int:pump_id>/', views.fuel_pump, name='fuel_pump'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('map/', views.map_view, name='map'),
    path('shop/', views.shop_view, name='shop'),
    path('promotions/', views.promotions_view, name='promotions'),
    path('receipt/<int:transaction_id>/', views.download_receipt, name='download_receipt'),
]
