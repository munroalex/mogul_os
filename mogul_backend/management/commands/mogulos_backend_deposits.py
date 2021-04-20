import logging
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from mogul_backend.tasks import processsubscriptions

class Command(BaseCommand):
    help = "processes deposits and subscriptions"

    def handle(self, *args, **options):
    	processsubscriptions()