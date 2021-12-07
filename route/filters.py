import django_filters
from .models import Loc
from .models import *

STATUS_CHOICES = (
    ('1', 'Открыт'),
    ('0', 'Закрыт'),
)
class RouteFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=STATUS_CHOICES)
    control_status = django_filters.ChoiceFilter(choices=STATUS_CHOICES)
    location = django_filters.ChoiceFilter(choices=Loc)
    class Meta:
        model = Route
        fields = ['idRoute', 'country_recipient', 'date', 'status', 'control_status', 'id', 'location']

class RegistrationFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Registration
        fields = ['id', 'name', 'description']

class DirectionFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Direction
        fields = ['id', 'name', 'code']

class CurrencyFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Currency
        fields = ['id', 'name', 'code']

class ServicePriceFilter(django_filters.FilterSet):
    class Meta:
        model = ServicePrice
        fields = ['id', 'date']


class PriceFilter(django_filters.FilterSet):
    class Meta:
        model = Price
        fields = ['id', "service", 'country', 'currency', 'price']

class RTFilter(django_filters.FilterSet):
    class Meta:
        model = ReceptionTransmission
        fields = ['id', "route", 'dateRT', 'sender', 'recipient', 'registration', 'operator']

