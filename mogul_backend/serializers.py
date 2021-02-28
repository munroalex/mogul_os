from rest_framework import serializers
from django.conf import settings
from mogul_backend.models import Transaction,Character,Order
from django.contrib.auth.models import User, Group
from mogul_auth.serializers import UserSerializer
from dynamic_preferences.types import BasePreferenceType
from django import forms
from mogul_backend.forms import PercentField
from django.core.exceptions import ValidationError
from dynamic_preferences.serializers import BaseSerializer
from decimal import Decimal, DecimalException
import decimal


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
    item = serializers.StringRelatedField(many=False, read_only=True)
    class Meta:
        model = Order
        fields = ['duration','is_buy_order','is_corporation','issued','location_id','min_volume','order_id','price','range','region_id','type_id','volume_remain','volume_total','character_id','last_updated','user','item','state']

class UserCharacterSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False, read_only=True)
    class Meta:
        model = Character
        fields = ['character_id','corporation_id','alliance_id','name','user','last_esi_pull']



class GenericNotificationRelatedField(serializers.RelatedField):

    def to_representation(self, value):
        if isinstance(value, Order):
            serializer = UserOrderSerializer(value)
        if isinstance(value, Transaction):
            serializer = UserTransactionSerializer(value)
        if isinstance(value, User):
            serializer = UserSerializer(value)

        return serializer.data


class NotificationSerializer(serializers.Serializer):
    recipient = GenericNotificationRelatedField(read_only=True)
    unread = serializers.BooleanField(read_only=True)
    target = GenericNotificationRelatedField(read_only=True)
    action_object = GenericNotificationRelatedField(read_only=True)
    verb = serializers.CharField()
    target_type = serializers.SerializerMethodField()
    object_type = serializers.SerializerMethodField()

    class Meta:
        fields = ['recipient','unread','target','action_object','verb','target_type','object_type']

    def get_target_type(self,obj):
        return obj.target.__class__.__name__
    def get_object_type(self,obj):
        return obj.action_object.__class__.__name__

class PercentSerializer(BaseSerializer):

    @classmethod
    def clean_to_db_value(cls, value):
        if not isinstance(value, decimal.Decimal):
            raise cls.exception('DecimalSerializer can only serialize Decimal instances')
        return value

    @classmethod
    def to_python(cls, value, **kwargs):
        try:
            #Let's do some math
            value = decimal.Decimal(value)
            if value is None:
                return None
            if (value < 0):
                return 0
            if (value > 1):
                return 1
            return decimal.Decimal(value)
        except decimal.InvalidOperation:
            raise cls.exception("Value {0} cannot be converted to decimal".format(value))

class PercentagePreference(BasePreferenceType):
    """
    A preference type that stores a :py:class:`decimal.Decimal`.
    """
    field_class = PercentField
    serializer = PercentSerializer