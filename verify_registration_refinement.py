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
from django.test import Client
from django.test.utils import setup_test_environment

setup_test_environment()

def verify_registration_refinement():
    client = Client()
    suffix = random.randint(10000, 99999)
    
    # 1. Test Successful Registration Redirect
    print("1. Testing Registration Redirect...")
    data = {
        'username': f'redirect_user_{suffix}',
        'email': f'redirect_{suffix}@test.com',
        'password': 'pass1234',
        'role': 'Customer',
        'phone_number': f'777{suffix}',
        'address': 'Redirect St'
    }
    response = client.post('/register/', data)
    
    if response.status_code == 302:
        if response.url == '/login/':
            print("Success: Redirected to /login/")
        else:
            print(f"Failure: Redirected to {response.url}, expected /login/")
    else:
        print(f"Failure: Registration failed with status {response.status_code}")
        # print(response.content.decode()[:500])
        return

    # 2. Verify User NOT Logged In
    # Client session should not have user_id if not logged in
    if '_auth_user_id' not in client.session:
        print("Success: User is NOT logged in.")
    else:
        print("Failure: User IS logged in.")

    # 3. Test Invalid Role (Restaurant Owner)
    print("\n2. Testing Invalid Role (Restaurant Owner)...")
    data_owner = {
        'username': f'owner_try_{suffix}',
        'email': f'owner_{suffix}@test.com',
        'password': 'pass1234',
        'role': 'Restaurant Owner', # Should be invalid now
        'phone_number': f'888{suffix}'
    }
    response = client.post('/register/', data_owner)
    
    if response.status_code == 200:
        if response.context and 'role' in response.context['form'].errors:
             print("Success: 'Restaurant Owner' role rejected.")
        else:
             print("Failure: 'Restaurant Owner' role NOT rejected.")
             print(f"Form Errors: {response.context['form'].errors}")
    else:
        print(f"Failure: Expected form error (200), got {response.status_code}")

if __name__ == '__main__':
    verify_registration_refinement()
