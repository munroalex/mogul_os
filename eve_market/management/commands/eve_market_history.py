import logging
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from eve_market.tasks import updateMarketHistory

class Command(BaseCommand):
    help = "Update market history"

    def handle(self, *args, **options):
    	updateMarketHistory()