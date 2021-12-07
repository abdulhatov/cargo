from django.contrib import admin
from .models import *

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    list_display_links = ['name', 'code']


@admin.register(Country)
class Country(admin.ModelAdmin):
    list_display = ['name', 'code']
    list_display_links = ['name', 'code']


@admin.register(City)
class City(admin.ModelAdmin):
    list_display = ['pk', 'name']
    list_display_links = ['name']


@admin.register(Client)
class Client(admin.ModelAdmin):
    list_display = ['fullname', 'type']
    list_display_links = ['fullname']


@admin.register(StoreOfClient)
class StoreOfClientAdmin(admin.ModelAdmin):
    list_display = ['pk']
    list_display_links = ['pk']


@admin.register(EmployeeRole)
class EmployeeRole(admin.ModelAdmin):
    list_display = ['name']
    list_display_links = ['name']


@admin.register(Employee)
class Employee(admin.ModelAdmin):
    list_display = ['role']
    list_display_links = ['role']


@admin.register(AgentOfClient)
class AgentOfClient(admin.ModelAdmin):
    list_display = ['fullname']
    list_display_links = ['fullname']
