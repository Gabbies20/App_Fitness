# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Usuario, Perfil_de_Usuario

# @receiver(post_save, sender=Usuario)
# def crear_perfil_usuario(sender, instance, created, **kwargs):
#     if created:
#         Perfil_de_Usuario.objects.create(usuario=instance)
