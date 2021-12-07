from django.contrib import admin
from .models import *


@admin.register(AddList)
class AdminAddList(admin.ModelAdmin):
    list_display = ['id', 'title', 'content']
    list_display_links = ['title', 'content']


@admin.register(ListName)
class ListNameAdmin(admin.ModelAdmin):
    list_display = ['id', ]
    list_display_links = ['id', ]


@admin.register(CategoryName)
class CategoryNameAdmin(admin.ModelAdmin):
    list_display = ['id', ]
    list_display_links = ['id', ]


@admin.register(WarehouseOperation)
class WarehouseOperationAdmin(admin.ModelAdmin):
    list_display = ['id', 'date']
    list_display_link = ['id', 'date']


@admin.register(WarehouseOperationInner)
class WarehouseOperationInnerAdmin(admin.ModelAdmin):
    list_display = ['id', 'category']
    list_display_link = ['id', 'category']



