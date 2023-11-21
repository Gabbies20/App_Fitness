from typing import Any
from django import forms
from .models import *
from django.forms import ModelForm
import re 

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
           
        if len(descripcion) < 5:
            self.add_error('descripcion','La descripcion deber ser superior a 5 caracteres.') 
            
        
        if not re.match("^[a-zA-Z]+$", tipo_ejercicio):
        
           # La función re.match(pattern, string) es una función del módulo re en Python que se utiliza para verificar si el patrón especificado al principio de la cadena coincide. 
        
            self.add_error('tipo_ejercicio','Este campo solo debe contener letras.')
            
        return self.cleaned_data
        
        
        