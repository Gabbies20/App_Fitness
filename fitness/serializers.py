from rest_framework import serializers
from .models import *

class EjercicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ejercicio
        fields = ['id','nombre','descripcion','tipo_ejercicio','usuarios']

class UsuarioSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Usuario
        fields = '__all__'
        
      
class HistorialEjercicioSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()
    class Meta:
        model = HistorialEjercicio
        fields = '__all__'
        
class EjercicioMejoradoSerializer(serializers.ModelSerializer):
    usuarios = HistorialEjercicioSerializer(read_only=True,source='historialejercicio_set',many=True)
    class Meta:
        model = Ejercicio
        fields =('id','nombre','descripcion','tipo_ejercicio','usuarios')
        #fields = '__all__'
    
    
class EjercicioSerializerCreate(serializers.ModelSerializer):
    
    class Meta:
        model = Ejercicio
        fields = ['nombre','descripcion','tipo_ejercicio',
                  'usuarios']
    
    def validate_nombre(self,nombre):
        ejercicioNombre = Ejercicio.objects.filter(nombre=nombre).first()
        if(not ejercicioNombre is None
           ):
             if(not self.instance is None and ejercicioNombre.id == self.instance.id):
                 pass
             else:
                raise serializers.ValidationError('Ya existe un ejercicio con ese nombre')
            
        
        return nombre
    
    def validate_descripcion(self,descripcion):
        if len(descripcion) < 10:
             raise serializers.ValidationError('Al menos debes indicar 10 caracteres')
        return descripcion
    
    def validate_tipo_ejercicio(self, tipo_ejercicio):
        # Verifica si el campo tipo_ejercicio está vacío
        if not tipo_ejercicio:
            raise serializers.ValidationError('El campo tipo_ejercicio no puede estar vacío')

        # Verifica si el campo tipo_ejercicio contiene solo letras
        if not tipo_ejercicio.isalpha():
            raise serializers.ValidationError('El campo tipo_ejercicio solo puede contener letras')

        return tipo_ejercicio
    #def validate_fecha_publicacion(self,fecha_publicacion):
     #   fechaHoy = date.today()
      #  if fechaHoy >= fecha_publicacion:
       #     raise serializers.ValidationError('La fecha de publicacion debe ser mayor a Hoy')
       # return fecha_publicacion
    
    
    def create(self, validated_data):
        usuarios = self.initial_data['usuarios']
        if len(usuarios) < 1:
            raise serializers.ValidationError(
                    {'usuarios':
                    ['Debe seleccionar al menos un usuarios.']
                    })
        
        ejercicio = Ejercicio.objects.create(
            nombre = validated_data["nombre"],
            descripcion = validated_data["descripcion"],
            tipo_ejercicio = validated_data["tipo_ejercicio"]
        )
        #libro.autores.set(validated_data["autores"])
       
        for usuario in usuarios:
            modeloUsuario = Usuario.objects.get(id=usuario)
            HistorialEjercicio.objects.create(usuario=modeloUsuario,ejercicio=ejercicio)
        return ejercicio
    
    def update(self, instance, validated_data):
        usuarios = self.initial_data['usuarios']
        if len(usuarios) < 2:
            raise serializers.ValidationError(
                    {'usuarios':
                    ['Debe seleccionar al menos dos usuarios']
                    })
        
        instance.nombre = validated_data["nombre"]
        instance.descripcion = validated_data["descripcion"]
        instance.tipo_ejercicio = validated_data["tipo_ejercicio"]
        instance.save()
        
        #instance.autores.set(validated_data["autores"])

        instance.usuarios.clear()
        for usuario in usuarios:
            modeloUsuario = Usuario.objects.get(id=usuario)
            HistorialEjercicio.objects.create(usuario=modeloUsuario,ejercicio=instance)
        return instance

class EjercicioSerializerActualizarNombre(serializers.ModelSerializer):
 
    class Meta:
        model = Ejercicio
        fields = ['nombre']
    
    def validate_nombre(self,nombre):
        ejercicioNombre = Ejercicio.objects.filter(nombre=nombre).first()
        if(not ejercicioNombre is None and ejercicioNombre.id != self.instance.id):
            raise serializers.ValidationError('Ya existe un ejercicio con ese nombre')
        return nombre

class EntrenamientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrenamiento
        fields = '__all__'
        
class EntrenamientoEjercicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrenamientoEjercicio
        fields = '__all__'
        
class EntrenamientoMejoradoSerializer(serializers.ModelSerializer):
    
    usuario = UsuarioSerializer()
    
    # No es necesario especificar source para el campo 'ejercicios'.
    ejercicios = EjercicioSerializer(read_only=True,many=True)
    
    tipo = serializers.CharField(source='get_tipo_display')
    
    class Meta:
        model = Entrenamiento
        fields = ['usuario', 'nombre', 'descripcion', 'duracion', 'tipo', 'ejercicios']


        
class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = '__all__'


class ComentarioMejoradoSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()
    entrenamiento = EntrenamientoSerializer()
    
    class Meta:
        model = Comentario
        fields = ['texto','fecha','usuario','entrenamiento']