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
from delivery.models import Order, UserProfile
from django.test import Client

def verify_dashboard():
    client = Client()
    suffix = random.randint(10000, 99999)
    
    # 1. Setup User
    print("1. Setting up User...")
    username = f'dash_user_{suffix}'
    user = User.objects.create_user(username=username, email=f'dash_{suffix}@test.com', password='pass1234')
    
    # Ensure profile exists (signal should handle it, but being safe)
    profile, _ = UserProfile.objects.get_or_create(user=user)
    profile.phone_number = '123-456-7890'
    profile.address = '123 Dashboard Ave'
    profile.save()
    
    client.login(username=username, password='pass1234')

    # 2. Create Orders
    print("2. Creating Orders...")
    # Active Order
    Order.objects.create(user=user, status='Delivering', total_price=25.50)
    # Past Order
    Order.objects.create(user=user, status='Delivered', total_price=15.00)

    # 3. Access Dashboard
    print("3. Accessing Dashboard...")
    response = client.get('/my-orders/')
    
    if response.status_code == 200:
        print("Success: Dashboard loaded (200 OK)")
        content = response.content.decode()
        
        # Check for Sections
        if "Active Orders" in content:
            print("Success: 'Active Orders' section found.")
        else:
            print("Failure: 'Active Orders' section MISSING.")

        if "Recent History" in content:
            print("Success: 'Recent History' section found.")
        else:
            print("Failure: 'Recent History' section MISSING.")
            
        # Check for Profile Info
        if "123 Dashboard Ave" in content:
            print("Success: Address displayed.")
        else:
            print("Failure: Address MISSING.")
            
        # Check for Order Status
        if "On the Way" in content:
             print("Success: Progress bar 'On the Way' found.")
        else:
             print("Failure: Progress bar MISSING.")

    else:
        print(f"Failure: Dashboard failed to load (Status {response.status_code})")

if __name__ == '__main__':
    verify_dashboard()
