from django.db import models
from django.conf import settings
from eveuniverse.models import EveType
from django.utils import timezone
from dynamic_preferences.models import PerInstancePreferenceModel

def one_day_ago():
    return timezone.now() + timezone.timedelta(days=-1)


class MarketHistory(models.Model):
	item = models.ForeignKey(EveType,on_delete=models.CASCADE,help_text="The item involved on this profit row.",null=True)
	average = models.FloatField(null=True, default=None, blank=True)
	highest = models.FloatField(null=True, default=None, blank=True)
	lowest = models.FloatField(null=True, default=None, blank=True)
	order_count = models.IntegerField()
	volume = models.IntegerField()
	date = models.DateTimeField(null=False)
	region_id = models.IntegerField()

class MarketOrders(models.Model):
	item = models.ForeignKey(EveType,on_delete=models.CASCADE,help_text="The item involved on this profit row.",null=True)
	duration = models.IntegerField()
	is_buy_order = models.BooleanField(null=True)
	issued = models.DateTimeField()
	location_id = models.BigIntegerField()
	min_volume = models.IntegerField(null=True,default=0)
	order_id = models.BigIntegerField(primary_key = True)
	price = models.DecimalField(default=0,max_digits=20,decimal_places=2)
	range = models.CharField(max_length=16,default="0")
	system_id = models.IntegerField()
	volume_remain = models.IntegerField()
	volume_total = models.IntegerField()