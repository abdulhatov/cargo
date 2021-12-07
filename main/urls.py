from django.urls import path
from . import views
from .views import *

app_name = 'main'

urlpatterns = [
    path('', views.HomePage.as_view(), name='home_page'),
    path('products', views.Products.as_view(), name='products'),
    path('product/edit/<int:pk>', ProductEditView.as_view(), name='product_edit'),
    path('product/delete/<int:pk>', deleteProduct, name='delete_product'),
    path('product/add/', views.ProductAddView.as_view(), name='product_add'),

    path('clients', views.ClientListView.as_view(), name='clients'),
    path('client/add/', views.ClientAddView.as_view(), name='client_add'),
    path('client/edit/<int:pk>', ClientEditView.as_view(), name='client_edit'),
    path('clients/delete/<int:pk>', delete_client, name='delete_client'),

    #path('senders', SenderListView.as_view(), name='senders'),
    path('senders/addjx/', add_sender, name='sender_add_ajax'),
    path('load_senders/', load_senders, name='load_senders_ajax'),
    path('senders/edit/<int:pk>', SenderEditView.as_view(), name='sender_edit'),
    #path('senders/delete/<int:pk>', delete_sender, name='delete_sender'),

    path('employees', EmployeeListView.as_view(), name='employees'),
    path('employee/add', EmployeeAdd.as_view(), name='employee_add'),
    path('employees/edit/<int:pk>', EmployeeEditView.as_view(), name='employee_edit'),
    path('delete/employees/<int:pk>', delete_employee, name='delete_employee'),

    path('contrageny', AgentOfClients.as_view(), name='contrageny'),
    path('contrageny/add', AgentOfClientAddView.as_view(), name='contrageny_add'),
    path('contrageny/edit/<int:pk>', AgentOfClientEditView.as_view(), name='contragenty_edit'),
    path('contrageny/delete/<int:pk>', delete_agenty, name='delete_contragenty'),

]
