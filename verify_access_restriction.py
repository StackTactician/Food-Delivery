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
from delivery.models import Restaurant
from django.test import Client

def verify_access_restriction():
    client = Client()
    
    # Ensure a restaurant exists for testing detail view
    restaurant, _ = Restaurant.objects.get_or_create(
        name="Test Resto",
        defaults={'description': "Test", 'address': "Test Addr"}
    )
    
    print("1. Testing Unauthenticated Access to List (/)..")
    response = client.get('/')
    if response.status_code == 302 and response.url.startswith('/login/'):
        print("Success: Redirected to /login/.")
    else:
        print(f"Failure: Expected redirect to /login/, got {response.status_code} - {response.url if response.status_code == 302 else ''}")

    # 2. Test Unauthenticated Access to Detail
    print("\n2. Testing Unauthenticated Access to Detail...")
    response = client.get(f'/restaurant/{restaurant.pk}/')
    if response.status_code == 302 and '/login/' in response.url:
        print("Success: Redirected to login.")
    else:
        print(f"Failure: Expected redirect to login, got {response.status_code} - {response.url if response.status_code == 302 else ''}")

    # 3. Test Authenticated Access
    print("\n3. Testing Authenticated Access...")
    suffix = random.randint(1000, 9999)
    user = User.objects.create_user(username=f'access_user_{suffix}', password='pass1234')
    client.login(username=f'access_user_{suffix}', password='pass1234')
    
    response = client.get('/')
    if response.status_code == 200:
        print("Success: Authenticated user can access list.")
    else:
        print(f"Failure: Authenticated user blocked? Status {response.status_code}")

if __name__ == '__main__':
    verify_access_restriction()
