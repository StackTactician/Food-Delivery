from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.restaurant_list, name='restaurant_list'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='delivery/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='restaurant_list'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('restaurant/<int:pk>/', views.restaurant_detail, name='restaurant_detail'),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/<int:pk>/', views.order_confirmation, name='order_confirmation'),
    path('driver/dashboard/', views.driver_dashboard, name='driver_dashboard'),
    path('driver/accept/<int:pk>/', views.accept_order, name='accept_order'),
    path('driver/complete/<int:pk>/', views.complete_order, name='complete_order'),
    path('my-orders/', views.customer_dashboard, name='customer_dashboard'),
    path('confirm-delivery/<int:pk>/', views.confirm_delivery_customer, name='confirm_delivery_customer'),
    
    # Restaurant Management
    path('restaurant/manage/', views.manage_restaurants, name='manage_restaurants'),
    path('restaurant/<int:pk>/menu/add/', views.add_menu_item, name='add_menu_item'),
    path('menu-item/<int:pk>/edit/', views.edit_menu_item, name='edit_menu_item'),
    path('menu-item/<int:pk>/delete/', views.delete_menu_item, name='delete_menu_item'),
]
