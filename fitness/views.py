from django.shortcuts import render
from .models import Ejercicio

# Create your views here.
def index(request):
    return render (request,'fitness/index.html',{})

def lista_ejercicios(request):
    ejercicios = Ejercicio.objects.prefetch_related('usuarios')
    return render(request,'fitness/lista_ejercicios.html',{'ejercicios_mostrar':ejercicios})
