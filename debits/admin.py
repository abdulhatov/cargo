from django.contrib import admin
from .models import *

@admin.register(ClientContrAgents)
class ClientContrAgentsAdmin(admin.ModelAdmin):
    list_display = ['pk']
    list_display_links = ['pk']

@admin.register(IncomeDebits)
class IncomeDebitsAdmin(admin.ModelAdmin):
    list_display = ['pk']
    list_display_links = ['pk']

@admin.register(IncomeDebitsInner)
class IncomeDebitsInnerAdmin(admin.ModelAdmin):
    list_display = ['pk']
    list_display_links = ['pk']
