from django.urls import path
from .api_views import *

urlpatterns = [
    path('ejercicios',ejercicio_list),
    path('ejercicios/busqueda_simple',ejercicio_buscar),
    path('ejercicios/busqueda_avanzada',ejercicio_buscar_avanzado),
    path('entrenamientos',entrenamiento_list),
    
]

