from django.contrib.auth.models import User, Group
from esi.models import Token
from rest_framework import viewsets,permissions,generics, mixins, views,filters
from rest_framework.decorators import api_view
from mogul_backend.serializers import UserTransactionSerializer,UserOrderSerializer,UserCharacterSerializer,NotificationSerializer,UserStockSerializer,UserProfitSerializer
from mogul_backend.models import Transaction, Order,Character,Stock,Profit
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django_filters.rest_framework import DjangoFilterBackend
from notifications.models import Notification
from dynamic_preferences import exceptions
from dynamic_preferences.settings import preferences_settings
from dynamic_preferences.models import GlobalPreferenceModel
from dynamic_preferences.api.serializers import GlobalPreferenceSerializer
from dynamic_preferences.api.viewsets import GlobalPreferencePermission,PreferenceViewSet
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from cacheops import cached_as,cached_view_as
from rest_framework.response import Response

type_id_parameter = openapi.Parameter('type_id', openapi.IN_QUERY, description="Filter by type_id", type=openapi.TYPE_INTEGER)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100


class TransactionViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
    pagination_class = StandardResultsSetPagination
    serializer_class = UserTransactionSerializer
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter,filters.SearchFilter]
    ordering_fields = ['date']
    ordering = ['-date']
    filterset_fields = ['type_id','is_buy']
    search_fields = ['type_name']

    def get_queryset(self):
        queryset = Transaction.objects.filter(user=self.request.user)
        return queryset

class OrderViewSet(generics.ListAPIView,viewsets.GenericViewSet):
    pagination_class = StandardResultsSetPagination
    serializer_class = UserOrderSerializer
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter,filters.SearchFilter]
    ordering_fields = ['issued']
    ordering = ['-issued']
    filterset_fields = ['type_id','state']
    search_fields = ['item','station']

    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Order.objects.all()
        queryset.filter(user=self.request.user)
        return queryset

class StockViewSet(generics.ListAPIView,viewsets.GenericViewSet):
    pagination_class = StandardResultsSetPagination
    serializer_class = UserStockSerializer
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    ordering_fields = ['date']
    ordering = ['-date']
    filterset_fields = ['item_id']

    def get_queryset(self):
        queryset = Stock.objects.all()
        queryset.filter(user=self.request.user)
        return queryset

class ProfitViewSet(generics.ListAPIView,viewsets.GenericViewSet):
    pagination_class = StandardResultsSetPagination
    serializer_class = UserProfitSerializer
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    ordering_fields = ['date']
    ordering = ['-date']
    filterset_fields = ['item_id']

    def get_queryset(self):
        queryset = Profit.objects.filter(user=self.request.user)
        return queryset

class CharacterViewSet(mixins.ListModelMixin,viewsets.GenericViewSet,mixins.RetrieveModelMixin):
    pagination_class = StandardResultsSetPagination
    serializer_class = UserCharacterSerializer

    def get_queryset(self):
        queryset = Character.objects.filter(user=self.request.user)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data['preferences'] = instance.preferences
        return Response(data)

class NotificationViewSet(generics.ListAPIView,viewsets.GenericViewSet):
    pagination_class = StandardResultsSetPagination
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()

class GlobalPreferencesViewSet(PreferenceViewSet):
    queryset = GlobalPreferenceModel.objects.all()
    serializer_class = GlobalPreferenceSerializer
    permission_classes = [GlobalPreferencePermission]
    http_method_names = ['get']
