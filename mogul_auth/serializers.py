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