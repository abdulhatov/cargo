from django.urls import path
from .views import *
from .viewRecTran import *
from .print import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'route'
urlpatterns = [
    path('list/', ListRoute.as_view(), name='list_route_url'),
    path('route/add/', CreateRoute.as_view(), name='create_route_url'),
    path('routeIDD/', showRouteModal, name='show_routeRT_url'),
    path('route/update/<int:pk>/', UpdateRouteView.as_view(), name='update_route_url'),
    path('route/delete/<int:pk>/', deleteRoute, name='delete_route_url'),

    path('routeID/<int:pk>/', ShowRouteID.as_view(), name='show_route_ID_url'),
    path('routeID_bag_report_old/<int:pk>/', RouteBagReportOld.as_view(), name='route_bag_report_old'),
    path('routeID_bag_report/<int:pk>/', RouteBagReportView.as_view(), name='route_bag_report'),
    path('routeID_num_places/<int:pk>/', RouteNumberOfPlaces.as_view(), name='route_num_places'),
    path('routeID_num_places_client/<int:pk>/', RouteNumberOfPlacesClient.as_view(), name='route_num_places_client'),
    path('routeID_num_place_agent/<int:pk>/', RouteNumberOfPlacesAgent.as_view(), name='route_num_places_agent'),
    path('routeID_count_prod/<int:pk>/', RouteCountProducts.as_view(), name='route_count_products'),

    path('routeIDprint/<int:pk>/', printRouteID, name='print_routeID_url'),
    path('routebagReportOldprint/<int:pk>/', printRouteBagReportOld, name='print_bagReport_old'),
    path('routebagReportprint/<int:pk>/', printRouteBagReport, name='print_bagReport'),
    path('routeNumberOfPlacesprint/<int:pk>/', printRouteNumberOfPlaces, name='print_number_of_places'),
    path('routeNumberOfPlacesAgentprint/<int:pk>/', printRouteNumberOfPlacesAgent, name='print_num_pl_agent'),
    path('routeProductsprint/<int:pk>/', printRouteCountProducts, name='print_products'),

    path('route_select/', selectedRoute, name='selected_route'),
    path('route_location/', change_location, name='change_location'),


    path('ReceptionTransmission/', ListReceptionTransmission.as_view(), name='list_rt'),
    path('ReceptionTransmission/history/', ListReceptionTransmissionHistory.as_view(), name='list_rt_history'),
    path('ReceptionTransmission/history/<int:pk>/', ReceptionTransmissionContractHistory, name='rt_history_id'),
    path('ReceptionTransmission/RecTransCont/<int:pk>/', ReceptionTransmissionContract, name='rt_id'),
    path('create_RecTran/', ReceptionTransmissionAddView.as_view(), name='add_rt'),
    path('ReceptionTransmission/update_RecTran/<int:pk>/', ReceptionTransmissionEditView.as_view(), name='edit_rt'),
    path('delete_RecTran/<int:pk>/', recTrans_delete, name='delete_rt'),
    path('export/<int:pk>/', export_to_pdf, name='export_pdf'),
    path('search/', searchByBagNumber, name='search_recTran_url'),
    path('search2/', SeatsAndWeightReport, name='search2_recTran_url'),

    path('reg_places', RegistrationPlaceView.as_view(), name='reg_places'),
    path('reg_places_add', RegPlacesAddView.as_view(), name='reg_places_add'),
    path('edit/reg_places/<int:pk>/', RegPlacesEditView.as_view(), name='reg_places_edit'),
    path('delete/reg_places/<int:id>/', reg_places_delete, name='reg_places_delete'),

    path('directions', DirectionsView.as_view(), name='directions'),
    path('directions_add', DirectionAddView.as_view(), name='directions_add'),
    path('edit/directions/<int:pk>', DirectionEditView.as_view(), name='directions_edit'),
    path('delete/directions/<int:id>', directions_delete, name='directions_delete'),

    path('currency', CurrencyView.as_view(), name='currency'),
    path('currency_add', CurrencyAddView.as_view(), name='currency_add'),
    path('edit/currency/<int:pk>', CurrencyEditView.as_view(), name='currency_edit'),
    path('delete/currency/<int:id>', currency_delete, name='currency_delete'),

    path('service_price', ServicePriceView.as_view(), name='service_price'),
    path('service_price/add', ServicePriceAddView.as_view(), name='service_price_add'),
    path('service_price/view/<int:pk>', ServicePriceViewID.as_view(), name='service_price_view_id'),
    path('service_price/edit/<int:pk>', ServicePriceEditView.as_view(), name='service_price_edit'),
    path('delete/service_price/<int:id>', service_price_delete, name='service_price_delete'),

    path('financial_report/', FinancialReport.as_view(), name='financial_report'),
    path('checkBagNumber/', checkBagNumber, name='check_bagNum_jx'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
