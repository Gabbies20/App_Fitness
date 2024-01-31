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
    pepe = HistorialEjercicioSerializer(read_only=True,source='historialejercicio_set',many=True)
    class Meta:
        model = Ejercicio
        fields =('nombre','descripcion','tipo_ejercicio','pepe')
        #fields = '__all__'