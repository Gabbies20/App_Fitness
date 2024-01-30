from typing import Any
from django import forms
from .models import *
from django.forms import ModelForm
import re 
from datetime import datetime 
from django.contrib.auth.forms import UserCreationForm

"""
Los formularios en Django se crean mediante la definición de una clase que hereda de django.forms.Form. 
    """

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
            
        
        if not re.match("^[a-zA-ZÀ-ÖØ-öø-ÿ]+$", tipo_ejercicio):
        
           # La función re.match(pattern, string) es una función del módulo re en Python que se utiliza para verificar si el patrón especificado al principio de la cadena coincide. 
        
            self.add_error('tipo_ejercicio','Este campo solo debe contener letras.')
            
        return self.cleaned_data
        
        
#FORMULARIO DE BÚSQUEDA PARA EJERCICIO:
class BusquedaEjercicioForm(forms.Form):
    #El formulario solo tendra un campo y este no esta relacionado con ningún modelo, por esa razón se usa el formulario genérico.
    textoBusqueda = forms.CharField(required=True)
    
    
    
class BusquedaAvanzadaEjercicioForm(forms.Form):

        
        
    """
    forms.CharField: Sería como un InputText en HTML y los usaremos para los campos tipo Char y Text
forms.DateField: Sería como input tipo Date en HTML y lo usaremos para los campos tipo Fecha
forms.ChoiceField: Sería como un select en HTML y lo usaremos para los campos tipo Char con opciones
forms.ModelChoiceField: Sería como un Select en HTML y lo usaremos para las relaciones OneToOne o ManyToOne
forms.ModelMultipleChoiceField: Sería como un Select Múltiple en HTML y lo usaremos para las relaciones ManyToMany o OneToMany 
Existen más tipos de campos que podemos encontrar en la documentación
    
    """
    
    """
    Los campos anteriormente especificados pueden tener una serie de parámetros para personalizarlos. :
required: Para indicar si el campo es obligatorio en el formulario.
max_length: Para indicar el tamaño máximo de caracteres del campo
help_text: Texto de ayuda que aparecerá al lado del campo del formulario para facilitar la introducción de datos al usuario
label: La etiqueta label que queremos que aparezca en el formulario asociada al campo
initial: Valor por defecto en el campo
choices: Para especificar los valores que aparecerán para seleccionar en el Select
empty_label: Cuando hay que seleccionar en un Select
querySet: QuerySet del Modelo correspondiente a la relación. Para que aparezcan las opciones correspondientes. """
    
    textoBusqueda = forms.CharField(required=False)
    descripcion = forms.CharField(widget=forms.Textarea, required=False)


    def clean(self):
    
        super().clean()

        # Obtenemos los campos:
        textoBusqueda = self.cleaned_data.get('textoBusqueda')
        descripcion = self.cleaned_data.get('descripcion')
        # Corregir sintaxis

        # Controlamos los campos:
        if not textoBusqueda and not descripcion:
            self.add_error('textoBusqueda', 'Debo introducir al menos un valor en un campo del formulario')
            self.add_error('descripcion', 'Debo introducir al menos un valor en el campo de la descripción')
        else:
        # Si introduce un texto al menos que tenga  3 caracteres o más
            if textoBusqueda and len(textoBusqueda) < 3:
                self.add_error('textoBusqueda', 'Debe introducir al menos 3 caracteres')
                
            if descripcion and len(descripcion) < 3:
                self.add_error('descripcion', 'Debe introducir al menos 3 caracteres')
            
            
        #Siempre devolvemos el conjunto de datos.
        return self.cleaned_data
    
    
    
#------------------ENTRENAMIENTO----------------------
        """
        
       class Entrenamiento(models.Model):
    TIPOS = [
        ('AER','Aeróbico'),
        ('FUE','Fuerza o anaeróbico'),
        ('FUN','Funcional'),
        ('HIT','Hit'),
        ('POT','Potencia'),
    ]
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    descripcion= models.TextField()
    duracion = models.IntegerField()
    tipo = models.CharField(max_length=3,
                            choices=TIPOS,
                            default='HIT',
                            )
    ejercicios = models.ManyToManyField(Ejercicio,through='EntrenamientoEjercicio'    
        """
class EntrenamientoForm(ModelForm):
    class Meta:
        model = Entrenamiento
        fields = ['nombre','descripcion','duracion','tipo','usuario','ejercicios']
        labels = {
            'nombre':('Nombre del entrenamiento'),
            
        }
        help_texts = {
            'nombre':('200 caracteres como máximo'),
            'ejercicios':('Mantén pulasada la tecla control paar seleccionar varios elementos.')
        }
        widgets = {
            'tipo': forms.Select(attrs={'class': 'tu-clase-css'}),
    'duracion': forms.NumberInput(attrs={'class': 'otra-clase-css', 'min': 0}),
        }


    def clean(self):
        super().clean()
        
        nombre = self.cleaned_data.get('nombre')
        descripcion = self.cleaned_data.get('descripcion')
        duracion = self.cleaned_data.get('duracion')
        tipo = self.cleaned_data.get('tipo')
        usuario = self.cleaned_data.get('usuario')
        ejercicios = self.cleaned_data.get('ejercicios')
        

        if len(nombre) < 3:
            self.add_error('nombre','El nombre debe tener al menos 3 caracteres.')
            
        if tipo == 'HIT' and duracion > 30:
            self.add_error('tipo','La duración para entrenamientos HIT no debe ser mayor a 30 minutos.')

        if ejercicios and len(ejercicios) < 2 :
            self.add_error('ejercicios','Selecciona al menos 2 ejercicios.')
        
        return self.cleaned_data

class BusquedaEntrenamientoForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)


class BusquedaAvanzadaEntrenamientoForm(forms.Form):
    textoBusqueda = forms.CharField(required=False)
    tipos = forms.MultipleChoiceField(choices =Entrenamiento.TIPOS,
                                      required=False,
                                      widget=forms.CheckboxSelectMultiple())
    duracion = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'min': 1, 'max': 100, 'class': 'tu-clase-css'})
    )
    
    def clean(self):
        super().clean()

        textoBusqueda = self.cleaned_data.get('textoBusqueda')
        tipos = self.cleaned_data.get('tipos')
        duracion = self.cleaned_data.get('duracion')
        

        # Si introduce un texto, debe tener 3 caracteres o más
        if textoBusqueda and len(textoBusqueda) < 3:
            self.add_error('textoBusqueda', 'Debe introducir al menos 3 caracteres')

        # La duración debe estar en el rango de 1 a 100
        if duracion is not None and (duracion < 1 or duracion > 100):
            self.add_error('duracion', 'La duración debe estar en el rango de 1 a 100.')

        # Validación de tipos (puedes ajustar según tus necesidades)
        #'issubset es un método en Python que pertenece al tipo de datos set. Este método se utiliza para comprobar si todos los elementos de un conjunto están presentes en otro conjunto.
        #En otras palabras, estamos asegurándonos de que todas las claves seleccionadas por el usuario (tipos) estén presentes en la lista de claves definidas en Entrenamiento.TIPOS. 
        if tipos and not set(tipos).issubset(dict(Entrenamiento.TIPOS).keys()):
            self.add_error('tipos', 'Selecciona tipos válidos.')

        # Siempre devolvemos el conjunto de datos
        return self.cleaned_data    






    
"""
        FORMULARIOS DE PLAN DE ENTRENAMIENTO:
        class PlanEntrenamiento(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    duracion_estimada = models.IntegerField()
    dificultad = models.CharField(max_length=20)
    entrenamientos = models.ManyToManyField('Entrenamiento', through='EntrenamientoPlan')
    fecha_inicio = models.DateTimeField(default=timezone.now)
    fecha_fin = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nombre
        """
    
    

class PlanEntrenamientoModelForm(ModelForm):
    class Meta:
        model = PlanEntrenamiento
        fields = ['usuario','nombre','descripcion','duracion_estimada','dificultad','entrenamientos','fecha_inicio','fecha_fin']
        help_texts ={
            'nombre':('100 caracteres como máximo.'),
            'entrenamientos' : ('Mantén pulsada la tecla control para seleccionar varios elementos.')
        }
        widgets = {
            'fecha_inicio':forms.SelectDateWidget(),
            'fecha_fin' : forms.SelectDateWidget()
        }
        localized_fields = ['fecha_inicio','fecha_fin']
        
        
    #Este metodo sirve para comprobar si los campos tienen el valor adecuado paar el modelo.
    def clean(self):
        
        
        #Estás utilizando super().clean() para llamar al método clean de la clase base, lo cual es importante porque realiza la mayor parte del trabajo relacionado con la validación y limpieza estándar proporcionado por Django.
        super().clean()
        #Obtenemos los campos:
        usuario = self.cleaned_data.get('usuario')
        nombre = self.cleaned_data.get('nombre')
        descripcion = self.cleaned_data.get('descripcion')
        duracion_estimada = self.cleaned_data.get('duracion_estimada')
        dificultad = self.cleaned_data.get('dificultad')
        entrenamientos = self.cleaned_data.get('entrenamientos')
        fecha_inicio = self.cleaned_data.get('fecha_inicio')
        fecha_fin = self.cleaned_data.get('fecha_fin')
        
        #Empezamos con las validaciones:
        #Comprobamos que no exista un plan con ese nombre.
        planNombre = PlanEntrenamiento.objects.filter(nombre=nombre).first()
        
        #En Python, None es un valor especial que representa la ausencia de un valor o la falta de asignación a una variable. Es un singleton del tipo NoneType. En otros términos, None no es lo mismo que 0, False, o una cadena vacía. Es un valor único que indica la ausencia de valor o la falta de algo concreto.
        
        #None se evalúa como False en contextos booleanos, pero ten en cuenta que None no es lo mismo que False. Por ejemplo, bool(None) es False, pero None == False es False. Es importante usar is o is not cuando se verifica si una variable es None para evitar sorpresas relacionadas con la igualdad de valores.
        if(not planNombre is None):
            self.add_error('nombre','Ya existe un plan con ese nombre.')
            
        if not usuario:
            self.add_error('usuario',"El campo usuario es obligatorio.")


        if not descripcion:
            self.add_error('descripcion',"El campo descripcion es obligatorio.")

        if duracion_estimada <= 0:
            self.add_error('duracion_estimada',"La duración estimada debe ser un número positivo.")

        # Puedes agregar más validaciones según tus necesidades.

        # Validación de fechas
        if fecha_inicio and fecha_fin:
            if fecha_fin < fecha_inicio:
                self.add_error('fecha_inicio', "La fecha de fin debe ser posterior a la fecha de inicio.")
                self.add_error('fecha_fin', "La fecha de fin debe ser posterior a la fecha de inicio.")

            
        return self.cleaned_data
    
    
class BusquedaPlanForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)  
    

class BusquedaAvanzadaPlanForm(forms.Form):
    #usuario,descripcion,fecha_inicio,fecha_fin:
    texto_busqueda = forms.CharField(required=False)
    descripcion = forms.Textarea()
    fecha_desde = forms.DateField(label='Fecha Inicio',
                                  required=False,
                                  widget=forms.SelectDateWidget(years=range(1990,2021)))
    fecha_hasta = forms.DateField(label='Fecha hasta',
                                  required=False,
                                  widget=forms.SelectDateWidget(years=range(1990,2025)))
    
    def clean(self):
        
        super().clean()
        
        #Obtenemos los campos:
        texto_busqueda = self.cleaned_data.get('texto_busqueda')
        descripcion = self.cleaned_data.get('descripcion')
        fecha_desde = self.cleaned_data.get('fecha_desde')
        fecha_hasta = self.cleaned_data.get('fecha_hasta')
        
        #Controlamos los campos:
        if(texto_busqueda==0
           and descripcion == ''
           and fecha_desde is None
           and fecha_hasta is None):
            self.add_error('texto_busqueda','Debe introducir al menos un valor')
            self.add_error('descripcion','Debe introduciar al menos un valor.')
            self.add_error('fecha_desde','Debe introducicar al menos un valor en un campo del formulario.')
            self.add_error('fecha_hasta','Debe introducir al menos un valor de un campo del formulario.')
        else:
            if(texto_busqueda != '' and len(texto_busqueda)<3):
                self.add_error('texto_busqueda','Debe introduciar al menos 3 caracteres.')
                
            if(not fecha_desde is None and not fecha_hasta is None and fecha_hasta < fecha_desde):
                self.add_error('fecha_desde','La fecha de fin no puede ser menor que la fecha de inicio.')
                self.add_error('fecha_hasta','La fecha de fin no puede ser menor que la fecha de incio.')
        
        return self.cleaned_data
    
    
    
"""
FORMULARIO: RUTINA DIARIA

"""
class RutinaModelForm(ModelForm):
    class Meta:
        model = RutinaDiaria
        fields = ['usuario','fecha','descripcion','duracion','ejercicios']
    
        help_texts ={
            'usuario':('500 caracteres como máximo.'),
            'ejercicios' : ('Mantén pulsada la tecla control para seleccionar varios elementos.')
        }
        widgets = {
            'usuario':forms.HiddenInput(),
            'fecha':forms.SelectDateWidget(),
            'duracion': forms.NumberInput(attrs={'min': 0}),  # Agregando el widget NumberInput
        }
        localized_fields = ['fecha']
    
    
    def clean(self):
        super().clean()
        #Obtenemos los campos:
        usuario = self.cleaned_data.get('usuario')
        fecha = self.cleaned_data.get('fecha')
        descripcion = self.cleaned_data.get('descripcion')
        duracion = self.cleaned_data.get('duracion')
        ejercicios = self.cleaned_data.get('ejercicios')
        
        
        #Empezamos con las validaciones:
        if not usuario:
            self.add_error('usuario','El campo usuario es obligatorio.')
        
        if fecha and fecha > timezone.now():
            self.add_error('fecha','La fecha no puede ser en el futuro.')

        if len(descripcion) < 10:
            self.add_error('descripcion','La descripción debe tener al menos 10 caracteres.')


        if duracion is not None and duracion <= 0:
            self.add_error('duracion','La duración debe ser un número positivo mayor que cero.')

    
        if not ejercicios:
            self.add_error('ejercicios','Selecciona al menos un ejercicio.')

        return self.cleaned_data
    
class BusquedaRutinaForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)
    
    
class BusquedaAvanzadaRutinaForm(forms.Form):
    texto_busqueda = forms.CharField(required=False)
    fecha = forms.DateField(label='Fecha',
                                  required=False,
                                  widget=forms.SelectDateWidget(years=range(1900,2025)
                                  ))
    
    def clean(self):
        
        super().clean()
        
        #Obtenemos los campos:
        texto_busqueda = self.cleaned_data.get('texto_busqueda')
        descripcion = self.cleaned_data.get('descripcion')
        fecha = self.cleaned_data.get('fecha')
        
        #Controlamos los campos:
        if(texto_busqueda==0
           and descripcion == ''
           and fecha is None):
            self.add_error('texto_busqueda','Debe introducir al menos un valor')
            self.add_error('fecha','Debe introducicar al menos un valor en un campo del formulario.')
        else:
            if(texto_busqueda != '' and len(texto_busqueda)<3):
                self.add_error('texto_busqueda','Debe introduciar al menos 3 caracteres.')
                
                
            if fecha and fecha.year < 1900:
                self.add_error('fecha', 'La fecha no puede ser anterior a 1900')

                
            
        
        return self.cleaned_data
    
    
    
    
"""
FORMULARIOS DE COMENATRIO:

"""
class ComentarioModelForm(ModelForm):
    class Meta:
        model = Comentario
        fields = ['usuario', 'entrenamiento', 'texto', 'fecha']
        widgets = {
            'entrenamiento': forms.Select(attrs={'class': 'form-control'})
        }

    def clean(self):
        super().clean()
        # Obtenemos los campos
        usuario = self.cleaned_data.get('usuario')
        entrenamiento = self.cleaned_data.get('entrenamiento')
        texto = self.cleaned_data.get('texto')
        fecha = self.cleaned_data.get('fecha')

        # Empezamos con las validaciones
        if not usuario:
            self.add_error('usuario', 'El campo usuario es obligatorio.')

        if not texto:
            self.add_error('texto', 'El campo texto es obligatorio.')

        # Validación específica para el campo entrenamiento
        if not entrenamiento:
            self.add_error('entrenamiento', 'El campo entrenamiento es obligatorio.')

        # Validación de longitud mínima para el texto
        if texto and len(texto) < 10:
            self.add_error('texto', 'El texto debe tener al menos 10 caracteres.')

        # Validación de fecha
        if fecha and fecha > timezone.now():
            self.add_error('fecha', 'La fecha no puede ser en el futuro.')

        # Puedes agregar más validaciones según tus necesidades.

        return self.cleaned_data
    
class BusquedaComentarioForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)
    
    
class BusquedaAvanzadaComentarioForm(forms.Form):
    texto_busqueda = forms.CharField(required=False)
    fecha = forms.DateField(
        label='Fecha',
        required=False,
        widget=forms.SelectDateWidget(years=range(1900, 2025))
    )

    def clean(self):
        super().clean()

        # Obtenemos los campos
        texto_busqueda = self.cleaned_data.get('texto_busqueda')
        fecha = self.cleaned_data.get('fecha')

        # Controlamos los campos
        if not texto_busqueda and not fecha:
            self.add_error('texto_busqueda', 'Debe introducir al menos un valor')
            self.add_error('fecha', 'Debe introducicar al menos un valor en un campo del formulario.')
        else:
            if texto_busqueda and len(texto_busqueda) < 3:
                self.add_error('texto_busqueda', 'Debe introducir al menos 3 caracteres.')

            if fecha and fecha.year < 1900:
                self.add_error('fecha', 'La fecha no puede ser anterior a 1900')

        return self.cleaned_data

    
    
"""

"""
class SuscripcionModelForm(ModelForm) :
      class Meta:
        model = Suscripcion
        fields = ['banco', 'numero_cuenta', 'titular']
        banco = forms.ChoiceField(
        choices=Suscripcion.BANCOS,
        widget=forms.RadioSelect,  # Opcional: Usa RadioSelect para mostrar botones de opción
    )
    
        def clean(self):
            super().clean()
            
            numero_cuenta = self.cleaned_data.get('numero_cuenta')
            titular = self.cleaned_data.get('titular')
            
            
            if not re.match("^[0-9]+$", numero_cuenta):
                self.add_error('numero_cuenta','El número de cuenta debe contener solo dígitos.')
                # Validación: El titular no debe contener caracteres especiales ni números
            if len(titular)< 10:
                self.add_error('titular','El titular no debe contener caracteres menos de 10 caracteres.')

            return self.cleaned_data


class BusquedaSuscripcionForm(forms.Form):
    textoBusqueda = forms.CharField(required=False)
    
class BusquedaAvanzadaSuscripcionForm(forms.Form):
    texto_busqueda = forms.CharField(required=False)
    titular = forms.CharField(required=False)

    def clean(self):
        super().clean()

        # Obtenemos los campos
        texto_busqueda = self.cleaned_data.get('texto_busqueda')
        titular = self.cleaned_data.get('titular')

        # Controlamos los campos
        if not texto_busqueda and not titular:
            self.add_error('texto_busqueda', 'Debe introducir al menos un valor')
            self.add_error('fecha', 'Debe introducicar al menos un valor en un campo del formulario.')
        else:
            if texto_busqueda and len(texto_busqueda) < 3:
                self.add_error('texto_busqueda', 'Debe introducir al menos 3 caracteres.')

            if re.search("[0-9]", titular):
                self.add_error('titular', 'Solo letras, por favor')

        return self.cleaned_data
    
    
    
    
"""
    FORMULARIO AUTENTICACIÓN:
"""
class RegistroForm(UserCreationForm): 
    roles = (
                                (Usuario.CLIENTE, 'cliente'),
                                (Usuario.ENTRENADOR, 'entrenador'),
            )   
    rol = forms.ChoiceField(choices=roles)  
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'password1', 'password2','rol')
    
    
    
class Inscripcion(ModelForm):
    pass













    
class PromocionModelForm(ModelForm):
    class Meta:
        model = Promocion
        fields = ['nombre','descripcion','descuento','fecha','usuario']
        labels = {
            'nombre': ('Nombre de la Promoción')
        }
        help_texts = {
            'nombre':('100 caracteres como maximo'),
            'usuarios':('Mantén pulsado la tecla control para seleccionar más autores')
        }
        widgets = {
            'fecha':forms.SelectDateWidget()
        }
        localized_fields = ['fecha']
        
    def clean(self):
    
        super().clean()
        
        #Obtenemos los campos:
        nombre = self.cleaned_data.get('nombre')
        descripcion = self.cleaned_data.get('descripcion')
        descuento = self.cleaned_data.get('descuento')
        fecha = self.cleaned_data.get('fecha')
        usuario = self.cleaned_data.get('usuario')
        
        promocionNombre = Promocion.objects.filter(nombre=nombre).first()
        if(not promocionNombre is None):
            self.add_error('nombre','Ya existe una promoción con ese nombre.')
    
    
        if(len(descripcion) < 100):
            self.add_error('descripcion','Debes introducir al menos 100 caracteres.')
            
        if not (0 <= descuento <=100):
            self.add_error('descuento','Tiene que ser un valor entero entre 0 y 100')
            
        if fecha < timezone.now().date():
            self.add_error('fecha','La fecha de fin de la promoción no puede ser inferior a la fecha actual.')
            
        return self.cleaned_data
    
#FORMULARIO DE LA PROMOCION PARA BUSQUEDA AVANZADA:
class BusquedaAvanzadaPromocionForm(forms.Form):
    
    textoBusqueda = forms.CharField(required=False)
    descripcion = forms.CharField(widget=forms.Textarea, required=False)


    def clean(self):
    
        super().clean()

        # Obtenemos los campos:
        textoBusqueda = self.cleaned_data.get('textoBusqueda')
        descripcion = self.cleaned_data.get('descripcion')
        # Corregir sintaxis

        # Controlamos los campos:
        if not textoBusqueda and not descripcion:
            self.add_error('textoBusqueda', 'Debo introducir al menos un valor en un campo del formulario')
            self.add_error('descripcion', 'Debo introducir al menos un valor en el campo de la descripción')
        else:
        # Si introduce un texto al menos que tenga  3 caracteres o más
            if textoBusqueda and len(textoBusqueda) < 3:
                self.add_error('textoBusqueda', 'Debe introducir al menos 3 caracteres')
                
            if descripcion and len(descripcion) < 100:
                self.add_error('descripcion', 'Debe introducir al menos 3 caracteres')
            
            
        #Siempre devolvemos el conjunto de datos.
        return self.cleaned_data
    
