from django.db import models
from django.conf import settings

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
    type_id = models.IntegerField() #int32
    unit_price = models.DecimalField(max_digits=24,decimal_places=2) #double
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text="The user to whom this token belongs."
    )