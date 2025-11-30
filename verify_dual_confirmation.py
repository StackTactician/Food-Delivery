import os
import sys
import django

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_delivery_project.settings')
django.setup()

from django.contrib.auth.models import User
from delivery.models import UserProfile, Order, Restaurant, MenuItem, OrderItem

def verify_dual_confirmation():
    # 1. Get Users
    customer_user = User.objects.get(username='customer1')
    driver_user = User.objects.get(username='driver1')

    # 2. Create Order
    restaurant = Restaurant.objects.first()
    menu_item = restaurant.menu_items.first()
    order = Order.objects.create(user=customer_user, total_price=menu_item.price)
    OrderItem.objects.create(order=order, menu_item=menu_item, price_at_time=menu_item.price)
    print(f"Order {order.id} created. Status: {order.status}")

    # 3. Driver Accepts
    order.driver = driver_user
    order.status = 'Delivering'
    order.save()
    print(f"Order {order.id} accepted by driver. Status: {order.status}")

    # 4. Driver Confirms
    order.driver_confirmed = True
    order.save()
    # Check logic from check_delivery_status
    if order.driver_confirmed and order.customer_confirmed:
        order.status = 'Delivered'
        order.save()
    print(f"Driver confirmed. Status: {order.status}")

    # 5. Customer Confirms
    order.customer_confirmed = True
    order.save()
    # Check logic from check_delivery_status
    if order.driver_confirmed and order.customer_confirmed:
        order.status = 'Delivered'
        order.save()
    print(f"Customer confirmed. Status: {order.status}")

if __name__ == '__main__':
    verify_dual_confirmation()
