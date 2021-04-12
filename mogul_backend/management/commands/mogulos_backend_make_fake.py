import sys

import shlex
import subprocess
from django.core.management.base import BaseCommand
from django.utils import autoreload
from eveuniverse.models import EveType, EveRace, EveStation
from mogul_backend.models import Transaction, Character
from django.contrib.auth.models import User
import random
import time
import datetime
from mogul_backend.helpers.orm import BulkCreateManager
import pytz

def random_date(start, end):
    """Generate a random datetime between `start` and `end`"""
    timedelta = start + datetime.timedelta(
        # Get a random amount of seconds between `start` and `end`
        seconds=random.randint(0, int((end - start).total_seconds())),
    )
    timedelta = datetime.datetime.combine(timedelta, datetime.datetime.min.time())

    timezone = pytz.timezone("UTC")
    return timezone.localize(timedelta)

class Command(BaseCommand):
    def handle(self, *args, **options):
        ships = [32788,32207,2836,32209,3518,33397,2863,44996,615]
        stations = [1028858195912,60003760,60002284,1025026043977,1023968078820]
        clients = [96368672]
        user = User.objects.get(id=1)
        trans = 0
        while trans < 20:
            #let's make a new transaction
            item, _ = EveType.objects.get_or_create_esi(id=random.choice(ships))
            #let's make a fake buy transacton
            Transaction.objects.create(
                    client_id=random.choice(clients),
                    date=random_date(datetime.date(2021,1,1), datetime.date(2021,2,1)),
                    is_buy=1,
                    is_personal=1,
                    journal_ref_id=trans,
                    location_id=random.choice(stations),
                    quantity=random.randint(1,5),
                    transaction_id=trans,
                    type_id=item.id,
                    unit_price=random.randint(50000000,150000000),
                    character_id=random.choice(clients),
                    user=user,
                    )
            Transaction.objects.create(
                    client_id=random.choice(clients),
                    date=random_date(datetime.date(2021,2,1), datetime.date(2021,3,1)),
                    is_buy=0,
                    is_personal=1,
                    journal_ref_id=trans + 100000,
                    location_id=random.choice(stations),
                    quantity=random.randint(1,5),
                    transaction_id=trans + 100000,
                    type_id=item.id,
                    unit_price=random.randint(150000000,250000000),
                    character_id=random.choice(clients),
                    user=user,
                    )
            trans = trans + 1
        