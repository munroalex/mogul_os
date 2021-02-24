from django.contrib.auth.models import User, Group
from rest_framework import serializers
from esi.models import Token
from django.conf import settings


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.StringRelatedField(many=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'groups']

class TokenSerializer(serializers.ModelSerializer):
    scopes = serializers.StringRelatedField(many=True)
    class Meta:
        model = Token
        fields = ['id','character_name','user','character_id','token_type','scopes']

class EsiCharacterTransactions(serializers.Serializer):
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
