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



"""EJERCICIOS"""
@api_view(['GET'])
def ejercicio_list(request):
    ejercicios = Ejercicio.objects.all()
    serializer = EjercicioMejoradoSerializer(ejercicios, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def usuarios_list(request):
    usuarios = Usuario.objects.all()
    serializer = UsuarioSerializer(usuarios, many=True)
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



@api_view(['POST'])
def ejercicio_create(request):
    # Imprime los datos recibidos en la solicitud para depurar
    print(request.data)
    
    # Intenta crear un nuevo libro utilizando el serializador
    ejercicio_create_serializer = EjercicioSerializerCreate(data=request.data)
    
    # Verifica si los datos son válidos según el serializador
    if ejercicio_create_serializer.is_valid():
        # Intenta guardar el libro
        try:
            ejercicio_create_serializer.save()
            # Si se guarda correctamente, devuelve una respuesta exitosa
            return Response("EJERCICIO CREADO", status=status.HTTP_200_OK)
        except serializers.ValidationError as error:
            # Si hay un error de validación, devuelve los detalles del error
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            # Si hay un error inesperado, imprime el error y devuelve un error interno del servidor
            print(repr(error))
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        # Si los datos no son válidos según el serializador, devuelve los errores de validación
        return Response(ejercicio_create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET']) 
def ejercicio_obtener(request,ejercicio_id):
    ejercicio = Ejercicio.objects.prefetch_related("usuarios")
    ejercicio = ejercicio.get(id=ejercicio_id)
    serializer = EjercicioMejoradoSerializer(ejercicio)
    return Response(serializer.data)

@api_view(['PUT'])
def ejercicio_editar(request, ejercicio_id):
    ejercicio = Ejercicio.objects.get(id=ejercicio_id)
    ejercicioCreateSerializer = EjercicioSerializerCreate(data=request.data,instance=ejercicio)
    if ejercicioCreateSerializer.is_valid():
        try:
            ejercicioCreateSerializer.save()
            return Response('ejercicio EDITADO')
        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(ejercicioCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def ejercicio_actualizar_nombre(request,ejercicio_id):
    ejercicio = Ejercicio.objects.get(id=ejercicio_id)
    serializers = EjercicioSerializerActualizarNombre(data=request.data,instance=ejercicio)
    if serializers.is_valid():
        try:
            serializers.save()
            return Response("Ejercicio EDITADO")
        except Exception as error:
            print(repr(error))
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def ejercicio_eliminar(request,ejercicio_id):

    ejercicio = Ejercicio.objects.get(id=ejercicio_id)
    try:
        ejercicio.delete()
        return Response("Ejercicio ELIMINADO")
    except Exception as error:
        return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)














"""
ENTRENAMIENTOS:    
"""
@api_view(['GET'])
def entrenamiento_list(request):
    entrenamientos = Entrenamiento.objects.all()
    #many=True -> para indicar que serializamos muchos valores.
    serializer = EntrenamientoMejoradoSerializer(entrenamientos, many=True)
    #serializer.data es un atributo que contiene los datos serializados.
    return Response(serializer.data)

@api_view(['GET'])
def entrenamiento_buscar(request):
    formulario = BusquedaEntrenamientoForm(request.query_params)
    if(formulario.is_valid()):
        texto = formulario.data.get('textoBusqueda')
        entrenamientos = Entrenamiento.objects.prefetch_related('ejercicios')
        entrenamientos = entrenamientos.filter(Q(nombre__contains=texto) | Q(descripcion__contains=texto)).all()
        serializer = EntrenamientoMejoradoSerializer(entrenamientos,many=True)
        return Response(serializer.data)
    else:
        return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def entrenamiento_buscar_avanzado(request):

    if(len(request.query_params) > 0):
        formulario = BusquedaAvanzadaEntrenamientoForm(request.query_params)
        if formulario.is_valid():
            texto = formulario.cleaned_data.get('textoBusqueda')
            QSEntrenamientos = Entrenamiento.objects.select_related("usuario").prefetch_related("ejercicios")
            
            #obtenemos los filtros
            textoBusqueda = formulario.cleaned_data.get('textoBusqueda')
            tipos = formulario.cleaned_data.get('tipos')
            nombre = formulario.cleaned_data.get('nombre')
            descripcion = formulario.cleaned_data.get('descripcion')
            duracion = formulario.cleaned_data.get('duracion')
            
            #Por cada filtro comprobamos si tiene un valor y lo añadimos a la QuerySet
            if textoBusqueda:
                QSEntrenamientos = QSEntrenamientos.filter(Q(nombre__icontains=textoBusqueda) | Q(descripcion__icontains=textoBusqueda))

            if nombre:
                QSEntrenamientos = QSEntrenamientos.filter(nombre__icontains=nombre)
                
            if descripcion:
                QSEntrenamientos = QSEntrenamientos.filter(descripcion__icontains=descripcion)
                
            if duracion:
                QSEntrenamientos = QSEntrenamientos.filter(duracion__icontains=duracion)

            # Si hay distintos tipos, iteramos por ellos, creamos la queryOR y le aplicamos el filtro
            if len(tipos) > 0:
                filtroOR = Q(tipo=tipos[0])
                for tipo in tipos[1:]:
                    mensaje_busqueda += " o "+tipos[1]
                    filtroOR |= Q(tipo=tipo)
                QSEntrenamientos = QSEntrenamientos.filter(filtroOR)
            libros = QSEntrenamientos.all()
            serializer = EntrenamientoMejoradoSerializer(libros, many=True)
            return Response(serializer.data)
        else:
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)
    

"""COMENTARIOS"""
@api_view(['GET'])
def comentario_list(request):
    ejercicios = Comentario.objects.all()
    serializer = ComentarioMejoradoSerializer(ejercicios, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def comentario_buscar(request):
    #if(request.user.has_perm("biblioteca.view_libro")):
        formulario = BusquedaEjercicioForm(request.query_params)
        if(formulario.is_valid()):
            texto = formulario.data.get('textoBusqueda')
            comentarios = Comentario.objects.select_related('usuario','entrenamiento')
            comentarios = comentarios.filter(Q(texto__contains=texto)).all()
            serializer = ComentarioMejoradoSerializer(comentarios, many=True)
            return Response(serializer.data)
        else:
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
    #else:
     #   return Response({"Sin permisos"}, status=status.HTTP_400_BAD_REQUEST)
     


@api_view(['GET'])
def comentario_buscar_avanzado(request):

    if(len(request.query_params) > 0):
        formulario = BusquedaAvanzadaComentarioForm(request.query_params)
        if formulario.is_valid():
            texto = formulario.cleaned_data.get('textoBusqueda')
            QSComentarios = Comentario.objects.select_related('usuario','entrenamiento')
            
            #obtenemos los filtros
            textoBusqueda = formulario.cleaned_data.get('textoBusqueda')
            fecha = formulario.cleaned_data.get('fecha')
            
            #Por cada filtro comprobamos si tiene un valor y lo añadimos a la QuerySet
            if texto:
                QSComentarios = QSComentarios.filter(Q(nombre__icontains=textoBusqueda))

            if(not fecha is None):
                QSComentarios = QSComentarios.filter(fecha__gte=fecha)
            
            libros = QSComentarios.all()
            serializer = ComentarioMejoradoSerializer(libros, many=True)
            return Response(serializer.data)
        else:
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)