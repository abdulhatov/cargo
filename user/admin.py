from django.contrib import admin
from .models import User


@admin.register(User)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['pk', 'email']
    list_display_links = ['pk']