from django.contrib import admin
from .models import *

@admin.register(CashBox)
class CashBoxAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_display_links = ['name']


@admin.register(Articles)
class ArticlesAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_display_links = ['name']

@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ['id', ]
    list_display_links = ['id']

@admin.register(SalaryInner)
class SalaryInnerAdmin(admin.ModelAdmin):
    list_display = ['id', ]
    list_display_links = ['id']

@admin.register(SalaryCurrency)
class SalaryCurrencyAdmin(admin.ModelAdmin):
    list_display = ['id']
    list_display_links = ['id']

@admin.register(Operations)
class OperationsAdmin(admin.ModelAdmin):
    list_display = ['pk']
    list_display_links = ['pk']

@admin.register(OperationsInner)
class OperationsInnerAdmin(admin.ModelAdmin):
    list_display = ['pk']
    list_display_links = ['pk']

@admin.register(ServicesSalary)
class ServicesSalaryAdmin(admin.ModelAdmin):
    list_display = ['id']
    list_display_links = ['id']

