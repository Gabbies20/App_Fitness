from django.db import models

# Create your models here.
class Usuario(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.nombre
    
class Perfil_de_Usuario(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    edad = models.PositiveBigIntegerField()
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
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    descripcion= models.TextField()
    duracion = models.PositiveBigIntegerField()
    dificultad = models.CharField(max_length=25)
    ejercicios = models.ManyToManyField(Ejercicio,through='EntrenamientoEjercicio')
    

class EntrenamientoEjercicio(models.Model):
    entrenamiento = models.ForeignKey(Entrenamiento, on_delete=models.CASCADE)
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE)
    repeticiones = models.PositiveIntegerField()
    peso_utilizado = models.FloatField()
    
class HistorialEjercicio(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE)
    fecha = models.DateField()
    duracion = models.PositiveIntegerField()
    repeticiones = models.PositiveIntegerField()
    peso = models.FloatField()

class Comentario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    entrenamiento = models.ForeignKey(Entrenamiento, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

class PlanEntrenamiento(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    duracion_estimada = models.PositiveIntegerField()
    dificultad = models.CharField(max_length=20)
    entrenamientos = models.ManyToManyField(Entrenamiento, through='EntrenamientoPlan')

class EntrenamientoPlan(models.Model):
    plan_entrenamiento = models.ForeignKey(PlanEntrenamiento, on_delete=models.CASCADE)
    entrenamiento = models.ForeignKey(Entrenamiento, on_delete=models.CASCADE)

class SeguimientoPlanEntrenamiento(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    plan_entrenamiento = models.ForeignKey(PlanEntrenamiento, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    progreso = models.PositiveIntegerField()

class RutinaDiaria(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha = models.DateField()
    descripcion = models.TextField()
    duracion = models.PositiveIntegerField()
    ejercicios = models.ManyToManyField(Ejercicio, through='RutinaEjercicio')

class RutinaEjercicio(models.Model):
    rutina_diaria = models.ForeignKey(RutinaDiaria, on_delete=models.CASCADE)
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE)