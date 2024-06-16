from django.contrib.auth.models import User
from django.core.management import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email="filenko.a@gmail.com",
            first_name="Admin",
            last_name="Admin",
            is_staff=True,
            is_superuser=True
        )

        user.set_password("30051980")
        user.save()
