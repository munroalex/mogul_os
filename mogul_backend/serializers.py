from rest_framework import serializers
from django.conf import settings
from mogul_backend.models import Transaction,Character
from django.contrib.auth.models import User, Group

class TransactionSerializer(serializers.Serializer):
    client_id = serializers.IntegerField() #int32
    date = serializers.DateTimeField()#date-time
    is_buy = serializers.NullBooleanField()#boolean
    is_personal = serializers.NullBooleanField()#boolean
    journal_ref_id = serializers.IntegerField() #int64
    location_id = serializers.IntegerField() #int64
    quantity = serializers.IntegerField() #int32
    transaction_id = serializers.IntegerField() #int64
    type_id = serializers.IntegerField() #int32
    unit_price = serializers.DecimalField(max_digits=24,decimal_places=2) #double

class UserTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['client_id','date','is_buy','is_personal','journal_ref_id','location_id','quantity','transaction_id','type_id','unit_price','user','type_name','station_name','state','profit','margin','taxes']

class UserCharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ['character_id','corporation_id','alliance_id','name','user','last_esi_pull']