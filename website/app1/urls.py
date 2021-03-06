
from django.urls import path

from . import views

app_name = 'app1'

urlpatterns = [
    path('', views.index, name='index'),
    path('RF_1', views.RF_1, name='RF_1'),
    path('RF_2', views.RF_2, name='RF_2'),
    path('RF_3', views.RF_3, name='RF_3'),
    path('RF_4', views.RF_4, name='RF_4'),
    path('RA_2', views.RA_2, name='RA_2'),
    path('RA_3', views.RA_3, name='RA_3')
]