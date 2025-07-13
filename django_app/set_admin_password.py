#!/usr/bin/env python
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'email_generator.settings')
django.setup()

from django.contrib.auth.models import User

# Set password for admin user
admin_user = User.objects.get(username='admin')
admin_user.set_password('admin123')  # Change this to a secure password
admin_user.save()

print("Admin password set successfully!")
print("Username: admin")
print("Password: admin123")
