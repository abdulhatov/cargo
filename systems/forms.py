from django import forms
from user.models import User
import django_filters
from .models import *

class UserFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'role', 'email']

