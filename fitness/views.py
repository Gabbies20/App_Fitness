from django.shortcuts import render
from django.views.defaults import page_not_found
from .models import Ejercicio,Usuario,Perfil_de_Usuario,Entrenamiento,RutinaDiaria,Comentario,CategoriaEjercicio,HistorialEjercicio

# Create your views here.
def index(request):
    return render (request,'fitness/index.html',{})

#1.Vista que muestra todos los ejercicios y sus datos, incluidos los relcionados.
def lista_ejercicios(request):
    ejercicios = Ejercicio.objects.prefetch_related('usuarios')
    return render(request,'fitness/lista_ejercicios.html',{'ejercicios_mostrar':ejercicios})

#2.Vista que muestra la información de un usuario especifico, incluyendo su nombre, correo y enlace a su perfil de usuario.
def informacion_usuario(request):
    usuario = Usuario.objects.all()
    return render(request,'fitness/informacion_usuario.html',{'usuario_mostrar':usuario})

def perfil_usuario(request, id_usuario):
    perfil = Perfil_de_Usuario.objects.filter(usuario_id=id_usuario).first()
    return render(request, 'fitness/perfil_usuario.html', {'perfil_mostrar': perfil})

def entrenamiento_aerobico(reques):
    entrenamientos = Entrenamiento.objects.prefetch_related('ejercicios').filter(tipo='AER')
    return render(reques,'fitness/entrenamientos_aerobicos.html',{'entrenamientos_mostrar':entrenamientos})


def usuario_con_h(request):
    # Filtra las rutinas diarias de usuarios cuyos nombres comienzan con 'H'
    rutinas_diarias = RutinaDiaria.objects.filter(usuario__nombre__istartswith='H').select_related('usuario').prefetch_related('ejercicios')
    return render(request, 'fitness/rutina_diaria_usuario_con_H.html', {'rutinas_diarias': rutinas_diarias})


def comentarios_entrenamiento(request, entrenamiento_id):
    entrenamiento = Entrenamiento.objects.select_related('usuario').get(id=entrenamiento_id)
    comentarios = Comentario.objects.filter(entrenamiento=entrenamiento)
    
    return render(request, 'fitness/comentarios_entrenamiento.html', {'entrenamiento': entrenamiento, 'comentarios': comentarios})


def comentarios_fecha(request,anyo_comentario,mes_comentario):
    comentarios = Comentario.objects.select_related('usuario','entrenamiento')
    comentarios = comentarios.filter(fecha__year=anyo_comentario,fecha__month=mes_comentario)
    return render(request,'fitness/comentarios_fecha.html',{'comentarios_mostrar':comentarios})


def categoria_lisos(request):
    categoria = CategoriaEjercicio.objects.prefetch_related('ejercicios')
    categoria = categoria.filter(grupo_muscular_principal = 'Lisos')
    return render(request,'fitness/categoria_lisos.html',{'categoria_mostrar':categoria})


def lista_entrenamientos(request):
    entrenamiento = Entrenamiento.objects.select_related('usuario').prefetch_related('ejercicios').filter(tipo='HIT',duracion__gt=10000)
    return render(request, 'fitness/lista_entrenamientos.html',{'entrenamientos':entrenamiento})


def grupo_muscular(request, grupo_muscular):
    categories = CategoriaEjercicio.objects.filter(grupo_muscular_principal=grupo_muscular)
    
    context = {
        'grupo_muscular': grupo_muscular,
        'categories': categories,
    }
    
    return render(request, 'fitness/grupo_muscular.html', context)



def usuarios_sin_comentarios(request):
    # Obtén la lista de usuarios que no han realizado ningún comentario
    usuarios_sin_comentarios = Usuario.objects.exclude(comentario__isnull=False)
    
    contexto = {
        'usuarios_sin_comentarios': usuarios_sin_comentarios
    }
    
    return render(request, 'fitness/usuarios_sin_comentarios.html', contexto)


def historial_ejercicios_usuario(request, usuario_id):
    usuario = Usuario.objects.get(id=usuario_id)
    historial_ejercicios = HistorialEjercicio.objects.filter(usuario=usuario)

    contexto = {
        'usuario': usuario,
        'historial_ejercicios': historial_ejercicios
    }

    return render(request, 'fitness/historial_ejercicios_usuario.html', contexto)


#ERRORES:

def mi_error_404(request, exception=None):
    return render(request, 'errores/404.html', None, status=404)

def mi_error_400(request, exception=None):
    return render(request, 'errores/400.html', None, status=400)

def mi_error_403(request, exception=None):
    return render(request, 'errores/403.html', None, status=403)

def mi_error_500(request, exception=None):
    return render(request, 'errores/500.html', None, status=500)