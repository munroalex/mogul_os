from django.contrib.auth.models import User, Group
from esi.models import Token
from rest_framework import viewsets
from rest_framework import permissions
from mogul_auth.serializers import UserSerializer, TokenSerializer
from rest_framework.response import Response
from esi.clients import EsiClientProvider
from django.utils import timezone

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
        data['CurrentTime'] = timezone.now()
        return Response(data)