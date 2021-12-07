import django_filters
from .models import *

class ClientContrAgentsFilter(django_filters.FilterSet):
    fullname = django_filters.CharFilter(lookup_expr='icontains')
    address = django_filters.CharFilter(lookup_expr='icontains')
    store = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = ClientContrAgents
        fields = ['id', 'fullname', 'country', 'phone', 'address', 'store', 'added_by']

class IncomeDebitsFilter(django_filters.FilterSet):

    class Meta:
        model = IncomeDebits
        fields = ['id', 'date', 'cashBox', 'sum', 'wh_article']


