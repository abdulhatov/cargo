from django.urls import path
from .views import *
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'systems'
urlpatterns = [

    path('users', views.UsersView.as_view(), name='users'),
    path('user_add', views.UserAddView.as_view(), name='user_add'),

    path('user_edit/<int:pk>', views.UserEditView.as_view(), name='user_edit'),

    path('delete/user/<int:pk>', views.delete_user, name='user_delete'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)