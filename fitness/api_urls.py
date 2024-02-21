from django.urls import path
from .api_views import *

urlpatterns = [
    #EJERCICIOS:
    path('ejercicios',ejercicio_list),
    path('ejercicio/<int:ejercicio_id>',ejercicio_obtener),
    path('ejercicios/busqueda_simple',ejercicio_buscar),
    path('ejercicios/busqueda_avanzada',ejercicio_buscar_avanzado),
    path('usuarios',usuarios_list),
    path('ejercicios/crear',ejercicio_create),
    path('ejercicios/editar/<int:ejercicio_id>',ejercicio_editar),
    path('ejercicios/actualizar/nombre/<int:ejercicio_id>',ejercicio_actualizar_nombre),
    path('ejercicios/eliminar/<int:ejercicio_id>',ejercicio_eliminar,name='libro_eliminar'),
    #ENTRENAMIENTOS:
    path('entrenamientos',entrenamiento_list),
    path('entrenamientos/busqueda_simple',entrenamiento_buscar),
    path('entrenamientos/busqueda_avanzada',entrenamiento_buscar_avanzado),
    #COMENTARIOS:
    path('comentarios',comentario_list),
    path('comentarios/busqueda_simple',comentario_buscar),
    path('comentarios/busqueda_avanzada',comentario_buscar_avanzado),
]

