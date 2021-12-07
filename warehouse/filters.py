import django_filters
from .models import *
from django_filters.widgets import RangeWidget

class AddListFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    content = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = AddList
        fields = ['id', 'title', 'content']


class CategoryNameFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = CategoryName
        fields = ['id', 'title']

class ListNameFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = ListName
        fields = ['id', 'title', 'category']

class WarehouseOperationFilter(django_filters.FilterSet):
    class Meta:
        model = WarehouseOperation
        fields = ['id', 'date', 'warehouse', 'from_warehouse', 'type', 'added_by']

class WHReportFilter(django_filters.FilterSet):
    inner__date = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={'type': 'date'}))

    class Meta:
        model = WarehouseOperationInner
        fields = ['inner__warehouse', 'name', 'inner__type', 'inner__date']
