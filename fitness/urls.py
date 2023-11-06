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
    path('comentarios/<int:anyo_comentario>/<int:mes_comentario>',views.comentarios_fecha,name='comentarios_fecha')
]
