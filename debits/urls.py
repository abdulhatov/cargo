from django.urls import path
from .views import *
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .prints import *

app_name = 'debits'
urlpatterns = [
    path('agentofclient/', ListAgentOfClient.as_view(), name='agentofclient'),
    path('agentofclient/add/', AgentOfClientAddView.as_view(), name='agentofclient_add'),
    path('agentofclient/edit/<int:pk>', AgentOfClientEditView.as_view(), name='agentofclient_edit'),
    path('agentofclient/delete/<int:pk>', deleteAgentOfClient, name='agentofclient_delete'),

    path('coming/', ListIncomes.as_view(), name='list_income'),
    path('coming/<int:pk>', IncomeId.as_view(), name='income_id'),
    path('coming2/<int:pk>', IncomeId2.as_view(), name='income2_id'),
    path('coming/print/<int:pk>', incomePrint, name='income_print'),
    path('coming/print2/<int:pk>', incomePrint2, name='income_print2'),

    path('coming/add', IncomeDebitsAdd.as_view(), name='income_add'),
    path('coming/edit/<int:pk>', IncomeDebitsEdit.as_view(), name='income_edit'),

    path('clients/', selectAgent, name='clients_jx'),
    path('routes/', selectClient, name='routes_jx'),
    path('debit/', getClientDebits, name='debits_jx'),

    path('report/', ReportView.as_view(), name='report'),
    path('report/client', showReportClientModal, name='report_client_jx'),

    path('clientReport/', ClientReportView.as_view(), name='clientReport'),
    path('clientReport/weight', ClientReportTonnageView.as_view(), name='clientReport_tonnage'),
    path('route/', getRoute, name='routeCR_jx'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)