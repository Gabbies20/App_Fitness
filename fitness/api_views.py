from django.http import JsonResponse
from django.shortcuts import get_object_or_404
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
    ejercicios = Ejercicio.objects.prefetch_related('usuarios','grupos_musculares')
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
            ejercicios = Ejercicio.objects.prefetch_related("usuarios", "grupos_musculares")
            ejercicios = ejercicios.filter(grupos_musculares__musculos__nombre__contains=texto)
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
            QSEjercicios = Ejercicio.objects.prefetch_related('usuarios','grupos_musculares')
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
        # Intenta guardar el ejercicio
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
def entrenamiento_obtener(request,entrenamiento_id):
    entrenamiento = Entrenamiento.objects.select_related('usuario').prefetch_related("ejercicios")
    entrenamiento = entrenamiento.get(id=entrenamiento_id)
    serializer = EntrenamientoMejoradoSerializer(entrenamiento)
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


@api_view(['GET'])
def usuario_list(request):
    usuarios = Usuario.objects.all()
    serializer =UsuarioSerializer(usuarios, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def entrenamiento_create(request): 
    print(request.data)
    entrenamientoCreateSerializer = EntrenamientoSerializerCreate(data=request.data)
    if entrenamientoCreateSerializer.is_valid():
        try:
            entrenamientoCreateSerializer.save()
            return Response("entrenamiento CREADO")
        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print(repr(error))
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        print(repr(entrenamientoCreateSerializer.errors))
        return Response(entrenamientoCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def entrenamiento_editar(request,entrenamiento_id):
    entrenamiento = Entrenamiento.objects.get(id=entrenamiento_id)
    entrenamientoCreateSerializer = EntrenamientoSerializerCreate(data=request.data,instance=entrenamiento)
    if entrenamientoCreateSerializer.is_valid():
        try:
            entrenamientoCreateSerializer.save()
            return Response("Entrenamiento EDITADO")
        except serializers.ValidationError as error:
            print(repr(error))
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print(repr(error))
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        print(repr(entrenamientoCreateSerializer.errors))
        return Response(entrenamientoCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PATCH'])
def entrenamiento_actualizar_descripcion(request,entrenamiento_id):
    entrenamiento = Entrenamiento.objects.get(id=entrenamiento_id)
    serializers = EntrenamientoSerializerActualizarDescripcion(data=request.data,instance=entrenamiento)
    if serializers.is_valid():
        try:
            serializers.save()
            return Response("entrenamiento EDITADO")
        except Exception as error:
            print(repr(error))
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def entrenamiento_eliminar(request,entrenamiento_id):
    entrenamiento = Entrenamiento.objects.get(id=entrenamiento_id)
    try:
        entrenamiento.delete()
        return Response("entrenamiento ELIMINADO")
    except Exception as error:
        return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


"""COMENTARIOS"""

@api_view(['GET'])
def comentario_list(request):
    comentarios = Comentario.objects.select_related('usuario','entrenamiento')
    serializer = ComentarioMejoradoSerializer(comentarios, many=True)
    return Response(serializer.data)

@api_view(['GET']) 
def comentario_obtener(request,comentario_id):
    comentario = Comentario.objects.select_related('usuario','entrenamiento')
    comentario = comentario.get(id=comentario_id)
    serializer = ComentarioMejoradoSerializer(comentario)
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
            
            #obtenemos los comentarios
            textoBusqueda = formulario.cleaned_data.get('textoBusqueda')
            fecha = formulario.cleaned_data.get('fecha')
            
            #Por cada filtro comprobamos si tiene un valor y lo añadimos a la QuerySet
            if texto:
                QSComentarios = QSComentarios.filter(Q(nombre__icontains=textoBusqueda))

            if(not fecha is None):
                QSComentarios = QSComentarios.filter(fecha__gte=fecha)
            
            comentarios = QSComentarios.all()
            serializer = ComentarioMejoradoSerializer(comentarios, many=True)
            return Response(serializer.data)
        else:
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['POST'])
def comentario_create(request):
    if(request.user.has_perm("fitness.add_comentario")):
        comentarioCreateSerializer = ComentarioSerializerCreate(data=request.data)
        if comentarioCreateSerializer.is_valid():
            try:
                comentarioCreateSerializer.save()
                return Response("comentario CREADO", status=status.HTTP_200_OK)
            except serializers.ValidationError as error:
                return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                print(repr(error))
                return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(comentarioCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("NO TIENE PERMISO", status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['PUT'])
def comentario_editar(request,comentario_id):
    comentario = Comentario.objects.get(id=comentario_id)
    comentarioCreateSerializer = ComentarioSerializerCreate(data=request.data,instance=comentario)
    if comentarioCreateSerializer.is_valid():
        try:
            comentarioCreateSerializer.save()
            return Response("comentario EDITADO")
        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(comentarioCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PATCH'])
def comentario_actualizar_nombre(request,comentario_id):
    comentario = Comentario.objects.get(id=comentario_id)
    serializers = ComentarioSerializerActualizarTexto(data=request.data,instance=comentario)
    if serializers.is_valid():
        try:
            serializers.save()
            return Response("comentario EDITADO")
        except Exception as error:
            print(repr(error))
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def comentario_eliminar(request,comentario_id):
    comentario = Comentario.objects.get(id=comentario_id)
    try:
        comentario.delete()
        return Response("comentario ELIMINADO")
    except Exception as error:
        return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)





# api_view(['GET'])
# def ejercicios_entrenamiento(request,entrenamiento_id):
#     entrenamiento = Entrenamiento.objects.get(id=entrenamiento_id)
#     ejercicios = entrenamiento.objects.all()
#     #Los serializamos:
#     serializer = EjercicioMejoradoSerializer(ejercicios,many=True)
#     return (serializer.data)
    



#VISTAS DE LAS FUNCIONALIDADES DE MIS COMPAÑEROS:

@api_view(['GET'])
def ejercicios_entrenamiento(request, entrenamiento_id):
    entrenamiento = Entrenamiento.objects.get(id=entrenamiento_id)
    ejercicios = entrenamiento.ejercicios.all()
    serializer = EjercicioMejoradoSerializer(ejercicios, many=True)
    return Response(serializer.data)

    
@api_view(['GET'])
def grupos_musculares_list(request):
    grupos_musculares = GrupoMuscular.objects.all()
    serializer = GrupoMuscularSerializer(grupos_musculares,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def obtener_historial(request,usuario_id):
    if(request.user.has_perm("fitness.view_historialejercicio")):
        usuario = Usuario.objects.get(id=usuario_id)
        historial_personalizado = HistorialEjercicio.objects.filter(usuario=usuario)
        serializer = HistorialEjercicioSerializer(historial_personalizado, many=True)
        return Response(serializer.data)
    else:
        return Response("NO TIENE PERMISO", status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def obtener_perfil_usuario(request,usuario_id):
    usuario = Usuario.objects.get(id=usuario_id)
    perfil = Perfil_de_Usuario.objects.filter(usuario=usuario)
    serializer = PerfilUsuarioSerializer(perfil, many=True)
    return Response(serializer.data)
    
@api_view(['GET'])
def perfil_list(request):
    perfiles = Perfil_de_Usuario.objects.all()
    serializer = PerfilUsuarioSerializer(perfiles, many=True)
    return Response(serializer.data)


@api_view(['GET']) 
def ejercicio_obtener(request,ejercicio_id):
    ejercicio = Ejercicio.objects.prefetch_related("usuarios")
    ejercicio = ejercicio.get(id=ejercicio_id)
    serializer = EjercicioMejoradoSerializer(ejercicio)
    return Response(serializer.data)

@api_view(['GET'])
def obtener_usuario(request,usuario_id):
    usuario = Usuario.objects.get(id=usuario_id)
    serializer = UsuarioSerializer(usuario)
    return Response(serializer.data)


@api_view(['PUT'])
def perfil_editar(request,usuario_id):
    perfil = Perfil_de_Usuario.objects.get(id=usuario_id)
    perfilCreateSerializer = PerfilUsuarioActualizarSerializer(data=request.data,instance=perfil)
    if perfilCreateSerializer.is_valid():
        try:
            perfilCreateSerializer.save()
            return Response("Libro EDITADO")
        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(perfilCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def ejercicio_buscar_musculos(request):
    formulario = BusquedaEjercicioForm(request.query_params)
    if(formulario.is_valid()):
        texto = formulario.data.get('textoBusqueda')
        ejercicios = Ejercicio.objects.prefetch_related("usuarios","grupos_musculares")
        ejercicios = ejercicios.filter(grupos_musculares__musculos__nombre__icontains=texto).distinct()
        serializer = EjercicioMejoradoSerializer(ejercicios, many=True)
        return Response(serializer.data)
    else:
        return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)










































#REGISTRO:
from rest_framework import generics
from rest_framework.permissions import AllowAny


class registrar_usuario(generics.CreateAPIView):
    serializer_class = UsuarioSerializerRegistro
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializers = UsuarioSerializerRegistro(data=request.data)
        if serializers.is_valid():
            try:
                rol = request.data.get('rol')
                user = Usuario.objects.create_user(
                        username = serializers.data.get("username"), 
                        email = serializers.data.get("email"), 
                        password = serializers.data.get("password1"),
                        rol = rol,
                        )
                if(rol == Usuario.CLIENTE):
                    grupo = Group.objects.get(name='Clientes') 
                    grupo.user_set.add(user)
                    cliente = Cliente.objects.create( usuario = user)
                    cliente.save()
                elif(rol == Usuario.ENTRENADOR):
                    grupo = Group.objects.get(name='Entrenadores') 
                    grupo.user_set.add(user)
                    entrenador = Entrenador.objects.create(usuario = user)
                    entrenador.save()
                usuarioSerializado = UsuarioSerializer(user)
                return Response(usuarioSerializado.data)
            except Exception as error:
                print(repr(error))
                return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

from oauth2_provider.models import AccessToken     
@api_view(['GET'])
def obtener_usuario_token(request,token):
    ModeloToken = AccessToken.objects.get(token=token)
    usuario = Usuario.objects.get(id=ModeloToken.user_id)
    serializer = UsuarioSerializer(usuario)
    return Response(serializer.data)


@api_view(['GET'])
def obtener_calorias_usuario(request):
    if(request.user.has_perm("fitness.view_historialejercicio")):
        sumatorio = HistorialEjercicio.objects
        return Response(sumatorio)
    else:
        return Response("NO TIENE PERMISO", status=status.HTTP_401_UNAUTHORIZED)