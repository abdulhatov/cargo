from django.urls import path
from . import views
from systems import views as system_views

urlpatterns = [
    path('', views.login_request, name='login'),
    path('user_profile/<int:pk>', system_views.UserProfileView.as_view(), name='profile'),
    path('exit', views.logout, name='logout'),
    path('password/', system_views.change_password, name='change_password'),
    path('register', views.register, name='register'),
]
