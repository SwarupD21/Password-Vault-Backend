from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    help = "Create default admin user if not exists"

    def handle(self, *args, **kwargs):
        username = os.getenv("DJANGO_ADMIN_USER", "swarup21")
        password = os.getenv("DJANGO_ADMIN_PASSWORD", "lizun21")
        email = os.getenv("DJANGO_ADMIN_EMAIL", "admin@example.com")

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            self.stdout.write(self.style.SUCCESS("✅ Admin user created"))
        else:
            self.stdout.write(self.style.WARNING("ℹ️ Admin already exists"))
