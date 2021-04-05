import logging
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Sets first user to superadmin"

    def handle(self, *args, **options):
        User = get_user_model()
        super = User.objects.get(id=1)
        super.is_staff = True
        super.is_admin = True
        super.is_superuser = True
        super.save()