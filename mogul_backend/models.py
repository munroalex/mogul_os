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
    is_buy = models.BooleanField(null=False,default=False)#boolean
    is_personal = models.BooleanField(null=False,default=False)#boolean
    journal_ref_id = models.BigIntegerField() #int64
    location_id = models.BigIntegerField() #int64
    quantity = models.IntegerField() #int32
    transaction_id = models.BigIntegerField() #int64
    type_id = models.ForeignKey(to=EveType, on_delete=models.DO_NOTHING) #int32
    unit_price = models.DecimalField(max_digits=24,decimal_places=2) #double
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text="The user to whom this transaction belongs."
    )
    # Alright let's add the post-processed data
    type_name = models.CharField(default="Unknown",max_length=32)
    station_name = models.CharField(default="Unknown",max_length=32)
    state = models.BooleanField(default=False, null=False)
    profit = models.DecimalField(default=0,max_digits=20,decimal_places=2)
    margin = models.DecimalField(default=0,max_digits=20,decimal_places=2)
    taxes = models.DecimalField(default=0,max_digits=20,decimal_places=2)
    stock_date = models.DateTimeField(null=True)

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