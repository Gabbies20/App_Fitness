from typing import Any
from django import forms
from .models import *
from django.forms import ModelForm

class EjercicioModelForm(ModelForm):
    class Meta:
        model = Ejercicio
        fields = ['nombre','descripcion','tipo_ejercicio']
        
        labels = {
            'nombre': ('Nombre del Ejercicio'),
        }
        help_texts = {
            'nombre': ('200 caracteres como máximo')
        }
    
    
    def clean(self):
        
        super().clean()
        
        
        #Primero obtenemos los campos 
        nombre = self.cleaned_data.get('nombre')
        descripcion = self.cleaned_data.get('descripcion')
        tipo_ejercicio = self.cleaned_data.get('tipo_ejercicio')
        
        ejercicioNombre = Ejercicio.objects.filter(nombre=nombre).first()
        if(not ejercicioNombre is None):
            self.add_error('nombre','Ya existe un ejercicio con ese nombre.')
            
        return self.cleaned_data
        
        