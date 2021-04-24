# Create your tasks here
import time
from celery import shared_task
from eveuniverse.models import EveType, EveRace, EveStation
from esi.clients import EsiClientProvider
from esi.decorators import single_use_token,token_required,tokens_required
from esi.models import Token
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from mogul_backend.helpers.orm import BulkCreateManager
from mogul_backend.datehelpers import one_hour_ago,one_day_ago
from eveuniverse.helpers import EveEntityNameResolver
from notifications.signals import notify
import simplejson as json
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict
from decimal import Decimal
from datetime import datetime, timedelta
from contextlib import contextmanager
from django.core.cache import cache
from hashlib import md5
from celery.utils.log import get_task_logger
from oscar_accounts import facade,models
from eve_market.models import MarketHistory
import pytz
import importlib

from django.core.management.base import BaseCommand

from subscriptions.conf import SETTINGS

logger = get_task_logger(__name__)

esi = EsiClientProvider(spec_file='mogul_auth/swagger.json')
LOCK_EXPIRE = 60 * 30  # Lock expires in 30 minutes

@contextmanager
def task_locker(lock_id):
    timeout_at = time.monotonic() + LOCK_EXPIRE - 3
    # cache.add fails if the key already exists
    status = cache.add(lock_id, True, LOCK_EXPIRE)
    try:
        yield status
    finally:
        # memcache delete is very slow, but we have to use it to take
        # advantage of using add() for atomic locking
        if time.monotonic() < timeout_at and status:
            # don't release the lock if we exceeded the timeout
            # to lessen the chance of releasing an expired lock
            # owned by someone else
            # also don't release the lock if we didn't acquire it
            cache.delete(lock_id)

def task_unlocker(lock_id):
    cache.delete(lock_id)
            

def first(iterable, default=None):
  for item in iterable:
    return item
  return default


@shared_task(name="updateMarketHistory") # requires a user_id
def updateMarketHistory():
    # Let's get the market history now. 
    region_id = 10000002
    typeidres = esi.client.Market.get_markets_region_id_types(
        region_id = region_id
        ).results()

    for item in typeidres:
        print("Processing f{item}")
        # Let's also get the last history
        latest = MarketHistory.objects.order_by('-date').filter(item_id= item).first()
        if latest is None:
            latest = timezone.now() - timedelta(days=700)
        else:
            latest = latest.date
        ordresults = esi.client.Market.get_markets_region_id_history(
            region_id = region_id,
            type_id = item
        ).results()
        for history in ordresults:
            historydate = datetime.combine(history.get('date'),datetime.min.time())
            historydate = pytz.utc.localize(historydate)
            if latest < historydate:
                #Let's save
                row = MarketHistory.objects.create(
                    item_id=item,
                    average=history.get('average'),
                    highest=history.get('highest'),
                    lowest=history.get('lowest'),
                    order_count=history.get('order_count'),
                    volume=history.get('volume'),
                    date=historydate,
                    region_id=region_id
                    )
    
