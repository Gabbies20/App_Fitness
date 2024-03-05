from rest_framework import serializers
from .models import *
from django.utils import timezone


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


#ENTRENAMIENTO:

class EntrenamientoEjercicioSerializer(serializers.ModelSerializer):
    ejercicio = EjercicioSerializer()
    class MEta:
        model = EntrenamientoEjercicio
        fields = '__all__'

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
            if not Usuario.objects.filter(id=usuario).exists():
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
                tipo = validated_data['tipo']
            )
            entrenamiento.usuarios.set(validated_data['usuarios'])
            
            for ejercicio in ejercicios:
                modeloEntrenamientoEjercicio = EntrenamientoEjercicio.objects.get(id=ejercicio)
                EntrenamientoEjercicio.objects.create(ejercicio=modeloEntrenamientoEjercicio,entrenamiento=entrenamiento)
            return ejercicio
        
        
class EntrenamientoSerializerActualizarNombre():
    pass


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
        fields = ['texto','fecha','usuario','entrenamiento']
        
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
            texto=validated_data['texto'],
            fecha=validated_data['fecha'],
            usuario=validated_data['usuario'],  # Asignar el ID del usuario
            entrenamiento=validated_data['entrenamiento']  # Asignar el ID del entrenamiento
        )
        return comentario


class ComentarioSerializerActualizarTexto():
    pass


class UsuarioSerializerRegistro(serializers.Serializer):
    username = serializers.CharField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()
    email = serializers.EmailField()
    rol = serializers.IntegerField()
    
    def validate_username(self,username):
        usuario = Usuario.objects.filter(username=username).first()
        if(not usuario is None):
            raise serializers.ValidationError('Ya existe un usuario con ese nombre')
        return username