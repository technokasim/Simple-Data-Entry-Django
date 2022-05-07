from django.urls import path , include
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name='home'),
    path('login', login_request, name='login'),
    path('add-data', addData, name='addData'),
    path('logout', logout_request, name='logout'),

    path('ajax_add', ajax_add, name='ajax_add'),
    path('ajax_update', ajax_update, name='ajax_update'),
    path('ajax_delete', ajax_delete, name='ajax_delete'),
]