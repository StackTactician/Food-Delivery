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
from delivery.models import UserProfile
from django.test import Client

def verify_validation():
    client = Client()
    suffix = random.randint(10000, 99999)
    
    email = f'unique_{suffix}@test.com'
    phone = f'555{suffix}'
    
    # 1. Register User A (Should Succeed)
    print("1. Registering User A...")
    data_a = {
        'username': f'user_a_{suffix}',
        'email': email,
        'password': 'pass1234',
        'role': 'Customer',
        'phone_number': phone,
        'address': '123 Test St'
    }
    response = client.post('/register/', data_a)
    if response.status_code == 302:
        print("User A Registered Successfully.")
    else:
        print(f"User A Registration Failed: {response.status_code}")
        print(response.content.decode()[:500])
        return

    # 2. Register User B with SAME EMAIL (Should Fail)
    print("\n2. Registering User B (Duplicate Email)...")
    data_b = {
        'username': f'user_b_{suffix}',
        'email': email, # Duplicate
        'password': 'pass1234',
        'role': 'Customer',
        'phone_number': f'666{suffix}', # Unique
        'address': '456 Test St'
    }
    response = client.post('/register/', data_b)
    content = response.content.decode()
    if "This email is already registered" in content:
        print("Success: Duplicate email blocked.")
    else:
        print("Failure: Duplicate email NOT blocked.")
        # print(content[:500])

    # 3. Register User C with SAME PHONE (Should Fail)
    print("\n3. Registering User C (Duplicate Phone)...")
    data_c = {
        'username': f'user_c_{suffix}',
        'email': f'unique_c_{suffix}@test.com', # Unique
        'password': 'pass1234',
        'role': 'Customer',
        'phone_number': phone, # Duplicate
        'address': '789 Test St'
    }
    response = client.post('/register/', data_c)
    content = response.content.decode()
    if "This phone number is already registered" in content:
        print("Success: Duplicate phone blocked.")
    else:
        print("Failure: Duplicate phone NOT blocked.")
        # print(content[:500])

if __name__ == '__main__':
    verify_validation()
