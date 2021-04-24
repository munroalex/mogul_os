from django.shortcuts import render
from rest_pandas import PandasSimpleView,PandasViewSet,PandasJSONRenderer,PandasBoxplotSerializer,PandasUnstackedSerializer
import pandas as pd
from .models import Profit
from .serializers import UserProfitReportSerializer,UserProfitSerializer
from rest_framework import viewsets,permissions,generics, mixins, views,filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
import django_filters
from django_filters import rest_framework as djfilters

class ProfitFilter(djfilters.FilterSet):
    date_gte = django_filters.DateTimeFilter(name="date", lookup_expr='gte')
    date_lte = django_filters.DateTimeFilter(name="date", lookup_expr='lte')
    class Meta:
        model = Profit
        fields = ['item_id','date','date_gte','date_lte']

class ProfitSeriesViewset(PandasViewSet):
    serializer_class = UserProfitReportSerializer
    renderer_classes = [PandasJSONRenderer]
    filter_backends = [DjangoFilterBackend]
    filter_class = ProfitFilter
    @action(methods=['get'], detail=False)
    def get_item_breakdown(self, request, pk=None):
        qs = self.get_queryset()
        df = UserProfitReportSerializer(qs.all(), many=True).data
        if not df.empty:
            df = df.groupby(['item','item_id']).sum().round(2)
        return Response(df)
    @action(methods=['get'], detail=False)
    def get_station_breakdown(self, request, pk=None):
        qs = self.get_queryset()
        df = UserProfitReportSerializer(qs.all(), many=True).data
        if not df.empty:
            df = df.groupby(['profit_station'])['amount','taxes','quantity'].sum().round(2)
        return Response(df)
    def get_queryset(self):
        queryset = Profit.objects
        queryset.prefetch_related('profit_station')
        queryset.filter(user=self.request.user)
        date_gte = self.request.query_params.get('date_gte')
        if date_gte is not None:
            queryset = queryset.filter(date__gte=date_gte)
        date_lte = self.request.query_params.get('date_lte')
        if date_lte is not None:
            queryset = queryset.filter(date__lte=date_lte)
        item_id = self.request.query_params.get('item_id')
        if item_id is not None:
            queryset = queryset.filter(item_id=item_id)
        return queryset