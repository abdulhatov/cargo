import django_filters
from .models import *

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Product
        fields = ['id', 'code']

class EmployeeFilter(django_filters.FilterSet):
    fullname = django_filters.CharFilter(lookup_expr='icontains')
    address = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Employee
        fields = ['employeeID', 'role', 'phone', 'salary']

class AgentOfClientFilter(django_filters.FilterSet):
    fullname = django_filters.CharFilter(lookup_expr='icontains')
    address = django_filters.CharFilter(lookup_expr='icontains')
    store = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = AgentOfClient
        fields = ['id', 'country', 'phone']

class ClientFilter(django_filters.FilterSet):
    fullname = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Client
        fields = ['id', 'clientID', 'type', 'country', 'city', 'phone']


