import os
import sys
import django

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_delivery_project.settings')
django.setup()

from django.contrib.auth.models import User
from delivery.models import UserProfile

def fix_profiles():
    users = User.objects.all()
    count = 0
    for user in users:
        try:
            user.userprofile
        except UserProfile.DoesNotExist:
            UserProfile.objects.create(user=user)
            print(f"Created profile for user: {user.username}")
            count += 1
    print(f"Fixed {count} users.")

if __name__ == '__main__':
    fix_profiles()
