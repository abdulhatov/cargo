from django.contrib import admin
from .models import *

m = admin.ModelAdmin

@admin.register(Currency)
class CurrencyAdmin(m):
    list_display = ['name', 'code']
    list_display_links = ['name', 'code']


@admin.register(ServicePrice)
class ServicePriceAdmin(m):
    list_display = ['date']
    list_display_links = ['date']


@admin.register(Route)
class RouteAdmin(m):
    list_display = ['id']
    list_display_links = ['id']


@admin.register(Registration)
class RegistrationAdmin(m):
    list_display = ['name']
    list_display_links = ['name']

@admin.register(Inspector)
class InspectorAdmin(m):
    list_display = ['employee', 'id_REC_TRAN']
    list_display_links = ['employee']

@admin.register(Packer)
class PackerAdmin(m):
    list_display = ['employee', 'id_REC_TRAN']
    list_display_links = ['employee']

@admin.register(ReceptionTransmission)
class ReceptionTransmissionAdmin(m):
    list_display = ['pk', 'route']
    list_display_links = ['pk']

@admin.register(ProductP)
class ProductPTransmissionAdmin(m):
    list_display = ['id', 'bag_number', 'weight']
    list_display_links = ['id']

@admin.register(Direction)
class DirectionAdmin(m):
    list_display = ['id', 'name', 'code']
    list_display_links = ['id']

@admin.register(Price)
class PriceAdmin(m):
    list_display = ['id', 'service', 'country', 'currency', 'price']
    list_display_links = ['id']

@admin.register(NumberOfPlaces)
class NumberOfPlacesAdmin(m):
    list_display = ['id', 'recipient', 'agent', 'route']
    list_display_links = ['id']

@admin.register(Services)
class ServicesAdmin(m):
    list_display = ['id', 'service', 'count', 'status', 'priceIV']
    list_display_links = ['id']
