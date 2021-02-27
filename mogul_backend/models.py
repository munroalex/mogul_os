from django.db import models
from django.conf import settings
from eveuniverse.models import EveType
from django.utils import timezone


def one_day_ago():
    return timezone.now() + timezone.timedelta(days=-1)

# Create your models here.
class Transaction(models.Model):
    client_id = models.IntegerField() #int32
    date = models.DateTimeField() #date-time
    is_buy = models.BooleanField(null=True,default=False)#boolean
    is_personal = models.BooleanField(null=True,default=False)#boolean
    journal_ref_id = models.BigIntegerField() #int64
    location_id = models.BigIntegerField() #int64
    quantity = models.IntegerField() #int32
    transaction_id = models.BigIntegerField() #int64
    type_id = models.IntegerField(default=0) #int32
    unit_price = models.DecimalField(max_digits=24,decimal_places=2) #double
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text="The user to whom this transaction belongs."
    )
    # Alright let's add the post-processed data
    type_name = models.CharField(default="Unknown",max_length=64)
    station_name = models.CharField(default="Unknown",max_length=64)
    state = models.BooleanField(default=False, null=False)
    profit = models.DecimalField(default=0,max_digits=20,decimal_places=2)
    margin = models.DecimalField(default=0,max_digits=20,decimal_places=2)
    taxes = models.DecimalField(default=0,max_digits=20,decimal_places=2)
    stock_date = models.DateTimeField(null=True)
    character_id = models.IntegerField(default=0)
    corporation_id = models.IntegerField(default=0)
class Order(models.Model):
    duration = models.IntegerField()
    is_buy_order = models.BooleanField(null=True)
    is_corporation = models.BooleanField(null=True,default=False)
    issued = models.DateTimeField()
    location_id = models.BigIntegerField()
    min_volume = models.IntegerField(null=True,default=0)
    order_id = models.BigIntegerField(primary_key = True)
    price = models.DecimalField(default=0,max_digits=20,decimal_places=2)
    range = models.CharField(max_length=16,default="0")
    region_id = models.IntegerField()
    type_id = models.IntegerField()
    volume_remain = models.IntegerField()
    volume_total = models.IntegerField()
    character_id = models.IntegerField(default=0)
    corporation_id = models.IntegerField(default=0,null=True)
    last_updated = models.DateTimeField(null=True,default=timezone.now)
    state = models.CharField(default="Open",max_length=32)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text="The user to whom this transaction belongs."
    )
    @property
    def item(self):
        return EveType.objects.filter(id=self.type_id).first()

class Character(models.Model):
    character_id = models.BigIntegerField(default=0)
    alliance_id = models.IntegerField(null=True)
    corporation_id = models.IntegerField(null=True)
    name = models.CharField(default="Cool Guy", max_length=32,null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text="The user to whom this character belongs."
    )
    last_esi_pull = models.DateTimeField(default=one_day_ago)

class Corporation(models.Model):
    corporation_id = models.BigIntegerField(default=0)
    alliance_id = models.IntegerField(null=True)
    name = models.CharField(default="Cool Corp", max_length=32,null=True)
    ceo_id = models.IntegerField()
    ticker = models.CharField(default="YETI", max_length=24)
    member_count = models.IntegerField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text="The user to whom this character belongs."
    )
    last_esi_pull = models.DateTimeField(default=one_day_ago)

class Structure(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(default="Unknown Structure",max_length=64,null=False)
    owner_id = models.IntegerField()
    solar_system_id = models.IntegerField()
    type_id = models.IntegerField()
    last_seen = models.DateTimeField(auto_now=True)
    position_x = models.FloatField(
        null=True, default=None, blank=True, help_text="x position in the solar system"
    )
    position_y = models.FloatField(
        null=True, default=None, blank=True, help_text="y position in the solar system"
    )
    position_z = models.FloatField(
        null=True, default=None, blank=True, help_text="z position in the solar system"
    )
