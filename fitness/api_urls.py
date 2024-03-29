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
    path('entrenamiento/<int:entrenamiento_id>',entrenamiento_obtener),
    path('entrenamientos/busqueda_simple',entrenamiento_buscar),
    path('entrenamientos/busqueda_avanzada',entrenamiento_buscar_avanzado),
    path('entrenamientos/crear',entrenamiento_create),
    path('entrenamientos/editar/<int:entrenamiento_id>',entrenamiento_editar),
    path('entrenamientos/actualizar/descripcion/<int:entrenamiento_id>',entrenamiento_actualizar_descripcion),
    path('entrenamientos/eliminar/<int:entrenamiento_id>',entrenamiento_eliminar,name='entrenamiento_eliminar'),
    #COMENTARIOS:
    path('comentarios',comentario_list),
    path('comentario/<int:comentario_id>',comentario_obtener),
    path('comentarios/busqueda_simple',comentario_buscar),
    path('comentarios/busqueda_avanzada',comentario_buscar_avanzado),
    path('comentarios/crear',comentario_create),
    path('comentarios/editar/<int:comentario_id>',comentario_editar),
    path('comentarios/actualizar/nombre/<int:comentario_id>',comentario_actualizar_nombre),
    path('comentarios/eliminar/<int:comentario_id>',comentario_eliminar,name='comentario_eliminar'),
    
    
    #FUNCIONALIDADES DE MIS COMPAÑEROS:
    path('entrenamiento-ejercicios/<int:entrenamiento_id>',ejercicios_entrenamiento),
    path('grupos-musculares',grupos_musculares_list),
    #path('historiales',obtener_historial),
    path('historiales/<int:usuario_id>',obtener_historial),
    path('perfil-usuario/<int:usuario_id>',obtener_perfil_usuario,name="perfil-usuario"),
    path('perfiles',perfil_list),
    path('usuario/<int:usuario_id>',obtener_usuario),
    path('ejercicios/musculos/busqueda',ejercicio_buscar_musculos),
    #REGISTRO:
    path('registrar/usuario',registrar_usuario.as_view()),
    path('usuario/token/<str:token>',obtener_usuario_token),
]


