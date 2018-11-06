
from django.urls import path

from . import views

app_name = 'app2'

urlpatterns = [
    path('', views.index, name='index'),
    path('polaridad', views.Polaridad, name='polaridad'),
    path('historico', views.Historico, name='historico'),
    # path('getDate', views.getDate, name='getDate'),
    path('rankedNetwork', views.rankedNetwork, name='rankedNetwork'),
    path('historicGrowth', views.historicGrowth, name='historicGrowth'),
    path('matoneo', views.Matoneo, name='matoneo'),
    path('clasificar', views.Clasificar, name='clasificar'),
    path('buscar_distribucion', views.BuscarDistribucion, name='buscar_distribucion')
]
