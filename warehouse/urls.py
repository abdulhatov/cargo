from django.urls import path
from . import views
from .views import *
from .print import *

app_name = 'warehouse'

urlpatterns = [
    path('storage/', WarehouseListView.as_view(), name='list_warehouse'),
    path('storage/add/', WarehouseAddView.as_view(), name='warehouse_add'),
    path('storage/edit/<int:pk>/', WarehouseUpdateView.as_view(), name='warehouse_update'),
    path('storage/delete/<int:pk>/', deleteWarehose, name='warehouse_delete'),

    path('category/', CategoryListView.as_view(), name='list_category'),
    path('category/add/', CategoryAddView.as_view(), name='category_add'),
    path('category/edit/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>/', deleteCategory, name='category_delete'),

    path('naming/', NamingListView.as_view(), name='list_naming'),
    path('naming/add/', NamingAddView.as_view(), name='naming_add'),
    path('naming/edit/<int:pk>/', NamingUpdateView.as_view(), name='naming_update'),
    path('naming/delete/<int:pk>/', deleteNaming, name='naming_delete'),

    path('bag_report/', views.BagReportView.as_view(), name='bag_report'),
    path('bag_report/load_routes', load_routes, name='ajax_load_routes'),

    path('wh_report', views.WHReportView.as_view(), name='wh_report'),
    path('ostatok', views.OstatokView.as_view(), name='ostatok'),
    path('selectListname/', selectListName, name='select_listName_url'),

    path('wh_operations/', views.WHOperatiosView.as_view(), name='wh_operations'),

    path('wh_incomeId/<int:pk>/', IncomeWarehouseView.as_view(), name='wh_incomeId'),
    path('wh_incomeCash/<int:pk>/', IncomeWarehouseCashierView.as_view(), name='wh_income_cashier'),

    path('wh_income_add/', WHIncomeAddView.as_view(), name='wh_income_add'),
    path('wh_income_edit/<int:pk>/', WHIncomeEditView.as_view(), name='wh_income_edit'),
    path('wh_income_delete/<int:pk>/', operationDelete, name='wh_income_delete'),
    path('wh_incomePrint/<int:pk>/', incomeWarehousePrint, name='wh_incomePrint'),
    path('wh_in_cash_Print/<int:pk>/', incomeWarehouseCashierPrint, name='wh_in_cash_Print'),


    path('wh_consumption_add/', WHConsumptionAddView.as_view(), name='wh_consumption_add'),
    path('wh_consumption_edit/<int:pk>/', WHConsumptionEditView.as_view(), name='wh_consumption_edit'),
    path('wh_consumption_delete/<int:pk>/', operationDelete, name='wh_consumption_delete'),
    path('wh_consumptionID/<int:pk>/', ConsumablesWarehouseView.as_view(), name='wh_consumptionId'),
    path('wh_consumptionPrint/<int:pk>/', consumablesWarehousePrint, name='wh_consumptionPrint'),

    path('wh_moving_add/', WHMovingAddView.as_view(), name='wh_moving_add'),
    path('wh_moving_edit/<int:pk>/', WHMovingEditView.as_view(), name='wh_moving_edit'),
    path('wh_moving_delete/<int:pk>/', operationDelete, name='wh_moving_delete'),
    path('wh_movingId/<int:pk>/', MovingWarehouseView.as_view(), name='wh_movingId'),
    path('wh_movingPrint/<int:pk>/', movingWarehousePrint, name='wh_movingPrint'),
]


