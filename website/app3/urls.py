from django.urls import path

from . import views

app_name = 'app3'

urlpatterns = [
    path('', views.index, name='index'),
    path('entidades', views.Entidades, name='entidades'),
    path('preguntas', views.Preguntas, name='preguntas'),
    path('pregunta_enriquecida', views.VistaEnriquecida, name='pregunta_enriquecida'),
    path('pregunta_enriquecida/<int:question_id>', views.VistaEnriquecidaPorId, name='pregunta_enriquecida_por_id'),
    path('navegar', views.NavegarPreguntas, name='navegar'),
]
