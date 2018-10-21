
from django.urls import path

from . import views

app_name = 'app2'

urlpatterns = [
    path('', views.index, name='index'),
    path('polaridad', views.Polaridad, name='polaridad'),
    path('historico', views.Historico, name='historico'),
    path('matoneo', views.Matoneo, name='matoneo')
]
