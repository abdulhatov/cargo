import django_filters
from django_filters.widgets import RangeWidget
from .models import *
from main.models import EmployeeRole
from itertools import repeat
from route.models import Route

class OperationsFilter(django_filters.FilterSet):
    date = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={'type': 'datetime-local'}))
    route = django_filters.ModelMultipleChoiceFilter(queryset=Route.objects.all(), null_label='--------')
    cash = django_filters.ModelMultipleChoiceFilter(queryset=CashBox.objects.all(), null_label='--------')

    class Meta:
        model = Operations
        fields = ['route', 'cash', 'article', 'type', 'currency', 'date']

class OperationsViewFilter(django_filters.FilterSet):
    class Meta:
        model = Operations
        fields = ['id', 'date', 'cash', 'cash_sender', 'type', 'sum', 'currency', 'article']


class AdvanceFilter(django_filters.FilterSet):
    inner__employee__role__name = django_filters.ModelMultipleChoiceFilter(queryset=EmployeeRole.objects.all())
    inner__date = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={'type': 'date'}))
    class Meta:
        model = OperationsInner
        fields = ['inner__currency']

    @property
    def qs(self):
        parent = super().qs
        dict = {}
        for ob in parent:
            key = ob.inner.employee
            if key in dict:
                last_index = len(dict[key]) - 1
                if len(dict[key][last_index]) < 5:
                    dict[key][last_index].append([str(ob.inner.date), ob.sum])
                else:
                    dict[key].append([[str(ob.inner.date), ob.sum]])
            else:
                dict[key] = [[[str(ob.inner.date), ob.sum]]]

        for key in dict:
            last_index = len(dict[key]) - 1
            length = len(dict[key][last_index])
            if length < 5:
                dict[key][last_index].extend(repeat([], 5-length))
        return dict

class FinesFilter(django_filters.FilterSet):
    inner__employee__role__name = django_filters.ModelMultipleChoiceFilter(queryset=EmployeeRole.objects.all(),
                                                                           null_label='--------')
    inner__date = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={'type': 'date'}))
    class Meta:
        model = OperationsInner
        fields = ['inner__currency']

    @property
    def qs(self):
        parent = super().qs
        dict = {}
        for ob in parent:
            key = ob.inner.employee
            if key in dict:
                last_index = len(dict[key]) - 1
                if len(dict[key][last_index]) < 3:
                    dict[key][last_index].append([str(ob.inner.date), ob.sum])
                else:
                    dict[key].append([[str(ob.inner.date), ob.sum]])
            else:
                dict[key] = [[[str(ob.inner.date), ob.sum]]]

        for key in dict:
            last_index = len(dict[key]) - 1
            length = len(dict[key][last_index])
            if length < 3:
                dict[key][last_index].extend(repeat([], 3-length))
        return dict


class SalaryFilter(django_filters.FilterSet):
    class Meta:
        model = Salary
        fields = ['id', 'dateFrom', 'dateTo']

class ArticleFilter(django_filters.FilterSet):
    class Meta:
        model = Articles
        fields = ['id', 'name', 'type', 'description']


