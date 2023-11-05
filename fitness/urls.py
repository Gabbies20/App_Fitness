from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    path('ejercicios/listar',views.lista_ejercicios,name='lista_ejercicios'),
    path('informacion_usuario/',views.informacion_usuario,name='informacion_usuario'),
    path('perfil_usuario/<int:id_usuario>/',views.perfil_usuario,name='perfil_usuario')
]
