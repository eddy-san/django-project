from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = "Run dev server with in-memory DB: migrate + ensure superuser + runserver"

    def handle(self, *args, **options):
        call_command("migrate", interactive=False)

        User = get_user_model()
        username = os.getenv("DJANGO_SU_NAME")
        password = os.getenv("DJANGO_SU_PASSWORD")
        email = os.getenv("DJANGO_SU_EMAIL")

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f"Created superuser '{username}'"))
        else:
            self.stdout.write(self.style.WARNING(f"Superuser '{username}' already exists"))

        call_command("runserver")