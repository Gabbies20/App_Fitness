from django.contrib import admin
from .models import Usuario,Perfil_de_Usuario,Ejercicio,CategoriaEjercicio,Entrenamiento,EntrenamientoEjercicio,HistorialEjercicio,Comentario,PlanEntrenamiento,EntrenamientoPlan,SeguimientoPlanEntrenamiento,RutinaDiaria,RutinaEjercicio

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Perfil_de_Usuario)
admin.site.register(Ejercicio)
admin.site.register(CategoriaEjercicio)
admin.site.register(Entrenamiento)
admin.site.register(EntrenamientoEjercicio)
admin.site.register(HistorialEjercicio)
admin.site.register(Comentario)
admin.site.register(PlanEntrenamiento)
admin.site.register(EntrenamientoPlan)
admin.site.register(SeguimientoPlanEntrenamiento)
admin.site.register(RutinaDiaria)
admin.site.register(RutinaEjercicio)
