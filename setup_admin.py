# setup_admin.py

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from courses.models import User

username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'luntik')
email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'luntik2703')

try:
    if User.objects.filter(username=username).exists():
        print(f"User '{username}' already exists")
    else:
        User.objects.create_superuser(username=username, email=email, password=password)
        print(f"✅ Superuser '{username}' created successfully!")
except Exception as e:
    print(f"❌ Error creating superuser: {e}")