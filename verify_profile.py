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
from django.test.utils import setup_test_environment

setup_test_environment()

def verify_profile():
    client = Client()
    suffix = random.randint(10000, 99999)
    
    # 1. Setup User
    print("1. Setting up User...")
    username = f'user_{suffix}'
    email = f'user_{suffix}@test.com'
    user = User.objects.create_user(username=username, email=email, password='pass1234')
    profile, _ = UserProfile.objects.get_or_create(user=user)
    profile.role = 'Customer'
    profile.save()
    
    client.login(username=username, password='pass1234')

    # 2. Test GET Profile
    print("2. Testing GET Profile...")
    response = client.get('/profile/')
    if response.status_code == 200:
        print("Success: Profile page loaded.")
    else:
        print(f"Failure: Profile page failed to load (Status {response.status_code})")
        return

    # 3. Test Update Profile
    print("3. Testing Update Profile...")
    new_phone = f"555-{suffix}"
    data = {
        'email': email, # Required field
        'phone_number': new_phone,
        'address': '123 New Address St',
        'role': 'Customer' # Should be ignored by form but good to have context
    }
    
    response = client.post('/profile/', data)
    
    # Reload profile from DB
    profile.refresh_from_db()
    
    if profile.phone_number == new_phone:
        print(f"Success: Phone number updated to {new_phone}")
    else:
        print(f"Failure: Phone number NOT updated. Current: {profile.phone_number}")
        
    if profile.address == '123 New Address St':
        print("Success: Address updated.")
    else:
        print("Failure: Address NOT updated.")

if __name__ == '__main__':
    verify_profile()
