from django.urls import path
from .api_views import *

urlpatterns = [
    #EJERCICIOS:
    path('ejercicios',ejercicio_list),
    path('ejercicios/busqueda_simple',ejercicio_buscar),
    path('ejercicios/busqueda_avanzada',ejercicio_buscar_avanzado),
    path('usuarios',usuarios_list),
    #ENTRENAMIENTOS:
    path('entrenamientos',entrenamiento_list),
    path('entrenamientos/busqueda_simple',entrenamiento_buscar),
    path('entrenamientos/busqueda_avanzada',entrenamiento_buscar_avanzado),
    #COMENTARIOS:
    path('comentarios',comentario_list),
    path('comentarios/busqueda_simple',comentario_buscar),
    path('comentarios/busqueda_avanzada',comentario_buscar_avanzado),
]

