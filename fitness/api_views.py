from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework import status
from .forms import *
from django.db.models import Q,Prefetch
from django.contrib.auth.models import Group
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated


@api_view(['GET'])
def ejercicio_list(request):
    
    ejercicios = Ejercicio.objects.all()
    serializer = EjercicioMejoradoSerializer(ejercicios, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def ejercicio_buscar(request):
    #if(request.user.has_perm("biblioteca.view_libro")):
        formulario = BusquedaEjercicioForm(request.query_params)
        if(formulario.is_valid()):
            texto = formulario.data.get('textoBusqueda')
            ejercicios = Ejercicio.objects.prefetch_related("usuarios")
            ejercicios = ejercicios.filter(Q(nombre__contains=texto) | Q(descripcion__contains=texto)).all()
            serializer = EjercicioMejoradoSerializer(ejercicios, many=True)
            return Response(serializer.data)
        else:
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
    #else:
     #   return Response({"Sin permisos"}, status=status.HTTP_400_BAD_REQUEST)
     
     
@api_view(['GET'])
def ejercicio_buscar_avanzado(request):
    if(len(request.query_params) > 0):
        formulario = BusquedaAvanzadaEjercicioForm(request.query_params)
        if formulario.is_valid():
            texto = formulario.cleaned_data.get('textoBusqueda')
            QSEjercicios = Ejercicio.objects.prefetch_related('usuarios')
            #Obtenemos los filtros:
            textoBusqueda = formulario.cleaned_data.get('textoBusqueda')
            descripcion = formulario.cleaned_data.get('descripcion')
            
            #Por cada filtro comprobamos si tiene un valor y lo añadimos a la qryset:
            if(textoBusqueda != ''):
                QSEjercicios = QSEjercicios.filter(Q(nombre__contains=textoBusqueda) | Q(descripcion__contains=textoBusqueda))
            
            if(descripcion != ''):
                QSEjercicios = QSEjercicios.filter(descripcion__contains=descripcion)

            
            ejercicios = QSEjercicios.all()
            serializer = EjercicioMejoradoSerializer(ejercicios, many=True)
            return Response(serializer.data)
        else:
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)

"""
SUSCRIPCION    
"""
@api_view(['GET'])
def entrenamiento_list(request):
    entrenamientos = Entrenamiento.objects.all()
    #many=True -> para indicar que serializamos muchos valores.
    serializer = EntrenamientoMejoradoSerializer(entrenamientos, many=True)
    #serializer.data es un atributo que contiene los datos serializados.
    return Response(serializer.data)