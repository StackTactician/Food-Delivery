import os
import sys
import django

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_delivery_project.settings')
django.setup()

from django.contrib.auth.models import User
from delivery.models import UserProfile
from django.test import Client

def verify_auth_revamp():
    client = Client()
    
    import random
    suffix = random.randint(1000, 9999)
    
    # 1. Test Customer Registration
    print("Testing Customer Registration...")
    customer_username = f'new_customer_{suffix}'
    customer_data = {
        'username': customer_username,
        'email': f'nc_{suffix}@test.com',
        'password': 'pass1234',
        'role': 'Customer',
        'phone_number': '1234567890',
        'address': '123 Main St',
    }
    response = client.post('/register/', customer_data)
    
    if response.status_code == 302:
        print("Customer Register: Success (Redirected)")
        user = User.objects.get(username=customer_username)
        if user.userprofile.address == '123 Main St':
            print("Customer Address Saved Correctly.")
        else:
            print(f"Customer Address Mismatch: {user.userprofile.address}")
    else:
        print(f"Customer Register: Failed (Status {response.status_code})")
        print(response.context['form'].errors if response.context else response.content.decode()[:500])

    # 2. Test Driver Registration
    print("\nTesting Driver Registration...")
    driver_username = f'new_driver_{suffix}'
    driver_data = {
        'username': driver_username,
        'email': f'nd_{suffix}@test.com',
        'password': 'pass1234',
        'role': 'Driver',
        'phone_number': '0987654321',
        'license_number': 'LIC123',
        'vehicle_plate': 'PLATE123',
        'vehicle_type': 'Bike',
        'bank_account': 'BANK123',
        'is_available': True
    }
    response = client.post('/register/', driver_data)
    
    if response.status_code == 302:
        print("Driver Register: Success (Redirected)")
        user = User.objects.get(username=driver_username)
        if user.userprofile.license_number == 'LIC123':
            print("Driver License Saved Correctly.")
        else:
            print(f"Driver License Mismatch: {user.userprofile.license_number}")
    else:
        print(f"Driver Register: Failed (Status {response.status_code})")
        print(response.context['form'].errors if response.context else response.content.decode()[:500])

    # 3. Test Validation (Driver missing license)
    print("\nTesting Validation (Driver missing license)...")
    invalid_driver_data = driver_data.copy()
    invalid_driver_data['username'] = f'invalid_driver_{suffix}'
    del invalid_driver_data['license_number']
    
    response = client.post('/register/', invalid_driver_data)
    
    if response.status_code == 200:
        print("Validation Test: Success (Form returned with errors)")
        content = response.content.decode()
        if "License number is required" in content:
            print("Correctly identified missing license number.")
        else:
            print("Failed to identify missing license number.")
            # print(content[:500])
    else:
        print(f"Validation Test: Failed (Status {response.status_code})")

if __name__ == '__main__':
    # Add testserver to allowed hosts for test client
    from django.conf import settings
    if 'testserver' not in settings.ALLOWED_HOSTS:
        settings.ALLOWED_HOSTS.append('testserver')
        
    verify_auth_revamp()
