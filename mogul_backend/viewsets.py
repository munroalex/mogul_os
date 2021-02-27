from django.contrib.auth.models import User, Group
from esi.models import Token
from rest_framework import viewsets,permissions,generics, mixins, views,filters
from rest_framework.decorators import api_view
from mogul_backend.serializers import UserTransactionSerializer,UserOrderSerializer,UserCharacterSerializer,NotificationSerializer
from mogul_backend.models import Transaction, Order,Character
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django_filters.rest_framework import DjangoFilterBackend
from notifications.models import Notification

type_id_parameter = openapi.Parameter('type_id', openapi.IN_QUERY, description="Filter by type_id", type=openapi.TYPE_INTEGER)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100


class TransactionViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
    pagination_class = StandardResultsSetPagination
    serializer_class = UserTransactionSerializer
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    ordering_fields = ['date']
    ordering = ['date']
    filterset_fields = ['type_id']

    def get_queryset(self):
        queryset = Transaction.objects.filter(user=self.request.user)
        return queryset

class OrderViewSet(generics.ListAPIView,viewsets.GenericViewSet):
    pagination_class = StandardResultsSetPagination
    serializer_class = UserOrderSerializer
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    ordering_fields = ['issued']
    ordering = ['issued']
    filterset_fields = ['type_id']

    def get_queryset(self):
        queryset = Order.objects.all()
        queryset.filter(user=self.request.user)
        return queryset

class CharacterViewSet(generics.ListAPIView,viewsets.GenericViewSet):
    pagination_class = StandardResultsSetPagination
    serializer_class = UserCharacterSerializer

    def get_queryset(self):
        queryset = Character.objects.filter(user=self.request.user)
        return queryset

class NotificationViewSet(generics.ListAPIView,viewsets.GenericViewSet):
    pagination_class = StandardResultsSetPagination
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()