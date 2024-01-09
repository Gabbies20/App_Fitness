from django.shortcuts import render,redirect
from django.views.defaults import page_not_found

from django.contrib import messages
from .models import Ejercicio,Usuario,Perfil_de_Usuario,Entrenamiento,RutinaDiaria,Comentario,CategoriaEjercicio,HistorialEjercicio,Voto,Suscripcion
from django.db.models import Q,F
from .forms import *
from datetime import datetime
from django.contrib.auth.models import Group
from django.contrib.auth import login



# Create your views here.
def index(request):
    if(not "fecha_inicio" in request.session):
        request.session["fecha_inicio"] = datetime.now().strftime('%d/%m/%Y %H:%M')
    return render(request, 'fitness/index.html')

#1.Vista que muestra todos los ejercicios y sus datos, incluidos los relcionados.
def lista_ejercicios(request):
    ejercicios = Ejercicio.objects.prefetch_related('usuarios')
    return render(request,'fitness/ejercicio/lista_ejercicios.html',{'ejercicios_mostrar':ejercicios})

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


    """
    EXAMEN:
    
    """
#El último voto que se realizó en un modelo principal en concreto, y mostrar el comentario, la votación e información del usuario o cliente que lo realizó.
def ultimo_voto(request,id_ejercicio):
    usuario = Voto.objects.select_related('u_creador','ejercicio').filter(ejercicio=id_ejercicio).order_by('-fecha')[:1].get()
    return render(request,'fitness/url1.html',{'usuario_mostrar':usuario})


#Todos los ejercicios que tengan votos con una puntuación numérica igual a 3 y que realizó un usuario o cliente en concreto. 
def puntuacion_tres(request, id_usuario):
    usuario = Usuario.objects.get(id=id_usuario)
    votos = Voto.objects.filter(puntuacion=3, u_creador=usuario)
    ejercicios = Ejercicio.objects.filter(voto__in=votos)

    return render(request, 'fitness/url2.html', {'ejercicios_mostrar': ejercicios})
    

#Todos los usuarios o clientes que no han votado nunca y mostrar información sobre estos usuarios y clientes al completo..
def usuarios_sin_votos(request):
    # Obtén una lista de usuarios o clientes que no han votado nunca
    usuarios_sin_votos = Usuario.objects.exclude(voto__isnull=False)

    return render(request, 'fitness/url3.html', {'usuarios_sin_votos': usuarios_sin_votos})



#Obtener las cuentas bancarias que sean de la Caixa o de Unicaja y que el propietario tenga un nombre que contenga un texto en concreto, por ejemplo “Juan”.

def cuentas_bancarias(request,texto):
    cuentas = Suscripcion.objects.select_related('titular')
    cuentas = cuentas.filter(Q(banco='CAI') | Q(banco='Uni'), titular__nombre__icontains=texto)
    return render(request, 'fitness/url4.html', {'cuenta_mostrar': cuentas})


#Obtener todos los modelos principales que tengan una media de votaciones mayor del 2,5.

"""
    CRUD EJERCICIO:
"""


#EJERCICIO MOSTRAR:
def ejercicio_mostrar(request,ejercicio_id):
    ejercicio = Ejercicio.objects.prefetch_related('usuarios','usuarios_votos')
    ejercicio = ejercicio.get(id=ejercicio_id)
    return render (request, 'fitness/ejercicio/ejercicio_mostrar.html',{'ejercicio':ejercicio})




#CREAR UN EJERCICIO:
def ejercicio_crear(request):
   # formulario = EjercicioModelForm()
    #return render(request, 'fitness/create.html',{'formulario':formulario})
    
    
    #Por defecto la primera vez que entra esta vacio.
    #Esto es una variable 
    datosFormulario = None
    
    #SI le escribimos datos ya entra a este if, ya esta usando el metodo POST
    if request.method == 'POST':
        datosFormulario = request.POST
    
    
    #Sigue vacio
    formulario = EjercicioModelForm(datosFormulario)
    
    
    #Ahora ya lo llenado es POST O GET, COMO YA HA PULSADO EL USUARIO ENVIAR,el ḿetodo es POSt ya ya entra aquí.
    if (request.method == 'POST'):
        #Llamamaos a la función que creará el libro.
        ejercicio_creado = crear_ejercicio_modelo(formulario)
        if(ejercicio_creado):
            messages.success(request, 'Se ha creado el ejercicio'+formulario.cleaned_data.get('nombre')+" correctamente.")
            return redirect("lista_ejercicios")
    return render(request, 'fitness/ejercicio/create.html',{"formulario":formulario})

def crear_ejercicio_modelo(formulario):
    ejercicio_creado = False
    
    #Compreubo si es valido y lo guarda.
    if formulario.is_valid():
        try:
            formulario.save()
            ejercicio_creado = True
        except:
            pass
    return ejercicio_creado


#Vista para la búsqueda:
def ejercicio_buscar(request):
    formulario = BusquedaEjercicioForm(request.GET)
    
    if(formulario.is_valid()):
        texto = formulario.cleaned_data.get('textoBusqueda')
        ejercicios = Ejercicio.objects.prefetch_related('usuarios_votos')
        ejercicios = ejercicios.filter(Q(nombre__contains=texto) | Q(descripcion__contains=texto)).all()
        return render (request,'fitness/ejercicio/lista_busqueda.html',{'ejercicios_mostrar':ejercicios,'texto_busqueda':texto})
    if('HTPP_REFERER' in request.META):
        return redirect(request.META['HTTP_REFERER'])
    else:
        print(formulario.error)
        return redirect('index')
    

#VISTA BÚSQUEDA AVANZADA:
def ejercicio_busqueda_avanzada(request):
    
    #Vamos a verificar si tenemos datos o no, para procesar el formulario y validarlo.
    if(len(request.GET)> 0):
        formulario = BusquedaAvanzadaEjercicioForm(request.GET)
        if formulario.is_valid():
            print('Es valido')
            
            mensaje_busqueda = 'Se ha buscado por los siguientes valores: \n'
            
            QSEjercicios = Ejercicio.objects.prefetch_related('usuarios_votos')
            
            #OBTENEMOS LOS FILTROS:
            textoBusqueda = formulario.cleaned_data['textoBusqueda']
            descripcion = formulario.cleaned_data['descripcion']
            #usuarios = formulario.cleaned_data.get['usuarios', []]
            
            #POR CADA FILTRO COMPROBAMOS SI TIENE UN VALOR Y LO AÑADIMOS A LA QUERYSET:
            if textoBusqueda:
                QSEjercicios = QSEjercicios.filter(Q(nombre__contains=textoBusqueda) | Q(descripcion__contains=textoBusqueda))
                mensaje_busqueda +=" Nombre o contenido que contengan la palabra "+textoBusqueda+"\n"
            if descripcion:
                QSEjercicios = QSEjercicios.filter(Q(nombre__contains=descripcion) | Q(descripcion__contains=descripcion))
                mensaje_busqueda +=" Nombre o contenido que contengan la palabra "+descripcion+"\n"
                
            ejercicios = QSEjercicios.all()
            
            print('Estamos aqui')
            
            return render(request,'fitness/ejercicio/lista_busqueda.html',{'ejercicios_mostrar':ejercicios,'texto_busqueda':mensaje_busqueda})
    else:
        #En el caso de que procesa desde una URL y no tenga datos, mostramos el formulario correspondiente.
        formulario = BusquedaAvanzadaEjercicioForm(None)
        print('No hay nada')
    return render(request,'fitness/ejercicio/busqueda_avanzada.html',{'formulario':formulario})



#VISTA EDITAR-EJERCICIO:
def ejercicio_editar(request, ejercicio_id):
    ejercicio = Ejercicio.objects.get(id=ejercicio_id)
    
    datosFormulario = None
    
    if(request.method == 'POST'):
        datosFormulario = request.POST
        
    formulario = EjercicioModelForm(datosFormulario,instance= ejercicio)
    
    if(request.method=='POST'):
        if(formulario.is_valid()):
            formulario.save()
            try:
                formulario.save()
                messages.success(request, 'Se ha editado el ejercicio'+formulario.cleaned_data.get('nombre')+" correctamente")
                return redirect('lista_ejercicios')
            except Exception as error:
                print(error)
    return render(request,'fitness/ejercicio/actualizar.html',{'formulario':formulario,'ejercicio':ejercicio})


#VISTA ELIMINAR-EJERCICIO:
def ejercicio_eliminar(request,ejercicio_id):
    ejercicio = Ejercicio.objects.get(id=ejercicio_id)
    try:
        ejercicio.delete()
        messages.success(request, "Se ha elimnado el ejercicio "+ejercicio.nombre+" correctamente")
    except:
        pass
    return redirect ('lista_ejercicios')
    return entrenamiento

def entrenamiento_mostrar(request,entrenamiento_id):
    entrenamiento = Entrenamiento.objects.select_related('usuario').prefetch_related('ejercicios')
    entrenamiento = entrenamiento.get(id=entrenamiento_id)
    return render(request,'fitness/entrenamiento/entrenamiento_mostrar.html',{'entrenamiento':entrenamiento})

def entrenamiento_create(request):
    
    datosFormulario = None
    
    if(request.method=='POST'):
        datosFormulario = request.POST
    
    formulario = EntrenamientoForm(datosFormulario)
    if(request.method=='POST'):
        if(formulario.is_valid()):
            try:
                #Gurada el entrenamiento en la base de datos.
                formulario.save()
                #print(formulario)
                return redirect('lista_entrenamientos')
            except Exception as error:
                print(error)
    else:
        print(formulario.errors)
    return render(request,'fitness/entrenamiento/create.html',{'formulario':formulario})


def lista_entrenamientos(request):
    entrenamientos = Entrenamiento.objects.select_related('usuario').prefetch_related('ejercicios')
    return render(request,'fitness/entrenamiento/lista_entrenamientos.html',{'mostrar_entrenamientos':entrenamientos})

#Vista de buscar:
def entrenamiento_buscar(request,):
    formulario = BusquedaEntrenamientoForm(request.GET)
    
    if(formulario.is_valid()):
        texto = formulario.cleaned_data.get('textoBusqueda')
        entrenamientos = Entrenamiento.objects.select_related('usuario').prefetch_related('ejercicios')
        entrenamientos = entrenamientos.filter(Q(nombre__contains=texto) | Q(descripcion__contains=texto)).all()
        return render (request,'fitness/entrenamiento/lista_busqueda.html',{'entrenamientos_mostrar':entrenamientos,'texto_busqueda':texto})
    if('HTPP_REFERER' in request.META):
        return redirect(request.META['HTTP_REFERER'])
    else:
        print(formulario.error)
        return redirect('index')

#VISTA BUESQUEDA AVANZADA - ENTRENAMIENTO:
def entrenamiento_buscar_avanzado(request):
    if len(request.GET) > 0:
        formulario = BusquedaAvanzadaEntrenamientoForm(request.GET)
        if formulario.is_valid():
            mensaje_busqueda = "Se ha buscado por los siguientes valores:\n"
            
            QSEntrenamientos = Entrenamiento.objects.select_related("usuario").prefetch_related("ejercicios")
            
            # Obtención de los filtros
            textoBusqueda = formulario.cleaned_data.get('textoBusqueda')
            tipos = formulario.cleaned_data.get('tipos')
            duracion = formulario.cleaned_data.get('duracion')
            
            # Por cada filtro, comprobamos si tiene un valor y lo añadimos a la QuerySet
            if textoBusqueda:
                QSEntrenamientos = QSEntrenamientos.filter(Q(nombre__contains=textoBusqueda) | Q(descripcion__contains=textoBusqueda))
                mensaje_busqueda += f"Nombre o contenido que contengan la palabra {textoBusqueda}\n"
            
            if tipos:
                mensaje_busqueda += f"El tipo sea {tipos[0]}"
                filtroOR = Q(tipo=tipos[0])
                for tipo in tipos[1:]:
                    mensaje_busqueda += f" o {tipo}"
                    filtroOR |= Q(tipo=tipo)
                mensaje_busqueda += "\n"
                QSEntrenamientos = QSEntrenamientos.filter(filtroOR)
            
            if duracion:
                QSEntrenamientos = QSEntrenamientos.filter(duracion=duracion)
                mensaje_busqueda += f"Duración sea igual a {duracion} minutos\n"
            
            entrenamientos = QSEntrenamientos.all()

            return render(request, 'fitness/entrenamiento/lista_busqueda.html',
                          {"entrenamientos_mostrar": entrenamientos,
                           "texto_busqueda": mensaje_busqueda})
    else:
        formulario = BusquedaAvanzadaEntrenamientoForm(None)
    return render(request, 'fitness/entrenamiento/busqueda_avanzada.html', {"formulario": formulario})

#VISTA DE EDITAR - ENTRENAMIENTO:
def entrenamiento_editar(request,entrenamiento_id):
    entrenamiento = Entrenamiento.objects.get(id=entrenamiento_id)
    
    datosFormulario = None
    if(request.method=='POST'):
        datosFormulario = request.POST
    
    formulario = EntrenamientoForm(datosFormulario,instance=entrenamiento)
    if(request.method=='POST'):
        if formulario.is_valid():
            formulario.save()
            try:
                formulario.save()
                return redirect('lista_entrenamientos')
            except Exception as e:
                pass
    return render(request,'fitness/entrenamiento/actualizar.html',{'formulario':formulario,'entrenamiento':entrenamiento})
        
        
def entrenamiento_eliminar(request,entrenamiento_id):
    entrenamiento = Entrenamiento.objects.get(id=entrenamiento_id)
    try:
        entrenamiento.delete()
    except:
        pass
    return redirect ('lista_entrenamientos')


    """CRUD PLAN DE ENTRENAMIENTO
    """

def lista_plan(request):
    plan = PlanEntrenamiento.objects.select_related('usuario').prefetch_related('entrenamientos')
    return render(request,'fitness/plan/lista_plan.html',{'mostrar_planes':plan})
    
def mostrar_plan(request, plan_id):
    plan = PlanEntrenamiento.objects.select_related('usuario').prefetch_related('entrenamientos')
    plan = plan.get(id=plan_id)
    return render(request,'fitness/plan/mostrar_plan.html',{'plan':plan})

def plan_create(request):
    datosFormulario = None
    if request.method=='POST':
        datosFormulario = request.POST
    formulario = PlanEntrenamientoModelForm(datosFormulario)
    if(request.method=='POST'):
        if formulario.is_valid():
            try:
                #Guarda el libro en la base de datos:
                formulario.save()
                return redirect('lista_plan')
            except Exception as error:
                print(error)
    return render (request,'fitness/plan/create.html',{'formulario':formulario})
                
def plan_buscar(request):
    formulario = BusquedaPlanForm(request.GET)
    
    if formulario.is_valid():
        texto = formulario.cleaned_data.get('textoBusqueda')
        plan = PlanEntrenamiento.objects.select_related('usuario').prefetch_related('entrenamientos')
        plan = plan.filter(Q(nombre__contains=texto) | Q(descripcion__contains=texto)).all()
        return render(request,'fitness/plan/lista_busqueda.html',{'planes_mostrar':plan,'texto_busqueda':texto})  
    if('HTPP_REFERER' in request.META):
        return redirect(request.META['HTTP_REFERER'])
    else:
        return redirect('index')
    
def plan_busqueda_avanzada(request):
    
    if(len(request.GET)>0):
        formulario = BusquedaAvanzadaPlanForm(request.GET)
        if formulario.is_valid():
            
            mensaje_busqueda = 'Se ha buscado por los siguientes valores:  \n'
            
            QSPlanes = PlanEntrenamiento.objects.select_related('usuario').prefetch_related('entrenamientos')
            
            #Obtenemos los filtros:
            texto_busqueda = formulario.cleaned_data.get('texto_busqueda')
            descripcion = formulario.cleaned_data.get('descripcion')
            fecha_desde = formulario.cleaned_data.get('fecha_desde')
            fecha_hasta = formulario.cleaned_data.get('fecha_hasta')
            
            
            #Por cada filtro comprobamos si tienen un valor y lo añadimos a la QuerySet:
            if(texto_busqueda!=0):
                QSPlanes = QSPlanes.filter(Q(nombre__contains=texto_busqueda) | Q(descripcion__contains=texto_busqueda))
                mensaje_busqueda +=" Nombre o contenido que contengan la palabra "+texto_busqueda+"\n"
                
    
            
            #Comprobamos fechas #Obtenemos los libros con fecha publicacion mayor a la fecha desde
            if(not fecha_desde is None):
                mensaje_busqueda +=" La fecha sea mayor a "+datetime.strftime(fecha_desde,'%d-%m-%Y')+"\n"
                QSPlanes = QSPlanes.filter(fecha_inicio__gte=fecha_desde)
            
             #Obtenemos los libros con fecha publicacion menor a la fecha desde
            if(not fecha_hasta is None):
                mensaje_busqueda +=" La fecha sea menor a "+datetime.strftime(fecha_hasta,'%d-%m-%Y')+"\n"
                QSPlanes = QSPlanes.filter(fecha_fin__lte=fecha_hasta)
            
            planes = QSPlanes.all()
           
            
            
            return render(request,'fitness/plan/lista_busqueda.html',{'planes_mostrar':planes,'texto_busqueda':mensaje_busqueda})
    else:
        formulario =BusquedaAvanzadaPlanForm(None)
    return render(request,'fitness/plan/busqueda_avanzada.html',{'formulario':formulario})

def plan_editar(request,plan_id):
    plan = PlanEntrenamiento.objects.get(id=plan_id)
    
    datosFormulario = None
    if(request.method=='POST'):
        datosFormulario = request.POST
    
    formulario = PlanEntrenamientoModelForm(datosFormulario,instance=plan)
    if(request.method=='POST'):
        if formulario.is_valid():
            formulario.save()
            try:
                formulario.save()
                return redirect('lista_plan')
            except Exception as e:
                pass
    return render(request,'fitness/plan/actualizar.html',{'formulario':formulario,'plan':plan})
        

def plan_eliminar(request,plan_id):
    plan = PlanEntrenamiento.objects.get(id=plan_id)
    try:
        plan.delete()
    except:
        pass
    return redirect ('lista_plan')




""" CRUD RUTINA DIARIA"""

def lista_rutina(request):
    rutina = RutinaDiaria.objects.select_related('usuario').prefetch_related('ejercicios')
    return render(request,'fitness/rutina/lista_rutina.html',{'mostrar_rutinas':rutina})
    
def mostrar_rutina(request, rutina_id):
    rutina = RutinaDiaria.objects.select_related('usuario').prefetch_related('ejercicios')
    rutina = rutina.get(id=rutina_id)
    return render(request,'fitness/rutina/mostrar_rutina.html',{'rutina':rutina})

#Incluir permiso
def rutina_create(request):
    datosFormulario = None
    if request.method=='POST':
        datosFormulario = request.POST
    formulario = RutinaModelForm(datosFormulario,initial={"usuario":request.user})
    if(request.method=='POST'):
        if formulario.is_valid():
            try:
                #Guarda el libro en la base de datos:
                formulario.save()
                
                #Si no usamos campo oculto
                '''rutina = RutinaDiaria.objects.create(
                    usuario = request.user,
                    fecha = formulario.cleaned_data.get("fecha"),
                    descripcion = formulario.cleaned_data.get("descripcion"),
                    duracion = formulario.cleaned_data.get("duracion"),
                    ejercicios = formulario.cleaned_data.get("ejercicios"),
                )
                rutina.save()'''
                return redirect('lista_rutina')
            except Exception as error:
                print(error)
    return render (request,'fitness/rutina/create.html',{'formulario':formulario})
                
def rutina_buscar(request):
    formulario = BusquedaRutinaForm(request.GET)
    
    if formulario.is_valid():
        texto = formulario.cleaned_data.get('textoBusqueda')
        rutinas = RutinaDiaria.objects.select_related('usuario').prefetch_related('ejercicios')
        rutinas = rutinas.filter(descripcion__contains=texto).all()

        return render(request, 'fitness/rutina/lista_busqueda.html', {'rutinas_mostrar': rutinas, 'texto_busqueda': texto})

    if 'HTPP_REFERER' in request.META:
        return redirect(request.META['HTTP_REFERER'])
    else:
        return redirect('index')

    
def rutina_busqueda_avanzada(request):
    
    if len(request.GET) > 0:
        formulario = BusquedaAvanzadaRutinaForm(request.GET)
        if formulario.is_valid():
            
            mensaje_busqueda = 'Se ha buscado por los siguientes valores:\n'
            
            QSRutinas = RutinaDiaria.objects.select_related('usuario').prefetch_related('ejercicios')
            
            # Obtenemos los filtros:
            texto_busqueda = formulario.cleaned_data.get('texto_busqueda')
            fecha = formulario.cleaned_data.get('fecha')
            
            # Por cada filtro comprobamos si tienen un valor y lo añadimos a la QuerySet:
            if texto_busqueda != 0:
                QSRutinas = QSRutinas.filter(Q(descripcion__contains=texto_busqueda))
                mensaje_busqueda += f" Nombre o contenido que contengan la palabra {texto_busqueda}\n"
            
    
            if fecha:
                fecha_limite = datetime.datetime(2023, 1, 1).date()
                mensaje_busqueda += f" La fecha sea mayor a {datetime.strftime(fecha, '%d-%m-%Y')}\n"
                QSRutinas = QSRutinas.filter(fecha__gte=fecha_limite)

            rutinas = QSRutinas.all()
            
            return render(request, 'fitness/rutina/lista_busqueda.html', {'rutinas_mostrar': rutinas, 'texto_busqueda': mensaje_busqueda})
    else:
        formulario = BusquedaAvanzadaRutinaForm(None)
    return render(request, 'fitness/rutina/busqueda_avanzada.html', {'formulario': formulario})


def rutina_editar(request,rutina_id):
    rutina = RutinaDiaria.objects.get(id=rutina_id)
    
    datosFormulario = None
    if(request.method=='POST'):
        datosFormulario = request.POST
    
    formulario = RutinaModelForm(datosFormulario,instance=rutina)
    if(request.method=='POST'):
        if formulario.is_valid():
            formulario.save()
            try:
                formulario.save()
                return redirect('lista_rutina')
            except Exception as e:
                pass
    return render(request,'fitness/rutina/actualizar.html',{'formulario':formulario,'rutina':rutina})
        

def rutina_eliminar(request,rutina_id):
    rutina = RutinaDiaria.objects.get(id=rutina_id)
    try:
        rutina.delete()
    except:
        pass
    return redirect ('lista_rutina')


"""

CRUD DE COMENTARIOS:

"""
def lista_comentarios(request):
    comentarios = Comentario.objects.select_related('usuario','entrenamiento').all()
    return render(request,'fitness/comentario/lista_comentarios.html',{'mostrar_comentarios':comentarios})

def mostrar_comentario(request, rutina_id):
    rutina = Comentario.objects.select_related('usuario','entrenamiento').all()
    rutina = rutina.get(id=rutina_id)
    return render(request,'fitness/rutina/mostrar_rutina.html',{'rutina':rutina})

def comentario_create(request):
    datosFormulario = None
    if request.method=='POST':
        datosFormulario = request.POST
    formulario = ComentarioModelForm(datosFormulario)
    if(request.method=='POST'):
        if formulario.is_valid():
            try:
                #Guarda el libro en la base de datos:
                formulario.save()
                return redirect('lista_comentarios')
            except Exception as error:
                print(error)
    return render (request,'fitness/comentario/create.html',{'formulario':formulario})


def comentario_buscar(request):
    formulario = BusquedaComentarioForm(request.GET)
    
    if formulario.is_valid():
        texto = formulario.cleaned_data.get('textoBusqueda')
        comentarios = Comentario.objects.select_related('usuario', 'entrenamiento').all()
        comentarios = comentarios.filter(texto__contains=texto).all()
        return render(request, 'fitness/comentario/lista_busqueda.html', {'comentarios_mostrar': comentarios, 'texto_busqueda': texto})
    if 'HTTP_REFERER' in request.META:
        return redirect(request.META['HTTP_REFERER'])
    else:
        print(formulario.errors)  # Aquí corregí el atributo errors
        return redirect('index')



def comentario_busqueda_avanzada(request):
    if len(request.GET) > 0:
        formulario = BusquedaAvanzadaComentarioForm(request.GET)
        if formulario.is_valid():
            mensaje_busqueda = 'Se ha buscado por los siguientes valores:\n'
            QSRutinas = Comentario.objects.select_related('usuario','entrenamiento').all()

            # Obtenemos los filtros:
            texto_busqueda = formulario.cleaned_data.get('texto_busqueda')
            fecha = formulario.cleaned_data.get('fecha')

            # Por cada filtro comprobamos si tienen un valor y lo añadimos a la QuerySet:
            if texto_busqueda:
                QSRutinas = QSRutinas.filter(Q(texto__contains=texto_busqueda))
                mensaje_busqueda += f" Nombre o contenido que contengan la palabra {texto_busqueda}\n"

            if fecha:
                fecha_limite = datetime(2023, 1, 1).date()
                mensaje_busqueda += f" La fecha sea mayor a {datetime.strftime(fecha, '%d-%m-%Y')}\n"
                QSRutinas = QSRutinas.filter(fecha__gte=fecha_limite)

            comentarios = QSRutinas.all()

            return render(request, 'fitness/comentario/lista_busqueda.html', {'comentarios_mostrar': comentarios, 'texto_busqueda': mensaje_busqueda})
    else:
        formulario = BusquedaAvanzadaRutinaForm(None)

    return render(request, 'fitness/comentario/busqueda_avanzada.html', {'formulario': formulario})



def comentario_editar(request,comentario_id):
    comentario =  Comentario.objects.get(id=comentario_id)
    
    datosFormulario = None
    if(request.method=='POST'):
        datosFormulario = request.POST
    
    formulario = ComentarioModelForm(datosFormulario,instance=comentario)
    if(request.method=='POST'):
        if formulario.is_valid():
            formulario.save()
            try:
                formulario.save()
                return redirect('lista_comentarios')
            except Exception as e:
                pass
    return render(request,'fitness/comentario/actualizar.html',{'formulario':formulario,'comentario':comentario})
        

def comentario_eliminar(request,comentario_id):
    rutina = Comentario.objects.get(id=comentario_id)
    try:
        rutina.delete()
    except:
        pass
    return redirect ('lista_comentarios')




"""
CRUD SUSCRIPCIÓN
"""

def suscripcion_mostrar(request,suscripcion_id):
    suscripcion = Suscripcion.objects.select_related('titular')
    suscripcion = suscripcion.get(id=suscripcion_id)
    return render(request,'fitness/suscripcion/suscripcion_mostrar.html',{'suscripcion':suscripcion})

def suscripcion_create(request):
    
    datosFormulario = None
    
    if(request.method=='POST'):
        datosFormulario = request.POST
    
    formulario = SuscripcionModelForm(datosFormulario)
    if(request.method=='POST'):
        if(formulario.is_valid()):
            try:
                #Gurada el entrenamiento en la base de datos.
                formulario.save()
                #print(formulario)
                return redirect('lista_suscripcion')
            except Exception as error:
                print(error)
    else:
        print(formulario.errors)
    return render(request,'fitness/suscripcion/create.html',{'formulario':formulario})


def lista_suscripcion(request):
    suscripciones = Suscripcion.objects.select_related('titular')
    return render(request,'fitness/suscripcion/lista_suscripcion.html',{'mostrar_suscripcion':suscripciones})

from .models import Suscripcion

def suscripcion_buscar(request):
    formulario = BusquedaSuscripcionForm(request.GET)
    
    if formulario.is_valid():
        texto = formulario.cleaned_data.get('textoBusqueda')
        suscripciones = Suscripcion.objects.filter(banco__icontains=texto)
        return render(request, 'fitness/suscripcion/lista_busqueda.html', {'suscripcion_mostrar': suscripciones, 'texto_busqueda': texto})
    
    # Manejo del caso en que el formulario no es válido
    if 'HTTP_REFERER' in request.META:
        return redirect(request.META['HTTP_REFERER'])
    else:
        print(formulario.errors)
        return redirect('index')




def suscripcion_busqueda_avanzada(request):
    if len(request.GET) > 0:
        formulario = BusquedaAvanzadaSuscripcionForm(request.GET)
        if formulario.is_valid():
            mensaje_busqueda = 'Se ha buscado por los siguientes valores:\n'
            QSRutinas = Comentario.objects.select_related('usuario','entrenamiento').all()

            # Obtenemos los filtros:
            texto_busqueda = formulario.cleaned_data.get('texto_busqueda')
            fecha = formulario.cleaned_data.get('fecha')

            # Por cada filtro comprobamos si tienen un valor y lo añadimos a la QuerySet:
            if texto_busqueda:
                QSRutinas = QSRutinas.filter(Q(texto__contains=texto_busqueda))
                mensaje_busqueda += f" Nombre o contenido que contengan la palabra {texto_busqueda}\n"

            if fecha:
                fecha_limite = datetime(2023, 1, 1).date()
                mensaje_busqueda += f" La fecha sea mayor a {datetime.strftime(fecha, '%d-%m-%Y')}\n"
                QSRutinas = QSRutinas.filter(fecha__gte=fecha_limite)

            comentarios = QSRutinas.all()

            return render(request, 'fitness/comentario/lista_busqueda.html', {'comentarios_mostrar': comentarios, 'texto_busqueda': mensaje_busqueda})
    else:
        formulario = BusquedaAvanzadaRutinaForm(None)

    return render(request, 'fitness/comentario/busqueda_avanzada.html', {'formulario': formulario})


def suscripcion_editar(request,suscripcion_id):
    suscripcion =  Suscripcion.objects.get(id=suscripcion_id)
    
    datosFormulario = None
    if(request.method=='POST'):
        datosFormulario = request.POST
    
    formulario = SuscripcionModelForm(datosFormulario,instance=suscripcion)
    if(request.method=='POST'):
        if formulario.is_valid():
            formulario.save()
            try:
                formulario.save()
                return redirect('lista_suscripcion')
            except Exception as e:
                pass
    return render(request,'fitness/suscripcion/actualizar.html',{'formulario':formulario,'suscripcion':suscripcion})
        

def suscripcion_eliminar(request,suscripcion_id):
    rutina = Suscripcion.objects.get(id=suscripcion_id)
    try:
        rutina.delete()
    except:
        pass
    return redirect ('lista_suscripcion')


#VISTA DE REGISTRAR USUARIO:
def registrar_usuario(request):
    if request.method == 'POST':
        formulario = RegistroForm(request.POST)
        if formulario.is_valid():
            user = formulario.save()
            rol = int(formulario.cleaned_data.get('rol'))
            if(rol == Usuario.CLIENTE):
                grupo = Group.objects.get(name='Clientes') 
                grupo.user_set.add(user)
                cliente = Cliente.objects.create( usuario = user)
                cliente.save()
            elif(rol == Usuario.ENTRENADOR):
                grupo = Group.objects.get(name='Bibliotecarios') 
                grupo.user_set.add(user)
                entrenador = Entrenador.objects.create(usuario = user)
                entrenador.save()
            
            login(request, user)
            return redirect('index')
    else:
        formulario = RegistroForm()
    return render(request, 'registration/signup.html', {'formulario': formulario})





















































































































"""
    
        VIEWS DEL EXAMEN
    
    """
    
def mostrar_promocion(request,promocion_id):
    promocion = Promocion.objects.select_related('usuario')
    promocion = promocion.get(id=promocion_id)
    return render (request, 'fitness/promocion/mostrar_promocion.html',{'promocion':promocion})
def lista_promocion(request):
    promociones = Promocion.objects.select_related('usuario')
    return render(request,'fitness/promocion/lista_promocion.html',{'mostrar_promociones':promociones})


def promocion_create(request):
    datosFormulario = None
    if request.method=='POST':
        datosFormulario = request.POST
    formulario = PromocionModelForm(datosFormulario)
    if(request.method=='POST'):
        if formulario.is_valid():
            try:
                #Guarda el libro en la base de datos:
                formulario.save()
                return redirect('lista_promocion')
            except Exception as error:
                print(error)
    return render (request,'fitness/promocion/create.html',{'formulario':formulario})

def promocion_eliminar(request,promocion_id):
    promocion = Promocion.objects.get(id=promocion_id)
    try:
        promocion.delete()
        messages.success(request, "Se ha eliminado el ejercicio "+ promocion.nombre+" correctamente")
    except:
        pass
    return redirect ('lista_promocion')

def promocion_editar(request,promocion_id):
    promocion = Promocion.objects.get(id=promocion_id)
    
    datosFormulario = None
    
    if(request.method == 'POST'):
        datosFormulario = request.POST
        
    formulario = PromocionModelForm(datosFormulario,instance= promocion)
    
    if(request.method=='POST'):
        if(formulario.is_valid()):
            formulario.save()
            try:
                formulario.save()
                messages.success(request, 'Se ha editado la promocion'+formulario.cleaned_data.get('nombre')+" correctamente")
                return redirect('lista_promocion')
            except Exception as error:
                print(error)
    return render(request,'fitness/promocion/actualizar.html',{'formulario':formulario,'promocion':promocion})

def promocion_busqueda_avanzada(request):
    
    #Vamos a verificar si tenemos datos o no, para procesar el formulario y validarlo.
    if(len(request.GET)> 0):
        formulario = BusquedaAvanzadaPromocionForm(request.GET)
        if formulario.is_valid():
            print('Es valido')
            
            mensaje_busqueda = 'Se ha buscado por los siguientes valores: \n'
            
            QSEjercicios = Promocion.objects.prefetch_related('usuarios_votos')
            
            #OBTENEMOS LOS FILTROS:
            textoBusqueda = formulario.cleaned_data['textoBusqueda']
            descripcion = formulario.cleaned_data['descripcion']
            #usuarios = formulario.cleaned_data.get['usuarios', []]
            
            #POR CADA FILTRO COMPROBAMOS SI TIENE UN VALOR Y LO AÑADIMOS A LA QUERYSET:
            if textoBusqueda:
                QSPromociones = QSPromociones.filter(Q(nombre__contains=textoBusqueda) | Q(descripcion__contains=textoBusqueda))
                mensaje_busqueda +=" Nombre o contenido que contengan la palabra "+textoBusqueda+"\n"
            if descripcion:
                QSPromociones = QSPromociones.filter(Q(nombre__contains=descripcion) | Q(descripcion__contains=descripcion))
                mensaje_busqueda +=" Nombre o contenido que contengan la palabra "+descripcion+"\n"
                
            promociones = QSPromociones.all()
            
            print('Estamos aqui')
            
            return render(request,'fitness/promocion/lista_busqueda.html',{'ejercicios_mostrar':promociones,'texto_busqueda':mensaje_busqueda})
    else:
        #En el caso de que procesa desde una URL y no tenga datos, mostramos el formulario correspondiente.
        formulario = BusquedaAvanzadaPromocionForm(None)
        print('No hay nada')
    return render(request,'fitness/ejercicio/busqueda_avanzada.html',{'formulario':formulario})



