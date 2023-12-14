# App_Fitness
Aplicación Fitness con Django


CREATE ->resuelto completo
BUSQUEDA AVANZADA -> solo texto y descripcion
EDITAR ->resuelto completo
ELIMINAR -> resuelto completo


LAS URLS:
path('promocion/<int:promocion_id>/',views.mostrar_promocion,name='promocion_mostrar'),
    path('promocion/listar',views.lista_promocion,name='lista_promocion'),
    path('create-promocion',views.promocion_create,name='create-promocion'),
    path('promocion/eliminar/<int:promocion_id>/',views.promocion_eliminar,name='promocion_eliminar'),
    path('plan/promocionar/<int:promocion_id>/',views.promocion_editar,name='promocion_editar'),


LOS FORMULARIOS:
class PromocionModelForm(ModelForm):
class BusquedaAvanzadaPromocionForm(forms.Form): 