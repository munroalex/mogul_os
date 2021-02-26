from rest_framework import serializers
from django.conf import settings
from mogul_backend.models import Transaction,Character,Order
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

class UserOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['duration','is_buy_order','is_corporation','issued','location_id','min_volume','order_id','price','range','region_id','type_id','volume_remain','volume_total','character_id','last_updated','user']

class UserCharacterSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False, read_only=True)
    class Meta:
        model = Character
        fields = ['character_id','corporation_id','alliance_id','name','user','last_esi_pull']