import os
import sys
import django
import random

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_delivery_project.settings')
django.setup()

from django.conf import settings
if 'testserver' not in settings.ALLOWED_HOSTS:
    settings.ALLOWED_HOSTS.append('testserver')

from django.contrib.auth.models import User
from delivery.models import Order, UserProfile, Restaurant, MenuItem, OrderItem
from django.test import Client
from django.test.utils import setup_test_environment

setup_test_environment()

def verify_driver_dashboard():
    client = Client()
    suffix = random.randint(10000, 99999)
    
    # 1. Setup Driver
    print("1. Setting up Driver...")
    username = f'driver_{suffix}'
    user = User.objects.create_user(username=username, email=f'driver_{suffix}@test.com', password='pass1234')
    
    profile, _ = UserProfile.objects.get_or_create(user=user)
    profile.role = 'Driver'
    profile.vehicle_type = 'Bike'
    profile.vehicle_plate = 'TEST-PLATE'
    profile.license_number = 'LIC-TEST'
    profile.is_available = False
    profile.save()
    
    client.login(username=username, password='pass1234')

    # 2. Test Availability Toggle
    print("2. Testing Availability Toggle...")
    response = client.post('/driver/dashboard/', {'toggle_availability': 'true'})
    
    profile.refresh_from_db()
    if profile.is_available:
        print("Success: Driver is now ONLINE.")
    else:
        print("Failure: Driver is still OFFLINE.")

    # 3. Setup Data for Stats
    print("3. Setting up Stats Data...")
    # Create a completed order
    order = Order.objects.create(driver=user, status='Delivered', total_price=50.00)
    
    # Need dummy restaurant/item for template rendering (avoid crash)
    resto = Restaurant.objects.create(name="Test Resto", address="123 Food St")
    item = MenuItem.objects.create(restaurant=resto, name="Burger", price=50.00)
    OrderItem.objects.create(order=order, menu_item=item, price_at_time=50.00)

    # 4. Check Dashboard Content
    print("4. Checking Dashboard Content...")
    response = client.get('/driver/dashboard/')
    
    if response.status_code == 200:
        content = response.content.decode()
        
        # Check Profile Info
        # Check Stats
        if "$50.00" in content:
            print("Success: Earnings displayed correctly.")
        else:
            print("Failure: Earnings MISSING or incorrect.")
            
        if "Online" in content:
             print("Success: Online status displayed.")
        else:
             print("Failure: Online status MISSING.")

    else:
        print(f"Failure: Dashboard failed to load (Status {response.status_code})")

if __name__ == '__main__':
    verify_driver_dashboard()
