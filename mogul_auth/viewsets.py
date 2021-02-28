from django.contrib.auth.models import User, Group
from esi.models import Token
from rest_framework import viewsets
from rest_framework import permissions
from mogul_auth.serializers import UserSerializer, TokenSerializer


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