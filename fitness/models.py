from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Usuario(AbstractUser):
    ADMINISTRADOR = 1
    CLIENTE = 2
    ENTRENADOR = 3
    ROLES = (
        (ADMINISTRADOR, 'administardor'),
        (CLIENTE, 'cliente'),
        (ENTRENADOR, 'entrenador'),
    )
    
    rol  = models.PositiveSmallIntegerField(
        choices=ROLES,default=1
    )
    
class Entrenador(models.Model):
    usuario = models.OneToOneField(Usuario, 
                             on_delete = models.CASCADE)
    
    
class Suscripcion(models.Model):
    BANCOS = [
        ('CAI', 'Caixa'),
        ('BBV', 'BBVA'),
        ('UNI', 'Unicaja'),
        ('ING', 'ING España'),
    ]
    
    banco = models.CharField(
                            max_length=3,
                            choices=BANCOS,
                            default='ING',
                             )
    
    numero_cuenta = models.CharField(max_length=20)
    titular = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    
class Cliente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    suscripcion = models.OneToOneField(Suscripcion, 
                                       on_delete=models.CASCADE,
                                       null=True, blank=True)
    
    
    def __str__(self):
        return f"Cliente: {self.usuario.username}"
    
class Perfil_de_Usuario(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    edad = models.IntegerField()
    altura = models.FloatField()
    peso = models.FloatField()
    foto_perfil = models.ImageField(upload_to='imagenes/')
    #upload_to --> especifica la carpeta donde se van a guardar las imagenes.
    
    def __str__(self) -> str:
        return  f"Perfil de {self.usuario.username}, Edad: {self.edad}, Altura: {self.altura}, Peso: {self.peso}"
    
    
class Ejercicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    tipo_ejercicio = models.CharField(max_length=20)
    usuarios = models.ManyToManyField(Usuario, through='HistorialEjercicio')
    #usuarios_votos = models.ManyToManyField(Usuario,through='Voto',related_name='usuarios_votos')

    def __str__(self) -> str:
        return self.nombre

class CategoriaEjercicio(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    grupo_muscular_principal = models.CharField(max_length=50)
    ejercicios = models.ManyToManyField('Ejercicio')
    
    def __str__(self) -> str:
        return self.nombre
    
class Entrenamiento(models.Model):
    TIPOS = [
        ('AER','Aeróbico'),
        ('FUE','Fuerza o anaeróbico'),
        ('FUN','Funcional'),
        ('HIT','Hit'),
        ('POT','Potencia'),
    ]
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    descripcion= models.TextField()
    duracion = models.IntegerField()
    tipo = models.CharField(max_length=3,
                            choices=TIPOS,
                            default='HIT',
                            )
    ejercicios = models.ManyToManyField(Ejercicio,through='EntrenamientoEjercicio')
    

class EntrenamientoEjercicio(models.Model):
    entrenamiento = models.ForeignKey(Entrenamiento, on_delete=models.CASCADE)
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE)
    repeticiones = models.IntegerField(default=0)
    peso_utilizado = models.FloatField(default=0)
    
class HistorialEjercicio(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE)
    fecha = models.DateTimeField(default=timezone.now)
    duracion = models.IntegerField(default=0)
    repeticiones = models.IntegerField(default=0)
    peso = models.FloatField(default=0)

class Comentario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    entrenamiento = models.ForeignKey(Entrenamiento, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha = models.DateTimeField(default=timezone.now)

class PlanEntrenamiento(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    duracion_estimada = models.IntegerField()
    dificultad = models.CharField(max_length=20)
    entrenamientos = models.ManyToManyField('Entrenamiento', through='EntrenamientoPlan')
    fecha_inicio = models.DateTimeField(default=timezone.now)
    fecha_fin = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nombre

class EntrenamientoPlan(models.Model):
    plan_entrenamiento = models.ForeignKey(PlanEntrenamiento, on_delete=models.CASCADE)
    entrenamiento = models.ForeignKey(Entrenamiento, on_delete=models.CASCADE)

class SeguimientoPlanEntrenamiento(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    plan_entrenamiento = models.ForeignKey(PlanEntrenamiento, on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField(default=timezone.now)
    fecha_fin = models.DateTimeField(default=timezone.now)
    progreso = models.IntegerField()

class RutinaDiaria(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha = models.DateTimeField(default=timezone.now)
    descripcion = models.TextField()
    duracion = models.IntegerField()
    ejercicios = models.ManyToManyField(Ejercicio, through='RutinaEjercicio')

class RutinaEjercicio(models.Model):
    rutina_diaria = models.ForeignKey(RutinaDiaria, on_delete=models.CASCADE)
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE)
    
    
class Voto(models.Model):
    u_creador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    puntuacion = models.IntegerField(default=1,
                                            validators=[
                                                MaxValueValidator(5),
                                                MinValueValidator(1)
                                            ])
    comentario = models.TextField()
    fecha = models.DateTimeField(default=timezone.now)
    #ejercicio = models.ForeignKey(Ejercicio,on_delete=models.CASCADE)
    

    
class Promocion(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    descuento = models.IntegerField(default=1,
                                            validators=[
                                                MaxValueValidator(100),
                                                MinValueValidator(0)
                                            ])
    fecha = models.DateField()
    usuario = models.ForeignKey(Usuario,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre
    

    