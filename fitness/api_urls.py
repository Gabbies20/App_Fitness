from django.urls import path
from .api_views import *

urlpatterns = [
    #EJERCICIOS:
    path('ejercicios',ejercicio_list),
    path('ejercicios/busqueda_simple',ejercicio_buscar),
    path('ejercicios/busqueda_avanzada',ejercicio_buscar_avanzado),
    #ENTRENAMIENTOS:
    path('entrenamientos',entrenamiento_list),
    path('entrenamientos/busqueda_simple',entrenamiento_buscar),
]

