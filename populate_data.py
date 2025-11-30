import os
import sys
import django

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_delivery_project.settings')
django.setup()

from delivery.models import Restaurant, MenuItem

def populate():
    # Clear existing data
    Restaurant.objects.all().delete()
    MenuItem.objects.all().delete()

    # Create Restaurant 1
    r1 = Restaurant.objects.create(
        name="Burger King",
        description="Home of the Whopper",
        address="123 Burger Lane"
    )
    MenuItem.objects.create(restaurant=r1, name="Whopper", description="Flame-grilled beef patty", price=5.99)
    MenuItem.objects.create(restaurant=r1, name="Fries", description="Golden crispy fries", price=2.99)

    # Create Restaurant 2
    r2 = Restaurant.objects.create(
        name="Pizza Hut",
        description="No One OutPizzas the Hut",
        address="456 Pizza Ave"
    )
    MenuItem.objects.create(restaurant=r2, name="Pepperoni Pizza", description="Classic pepperoni", price=12.99)
    MenuItem.objects.create(restaurant=r2, name="Breadsticks", description="Garlic butter breadsticks", price=4.99)

    print("Data populated successfully!")

if __name__ == '__main__':
    populate()
