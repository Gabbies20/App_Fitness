from django.apps import AppConfig


class FitnessConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fitness'

    # def ready(self):
    #     import fitness.signals 
 # Importa las señales cuando la aplicación esté lista

# signals.py
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Usuario, Perfil_de_Usuario

# @receiver(post_save, sender=Usuario)
# def crear_perfil_usuario(sender, instance, created, **kwargs):
#     if created:
#         Perfil_de_Usuario.objects.create(usuario=instance)



# apps.py
# # En el archivo apps.py de tu aplicación

# from django.apps import AppConfig

# class MiAppConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'mi_app'

#     def ready(self):
#         import mi_app.signals  # Importa las señales cuando la aplicación esté lista
