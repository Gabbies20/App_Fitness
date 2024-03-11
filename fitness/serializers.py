import re
from rest_framework import serializers
from .models import *
from django.utils import timezone



class MusculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Musculo
        fields = '__all__'

class GrupoMuscularSerializer(serializers.ModelSerializer):
    musculos = MusculoSerializer(many=True)
    class Meta:
        model = GrupoMuscular
        fields = ('id','nombre','nivel','musculos')


class EjercicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ejercicio
        fields = ['id','nombre','descripcion','tipo_ejercicio','usuarios','grupos_musculares']

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
    grupos_musculares = GrupoMuscularSerializer(many=True)
    class Meta:
        model = Ejercicio
        fields =('id','nombre','descripcion','tipo_ejercicio','usuarios','grupos_musculares')
        #fields = '__all__'
    
    
class EjercicioSerializerCreate(serializers.ModelSerializer):
    
    class Meta:
        model = Ejercicio
        fields = ['nombre','descripcion','tipo_ejercicio',
                  'usuarios','grupos_musculares']
    
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
        if not tipo_ejercicio:
            raise serializers.ValidationError('El campo tipo_ejercicio no puede estar vacío')
        if not tipo_ejercicio.isalpha():
            raise serializers.ValidationError('El tipo de ejercicio solo puede contener letras')
        return tipo_ejercicio
       
    def validate_grupos_musculares(self, grupos_musculares):
        if not grupos_musculares:
            raise serializers.ValidationError("Debe seleccionar al menos un grupo muscular.")
        return grupos_musculares
        
    def create(self, validated_data):
        usuarios = self.initial_data['usuarios']
        if len(usuarios) < 1:
            raise serializers.ValidationError({'usuarios': ['Debe seleccionar al menos un usuario.']})
    
        
        ejercicio = Ejercicio.objects.create(
            nombre = validated_data['nombre'],
            descripcion = validated_data['descripcion'],
            tipo_ejercicio = validated_data['tipo_ejercicio']  
        )
        ejercicio.grupos_musculares.set(validated_data['grupos_musculares'])
        for usuario_id in usuarios:
            usuario = Usuario.objects.get(id=usuario_id)
            HistorialEjercicio.objects.create(usuario=usuario, ejercicio=ejercicio)
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
        print(instance)
        instance.grupos_musculares.set(validated_data["grupos_musculares"])

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


#ENTRENAMIENTO:

class EntrenamientoEjercicioSerializer(serializers.ModelSerializer):
    ejercicio = EjercicioSerializer()
    class Meta:
        model = EntrenamientoEjercicio
        fields = '__all__'

class EntrenamientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrenamiento
        fields = '__all__'
        
class EntrenamientoMejoradoSerializer(serializers.ModelSerializer):
    
    usuario = UsuarioSerializer()
    
    ejercicios = EntrenamientoEjercicioSerializer(read_only=True,source='entrenamientoejercicio_set',many=True)
    
    tipo = serializers.CharField(source='get_tipo_display')
    
    class Meta:
        model = Entrenamiento
        fields = ['id','usuario', 'nombre', 'descripcion', 'duracion', 'tipo', 'ejercicios']



class EntrenamientoSerializerCreate(serializers.ModelSerializer):
    
    class Meta:
        model = Entrenamiento
        fields = [
            'usuario','nombre','descripcion','duracion','tipo','ejercicios'
        ]
        
    def validate_usuario(self, usuario):
        # Validar el campo 'usuario' aquí
        # Por ejemplo, podrías comprobar si el usuario existe en tu base de datos
        if not Usuario.objects.filter(id=usuario.id).exists():
            raise serializers.ValidationError("El usuario especificado no existe.")
        return usuario
    
    def validate_nombre(self, nombre):
    # Validar el campo 'nombre' aquí
        if len(nombre) < 2:
            raise serializers.ValidationError("El nombre debe tener al menos 3 caracteres.")
        return nombre
    
    def validate_descripcion(self, descripcion):
    # Validar el campo 'descripcion' aquí
        if len(descripcion) < 2:
            raise serializers.ValidationError("El descripcion debe tener al menos 3 caracteres.")
        return descripcion
    
    
    def validate_duracion(self, duracion):
    # Validar el campo 'duracion' aquí
        if duracion <= 0:
            raise serializers.ValidationError("La duración debe ser un número positivo.")
        return duracion
    
    def validate_tipo(self, tipo):
        # Validar el campo 'tipo' aquí
        # Por ejemplo, podrías comprobar si el tipo es uno de los valores permitidos
        tipos_permitidos = ['AER', 'FUE', 'FUN', 'HIT', 'POT']
        if tipo not in tipos_permitidos:
            raise serializers.ValidationError("El tipo especificado no es válido.")
        return tipo
    
    #def validate_ejercicios(self, ejercicios):
        # Validar el campo 'ejercicios' aquí
        # Por ejemplo, podrías comprobar si todos los ejercicios existen en tu base de datos
        #   for ejercicio_id in ejercicios:
        #      if not Ejercicio.objects.filter(id=ejercicio_id).exists():
        #         raise serializers.ValidationError(f"El ejercicio con ID {ejercicio_id} no existe.")
        #return ejercicios
    
    
    def create(self, validated_data):
        ejercicios= self.initial_data['ejercicios']
        if len(ejercicios) < 1:
            raise serializers.DjangoValidationError(
                {'ejercicios':
                    ['Debe seleccionar al menos 1 ejercicio']}
            )
            
        entrenamiento = Entrenamiento.objects.create(
            nombre = validated_data['nombre'],
            descripcion = validated_data['descripcion'],
            duracion = validated_data['duracion'],
            tipo = validated_data['tipo'],
            usuario =  validated_data["usuario"]
        )

        
        for ejercicio in ejercicios:
            ejercicio = Ejercicio.objects.get(id=ejercicio)
            EntrenamientoEjercicio.objects.create(ejercicio=ejercicio,entrenamiento=entrenamiento)
        return entrenamiento
    
    def update(self,instance, validated_data):
        ejercicios = self.initial_data['ejercicios']
        if len(ejercicios) < 1:
            raise serializers.ValidationError(
                {'ejercicios':'Debe seleccionar al menos un ejercico'
                    
                })
            
        instance.nombre = validated_data['nombre']
        instance.descripcion = validated_data['descripcion']
        instance.duracion = validated_data['duracion']
        instance.tipo = validated_data['tipo']
        instance.usuario = validated_data['usuario']
        instance.save()
        
        #Actualizamos los ejercicios que es una relación ManytoMany y tabla intermedia, se eliminan clear():
        instance.ejercicios.clear()
        for ejercicio in ejercicios:
            modeloEjercicio =Ejercicio.objects.get(id=ejercicio)
            EntrenamientoEjercicio.objects.create(entrenamiento=instance,ejercicio=modeloEjercicio) 
        
        return instance
                
                
            
class EntrenamientoSerializerActualizarDescripcion(serializers.ModelSerializer):
    class Meta:
        model = Entrenamiento
        fields = ['descripcion']
    
    def validate_descripcion(self,descripcion):
        entrenamientoDescripcion = Entrenamiento.objects.filter(descripcion=descripcion).first()
        if(not entrenamientoDescripcion is None and entrenamientoDescripcion.id != self.instance.id):
            raise serializers.ValidationError('No se ha modificado la descripcion.')
        return descripcion


#COMENTARIOS:        
class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = '__all__'


class ComentarioMejoradoSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()
    entrenamiento = EntrenamientoSerializer()
    
    class Meta:
        model = Comentario
        fields = ['id','texto','fecha','usuario','entrenamiento']
        
class ComentarioSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = ['usuario','entrenamiento','texto','fecha'] 
        
    def validate_usuario(self,usuario ):
        # Validar que el usuario exista en tu sistema o en tu base de datos
        # Aquí puedes agregar la lógica de validación que necesites
        if not Usuario.objects.filter(username=usuario).exists():
            raise serializers.ValidationError("El usuario no existe.")
        return usuario

    def validate_entrenamiento(self, entrenamiento):
        # Validar que el entrenamiento exista en tu sistema o en tu base de datos
        # Aquí puedes agregar la lógica de validación que necesites
        nombre_entrenamiento = entrenamiento.nombre
        if not Entrenamiento.objects.filter(nombre=nombre_entrenamiento).exists():
            print(nombre_entrenamiento)
            raise serializers.ValidationError("El entrenamiento no existe.")
        return entrenamiento


    def validate_texto(self, texto):
        # Validar que el texto no esté vacío o tenga una longitud mínima requerida
        # Aquí puedes agregar la lógica de validación que necesites
        if not texto.strip():
            raise serializers.ValidationError("El texto no puede estar vacío.")
        return texto

    from datetime import datetime

    def validate_fecha(self, fecha):
        # Convertir fecha a datetime.date
        fecha_actual = timezone.now().date()

        # Comparar la fecha recibida con la fecha actual
        if fecha.date() < fecha_actual:
            raise serializers.ValidationError("La fecha no puede ser en el pasado.")
        return fecha


    def create(self, validated_data):
        comentario = Comentario.objects.create(
            
            usuario=validated_data['usuario'],  # Asignar el ID del usuario
            entrenamiento=validated_data['entrenamiento'], # Asignar el ID del entrenamiento
            texto=validated_data['texto'],
            fecha=validated_data['fecha']
        )
        return comentario
    def update(self,instance,validated_data):
        
        instance.usuario = validated_data['usuario']
        instance.entrenamiento = validated_data['entrenamiento']
        instance.texto = validated_data['texto']
        instance.fecha = validated_data['fecha']
        instance.save()
        return instance
    
            
class ComentarioSerializerActualizarTexto(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = ['texto']
    
    def validate_texto(self,texto):
        comentarioNombre = Comentario.objects.filter(texto=texto).first()
        if(not comentarioNombre is None and comentarioNombre.id != self.instance.id):
            raise serializers.ValidationError('Texto fallido')
        return texto



    
    
class PerfilUsuarioSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()
    class Meta:
        model = Perfil_de_Usuario
        fields = ['usuario','edad','altura','peso','foto_perfil']
        
        
class PerfilUsuarioActualizarSerializer():
    class Meta:
        model = Perfil_de_Usuario
        fields = ['usuario','edad','altura','peso','gmail']
    
    def validate_edad(self, edad):
        if edad <= 0:
            raise serializers.ValidationError("La edad debe ser mayor que cero.")
        return edad

    def validate_altura(self, altura):
        if altura <= 0 or altura > 300:
            raise serializers.ValidationError("La altura debe estar entre 0 y 300.")
        return altura

    def validate_peso(self, peso):
        if peso <= 0 or peso > 1000:
            raise serializers.ValidationError("El peso debe estar entre 0 y 1000.")
        return peso

    def validate_gmail(self, gmail):
        # Validar el formato del correo electrónico
        if gmail:
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', gmail):
                raise serializers.ValidationError("El correo electrónico no tiene un formato válido.")
        return gmail
    
    
    
    
class UsuarioSerializerRegistro(serializers.Serializer):
    username = serializers.CharField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()
    email = serializers.EmailField()
    rol = serializers.IntegerField()
    
    