from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    path('ejercicios/listar',views.lista_ejercicios,name='lista_ejercicios'),
    path('informacion_usuario/',views.informacion_usuario,name='informacion_usuario'),
    path('perfil_usuario/<int:id_usuario>/',views.perfil_usuario,name='perfil_usuario'),
    path('entrenamientos',views.entrenamiento_aerobico,name='entrenamientos'),
    path('usuario_H',views.usuario_con_h,name='usuario_H'),
    path('entrenamiento/<int:entrenamiento_id>/comentarios/', views.comentarios_entrenamiento, name='comentarios_entrenamiento'),
    path('comentarios/<int:anyo_comentario>/<int:mes_comentario>',views.comentarios_fecha,name='comentarios_fecha'),
    path('categoria/',views.categoria_lisos,name='categoria_lisos'),
    path('lista_entrenamientos',views.lista_entrenamientos,name='lista_entrenamientos'),
    path('grupo_muscular/<str:grupo_muscular>/', views.grupo_muscular,name='grupo_muscular'),
    path('usuarios_sin_comentarios/', views.usuarios_sin_comentarios, name='usuarios_sin_comentarios'),
    path('historial_ejercicios/<int:usuario_id>/', views.historial_ejercicios_usuario, name='historial_ejercicios_usuario'),
    path('ultimo_voto/<int:id_ejercicio>',views.ultimo_voto,name='ultimo_voto'),
    path('banco_tipo/<str:texto>',views.cuentas_bancarias,name='banco_tipo'),
    path('puntuacion_tres/<int:id_usuario>',views.puntuacion_tres,name='puntuacion_tres'),
    path('usuarios_sin_votos',views.usuarios_sin_votos,name='usuarios_sin_votos'),
    path('create',views.ejercicio_crear,name='create'),
    #Url de búsqueda:
    path('ejercicio_buscar/',views.ejercicio_buscar,name='ejercicio_buscar'),
]
