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
    #URL DE EJERCICIO:
    path('create',views.ejercicio_crear,name='create'),
    path('ejercicio_buscar/',views.ejercicio_buscar,name='ejercicio_buscar'),
    path('ejercicio_busqueda_avanzada/',views.ejercicio_busqueda_avanzada,name='ejercicio_busqueda_avanzada'),
    path('ejercicio/editar/<int:ejercicio_id>/',views.ejercicio_editar,name='ejercicio_editar'),
    path('ejercicio/eliminar/<int:ejercicio_id>/',views.ejercicio_eliminar,name='ejercicio_eliminar'),
    path('ejercicio/<int:ejercicio_id>/',views.ejercicio_mostrar,name='ejercicio_mostrar'),
    #URL DE ENTRENAMIENTOS:
    path('create_entrenamiento',views.entrenamiento_create,name='create_entrenamiento'),
    path('listar_entrenamiento',views.lista_entrenamientos,name='listar_entrenamientos'),
     path('entrenamiento/<int:entrenamiento_id>/',views.entrenamiento_mostrar,name='entrenamiento_mostrar'),
     path('entrenamiento/editar/<int:entrenamiento_id>/',views.entrenamiento_editar,name='entrenamiento_editar'),
     path('entrenamiento/eliminar/<int:entrenamiento_id>/',views.entrenamiento_eliminar,name='entrenamiento_eliminar'),
     #URL PLAN_ENTRENAMIENTO:
    path('plan/listar',views.lista_plan,name='lista_plan'),
     path('create-plan',views.plan_create,name='create-plan'),
     path('plan_buscar/',views.plan_buscar,name='plan_buscar'),
    path('plan_busqueda_avanzada/',views.plan_busqueda_avanzada,name='plan_busqueda_avanzada'),
    path('plan/<int:plan_id>/',views.mostrar_plan,name='mostrar_plan'),
    
    #URL EXAMEN:
    path('promocion/<int:promocion_id>/',views.mostrar_promocion,name='promocion_mostrar'),
    path('promocion/listar',views.lista_promocion,name='lista_promocion'),
    path('create-promocion',views.promocion_create,name='create-promocion'),
    path('promocion/eliminar/<int:promocion_id>/',views.promocion_eliminar,name='promocion_eliminar'),
    path('plan/promocionar/<int:promocion_id>/',views.promocion_editar,name='promocion_editar'),
    path('promocion_busqueda_avanzada/',views.promocion_busqueda_avanzada,name='promocion_busqueda_avanzada'),
     
]
