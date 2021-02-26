from django.contrib.auth.models import User, Group
from esi.models import Token
from rest_framework import viewsets
from rest_framework import permissions
from mogul_backend.serializers import UserTransactionSerializer
from mogul_backend.models import Transaction
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    pagination_class = StandardResultsSetPagination
    serializer_class = UserTransactionSerializer
    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return Transaction.objects.filter(user=user).order_by('date')