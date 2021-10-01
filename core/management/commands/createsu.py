from pathlib import Path

from decouple import AutoConfig
from django.core.management.base import BaseCommand

from core.models import User

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
config = AutoConfig(search_path=BASE_DIR)
admin = config("ADMIN")
admin_email = config("ADMIN_EMAIL")
admin_password = config("ADMIN_PASSWORD")


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.filter(email=admin_email).exists():
            User.objects.create_superuser(
                email=admin_email, password=admin_password, name=admin
            )
            self.stdout.write(self.style.SUCCESS("Successfully created superuser"))
