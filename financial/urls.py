from django.urls import path
from .views import *
from .prints import *
from .search import *
from .salary import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'financial'
urlpatterns = [
    path('cash_box/', CashBoxView.as_view(), name='cash_box'),
    path('cash_box/print', printCashBoxes, name='cash_box_print'),
    path('cash_box_add/', CashBoxAddView.as_view(), name='cash_box_add'),

    path('reports/', Reports.as_view(), name='reports'),
    path('get_article/', getArticle, name='reports_article_js'),

    path('articles/', ArticlesView.as_view(), name='articles'),
    path('article/add/', ArticlesViewAdd.as_view(), name='article_add'),
    path('article/edit/<int:pk>/', ArticlesEditView.as_view(), name='article_edit'),
    path('article/delete/<int:id>/', article_delete, name='article_delete'),

    path('operations/', OperationsView.as_view(), name='operations'),

    path('operations/income/view/<int:pk>/', IncomeId.as_view(), name='operations_income_ID'),
    path('operations/consumption/view/<int:pk>', ConsumptionId.as_view(), name='operations_cons_ID'),
    path('operations/payroll/view/<int:pk>', PayrollID.as_view(), name='operations_payroll_ID'),
    path('operations/income/print/<int:pk>', IncomePrint.as_view(), name='operations_income_print'),

    path('operations/delete/<int:pk>', deleteOperations, name='operations_delete'),

    path('operations/income/client/add/', OperationsIncomeClientAdd.as_view(), name='operations_in_client_add'),
    path('operations/income/client/edit/<int:pk>/', OperationsIncomeClientEdit.as_view(), name='operations_in_client_edit'),

    path('operations/income/counterparty/add/', OperationsIncomeAgentAdd.as_view(), name='operations_in_agent_add'),
    path('operations/income/counterparty/edit/<int:pk>/', OperationsIncomeAgentEdit.as_view(), name='operations_in_agent_edit'),

    path('operations/income/various/add/', OperationsVarioustAdd.as_view(), name='operations_in_various_add'),
    path('operations/income/various/edit/<int:pk>', OperationsIncomeVariousEdit.as_view(), name='operations_in_various_edit'),

    path('operations/consumption/employee/add/', ConsumptionEmployeeAdd.as_view(), name='cons_employee_add'),
    path('operations/consumption/employee/edit/<int:pk>', ConsEmployeeEdit.as_view(), name='cons_employee_edit'),
    path('operations/consumption/employee/print/<int:pk>', consEmployee_print, name='cons_employee_print'),

    path('operations/consumption/agent/add/', ConsumptionAgentAdd.as_view(), name='cons_agent_add'),
    path('operations/consumption/agent/edit/<int:pk>', ConsumptionAgentEdit.as_view(), name='cons_agent_edit'),
    path('operations/consumption/agent/print/<int:pk>', consAgent_print, name='cons_agent_print'),

    path('operations/consumption/agent_of_client/', ConsAgentClientAdd.as_view(), name='cons_agent_client_add'),
    path('operations/consumption/agent_of_client/edit/<int:pk>', ConsAgentClientEdit.as_view(), name='cons_agent_client_edit'),
    path('operations/consumption/agent_of_client/print/<int:pk>', consAgentClient_print, name='cons_agent_client_print'),

    path('operations/consumption/various/', OperationsConsVarioustAdd.as_view(), name='cons_various_add'),
    path('operations/consumption/various/edit/<int:pk>', OperationsConsVarioustEdit.as_view(), name='cons_various_edit'),
    path('operations/consumption/various/print/<int:pk>', consVarious_print, name='cons_various_print'),

    path('operations/payroll/emp/add/', PaymentStatementEmployeeAddView.as_view(), name='payroll_emp_add'),
    path('operations/payroll/emp/edit/<int:pk>', PaymentStatementEmployeeEditView.as_view(), name='ps_emp_edit'),
    path('operations/payroll/emp/print/<int:pk>', psEmployee_print, name='ps_emp_print'),

    path('operations/payroll/agent/add/', PaymentStatementAgentAddView.as_view(), name='payroll_agent_add'),
    path('operations/payroll/agent/edit/<int:pk>', PaymentStatementAgentEditView.as_view(), name='ps_agent_edit'),
    path('operations/payroll/agent/print/<int:pk>', psAgent_print, name='ps_agent_print'),

    path('operations/consumption/cash_moving/', OperationsConsCashMovingAdd.as_view(), name='cons_cash_moving_add'),
    path('operations/consumption/cash_moving/<int:pk>', OperationsConsCashMovingID.as_view(),
         name='cons_cash_moving_ID'),
    path('operations/consumption/cash_moving/edit/<int:pk>', OperationsConsCashMovingEdit.as_view(),
         name='cons_cash_moving_edit'),
    path('operations/consumption/cash_moving/print/<int:pk>', consCashMoving_print, name='cons_cash_moving_print'),

    path('advance/', AdvanceView.as_view(), name='prepaid'),
    path('fines', FinesView.as_view(), name='fines'),

    path('work_pay', WorkPayView.as_view(), name='work_pay'),
    path('work_pay/emp/<int:pk>', WorkPayEmpView.as_view(), name='work_pay_emp'),

    path('loading_pay', LoadingPayView.as_view(), name='loading_pay'),
    path('loading_pay/emp/<int:pk>', LoadingPayEmpView.as_view(), name='loading_pay_emp'),

    path('salary', SalaryView.as_view(), name='salary'),
    path('salaryID/<int:pk>', SalaryViewID.as_view(), name='salary_id'),
    path('printsalary/<int:pk>', printSalaryID, name='salary_print'),
    path('salary/add/', SalaryAddView.as_view(), name='salary_add'),
    path('salary/edit/<int:pk>', SalaryEditView.as_view(), name='salary_edit'),
    path('salary/delete/<int:pk>', deleteSalary, name='salary_delete'),

    path('salary/emp/', showEmployeeModal, name='salary_show_emp_jx'),
    path('salary/emp_edit/', showEmployeeEditModal, name='salary_show_emp_edit_jx'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)