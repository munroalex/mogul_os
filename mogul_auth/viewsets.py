from django.contrib.auth.models import User, Group
from esi.models import Token
from rest_framework import viewsets
from rest_framework import permissions
from mogul_auth.serializers import UserSerializer, TokenSerializer, SubscriptionPlanSerializer,UserSubscriptionPlanSerializer
from rest_framework.response import Response
from esi.clients import EsiClientProvider
from django.utils import timezone
from mogul_backend.models import Transaction, Character, Order, Structure, Stock,Profit

from subscriptions import models as submodels

esi = EsiClientProvider(spec_file='mogul_auth/swagger.json')

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    swagger_schema = None

    def get_object(self):
        return self.request.user

    def list(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class SubscriptionViewset(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = submodels.PlanCost.objects.all()
    serializer_class = SubscriptionPlanSerializer
    swagger_schema = None

class UserSubscriptionViewset(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    model = submodels.UserSubscription
    serializer_class = UserSubscriptionPlanSerializer
    def get_queryset(self):
        """Overrides get_queryset to restrict list to logged in user."""
        return self.model.objects.filter(user=self.request.user, active=True)

class TokenViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    serializer_class = TokenSerializer
    http_method_names = ['get','delete']
    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return Token.objects.filter(user=user)

    def retrieve(self, request, pk=None):
        user = self.request.user
        token = Token.objects.get(id=pk)
        serializer = TokenSerializer(token)
        data = serializer.data
        # Okay, let's get the cache timers
        # Let's see if its a character token
        required_scopes = ['esi-wallet.read_character_wallet.v1']
        check = Token.get_token(token.character_id, required_scopes)
        if(check):
            operation = esi.client.Wallet.get_characters_character_id_wallet_transactions(
                # required parameter for endpoint
                character_id = token.character_id,
                # provide a valid access token, which wil be refresh the token if required
                token = token.valid_access_token()
            )
            operation.request_config.also_return_response = True
            transresults, response = operation.results()
            data['WalletExpires'] = response.headers['Expires']

            operation = esi.client.Market.get_characters_character_id_orders(
                # required parameter for endpoint
                character_id = token.character_id,
                # provide a valid access token, which wil be refresh the token if required
                token = token.valid_access_token()
            )
            operation.request_config.also_return_response = True
            transresults, response = operation.results()
            data['OrderExpires'] = response.headers['Expires']
        required_scopes = ['esi-wallet.read_corporation_wallets.v1']
        check = Token.get_token(token.character_id, required_scopes)
        if(check):
            character = Character.objects.filter(character_id=token.character_id).first()
            operation = esi.client.Wallet.get_corporations_corporation_id_wallets_division_transactions(
                # required parameter for endpoint
                corporation_id = character.corporation_id,
                division = 1,
                # provide a valid access token, which wil be refresh the token if required
                token = token.valid_access_token()
            )
            operation.request_config.also_return_response = True
            transresults, response = operation.results()
            data['WalletExpires'] = response.headers['Expires']

            operation = esi.client.Market.get_corporations_corporation_id_orders(
                # required parameter for endpoint
                corporation_id = character.corporation_id,
                # provide a valid access token, which wil be refresh the token if required
                token = token.valid_access_token()
            )
            operation.request_config.also_return_response = True
            transresults, response = operation.results()
            data['OrderExpires'] = response.headers['Expires']
        data['CurrentTime'] = timezone.now()
        return Response(data)