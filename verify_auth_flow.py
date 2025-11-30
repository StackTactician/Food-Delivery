import os
import sys
import django

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_delivery_project.settings')
django.setup()

from django.contrib.auth.models import User
from delivery.models import UserProfile, Order, Restaurant, MenuItem, OrderItem

def verify_flow():
    # 1. Create Users
    customer_user, _ = User.objects.get_or_create(username='customer1', email='c1@test.com')
    customer_user.set_password('pass1234')
    customer_user.save()
    profile, _ = UserProfile.objects.get_or_create(user=customer_user)
    profile.role = 'Customer'
    profile.save()

    driver_user, _ = User.objects.get_or_create(username='driver1', email='d1@test.com')
    driver_user.set_password('pass1234')
    driver_user.save()
    profile, _ = UserProfile.objects.get_or_create(user=driver_user)
    profile.role = 'Driver'
    profile.save()

    print("Users created.")

    # 2. Create Order (Simulate Customer)
    restaurant = Restaurant.objects.first()
    if not restaurant:
        print("No restaurant found. Run populate_data.py first.")
        return

    menu_item = restaurant.menu_items.first()
    order = Order.objects.create(user=customer_user, total_price=menu_item.price)
    OrderItem.objects.create(order=order, menu_item=menu_item, price_at_time=menu_item.price)
    
    print(f"Order {order.id} created by {customer_user.username}. Status: {order.status}")

    # 3. Accept Order (Simulate Driver)
    # Logic from accept_order view
    if order.status == 'Pending':
        order.driver = driver_user
        order.status = 'Delivering'
        order.save()
        print(f"Order {order.id} accepted by {driver_user.username}. Status: {order.status}")
    else:
        print("Order not pending.")

    # 4. Complete Order (Simulate Driver)
    # Logic from complete_order view
    if order.driver == driver_user:
        order.status = 'Delivered'
        order.save()
        print(f"Order {order.id} delivered. Status: {order.status}")
    else:
        print("Driver mismatch.")

if __name__ == '__main__':
    verify_flow()
