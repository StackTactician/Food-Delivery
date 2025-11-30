import os
import sys
import django

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_delivery_project.settings')
django.setup()

from django.conf import settings
settings.ALLOWED_HOSTS.append('testserver')

from django.contrib.auth.models import User
from delivery.models import Restaurant, MenuItem, UserProfile
from django.test import Client

def verify_menu_management():
    # 1. Setup Data
    print("Setting up data...")
    owner_user, _ = User.objects.get_or_create(username='owner1', email='owner1@test.com')
    owner_user.set_password('pass1234')
    owner_user.save()
    
    # Ensure profile exists and has correct role
    profile, _ = UserProfile.objects.get_or_create(user=owner_user)
    profile.role = 'Restaurant Owner'
    profile.save()

    restaurant, _ = Restaurant.objects.get_or_create(
        name="Owner's Bistro",
        defaults={'description': "Test Desc", 'address': "Test Addr", 'owner': owner_user}
    )
    # Ensure owner is set (if it existed before)
    restaurant.owner = owner_user
    restaurant.save()

    client = Client()
    client.login(username='owner1', password='pass1234')

    # 2. Test Add Menu Item
    print("Testing Add Menu Item...")
    add_url = f'/restaurant/{restaurant.pk}/menu/add/'
    response = client.post(add_url, {
        'name': 'New Dish',
        'description': 'Tasty',
        'price': '15.00'
    })
    
    if response.status_code == 302:
        print("Add Item: Success (Redirected)")
    else:
        print(f"Add Item: Failed (Status {response.status_code})")
        if response.context and 'exception' in response.context:
            print(f"Exception: {response.context['exception']}")
        else:
            # Print first 500 chars of content to guess error
            print(response.content.decode()[:500])

    # Verify item exists
    item = MenuItem.objects.filter(name='New Dish', restaurant=restaurant).first()
    if item:
        print(f"Item '{item.name}' created in DB.")
    else:
        print("Item not found in DB.")
        return

    # 3. Test Edit Menu Item
    print("Testing Edit Menu Item...")
    edit_url = f'/menu-item/{item.pk}/edit/'
    response = client.post(edit_url, {
        'name': 'Updated Dish',
        'description': 'Very Tasty',
        'price': '20.00'
    })

    if response.status_code == 302:
        print("Edit Item: Success (Redirected)")
    else:
        print(f"Edit Item: Failed (Status {response.status_code})")

    item.refresh_from_db()
    if item.name == 'Updated Dish' and item.price == 20.00:
        print("Item updated correctly.")
    else:
        print(f"Item update failed. Name: {item.name}, Price: {item.price}")

    # 4. Test Delete Menu Item
    print("Testing Delete Menu Item...")
    delete_url = f'/menu-item/{item.pk}/delete/'
    response = client.post(delete_url)

    if response.status_code == 302:
        print("Delete Item: Success (Redirected)")
    else:
        print(f"Delete Item: Failed (Status {response.status_code})")

    if not MenuItem.objects.filter(pk=item.pk).exists():
        print("Item deleted from DB.")
    else:
        print("Item still exists in DB.")

if __name__ == '__main__':
    verify_menu_management()
