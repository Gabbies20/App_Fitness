from rest_framework import serializers
from .models import *

class EjercicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ejercicio
        fields = ['nombre','descripcion','tipo_ejercicio','usuarios']

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
    usuario = HistorialEjercicioSerializer(read_only=True,source='historialejercicio_set',many=True)
    class Meta:
        model = Ejercicio
        #fields =('nombre','descripcion','tipo_ejercicio','usuario')
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
    ejercicios = EntrenamientoEjercicioSerializer(read_only=True,source='entrenamientoejercicio_set',many=True)
    
    tipo = serializers.CharField(source='get_tipo_display')
    
    class Meta:
        model = Entrenamiento
        fields = ['usuario', 'nombre', 'descripcion', 'duracion', 'tipo', 'ejercicios']


        
        