from typing import Any
from django import forms
from .models import *
from django.forms import ModelForm
import re 

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
    
    
    
#------------------ENTRENAMIOENTO----------------------
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
    ejercicios = models.ManyToManyField(Ejercicio,through='EntrenamientoEjercicio')
    
 
 
 class EntrenamientoForm(forms.Form):
    nombre = forms.CharField(label = 'Nombre', max_length=200, required=False)
    descripcion = forms.CharField(label='Descripcion',required=False,widget=forms.Textarea())
    duracion = forms.IntegerField()
    tipo = forms.ChoiceField(choices=Entrenamiento.TIPOS,
                             initial='AER')
    #Campo SelectMultiple para sellecionar los ejercicios que es una relación ManytoMany
    ejerciciosDisponibles = Ejercicio.objects.all()
    ejercicios = forms.ModelMultipleChoiceField(
        queryset=ejerciciosDisponibles,
        required=True,
        help_text='Selecciona varios ejercicios'
    )
    #Campo para selelcionar un usuario que es una relación ManytoOne:
    usuariosDisponibles= Usuario.objects.all()
    usuario = forms.ModelChoiceField(
    queryset=usuariosDisponibles,
    widget=forms.Select,
    required=True,
    empty_label='Ninguna'
    )
        
        """

    
class EntrenamientoForm(forms.ModelForm):
    class Meta:
        model = Entrenamiento
        fields = ['nombre', 'descripcion', 'duracion', 'tipo', 'ejercicios', 'usuario']
   
    
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
                self.add_error('fecha_inicio','fecha_fin',"La fecha de fin debe ser posterior a la fecha de inicio.")
            
        return self.cleaned_data
    
class BusquedaPlanForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)  
    

class BusquedaAvanzadaPlanForm(forms.Form):
    #usuario,descripcion,fecha_inicio,fecha_fin:
    texto_busqueda = forms.CharField(required=False)
    descripcion = forms.Textarea()
    fecha_desde = forms.DateField(label='Fecha Inicio',
                                  required=False,
                                  widget=forms.SelectDateWidget(years=range(1990,2023)))
    fecha_hasta = forms.DateField(label='Fecha hasta',
                                  required=False,
                                  widget=forms.SelectDateWidget(years=range(1990,2024)))
    
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
            self.add_error('fecha_desde','Debe introduicar al menos un valor en un campo del formulario.')
            self.add_error('fecha_hasta','Debe introducir al menos un valor de un campo del formulario.')
        else:
            if(texto_busqueda != '' and len(texto_busqueda)<3):
                self.add_error('texto_busqueda','Debe introduciar al menos 3 caracteres.')
                
            if(not fecha_desde is None and not fecha_hasta is None and fecha_hasta < fecha_desde):
                self.add_error('fecha_desde','La fecha de fin no puede ser menor que la fecha de inicio.')
                self.add_error('fecha_hasta','La fecha de fin no puede ser menor que la fecha de incio.')
        
        return self.cleaned_data
    
    
        """
        
                                    FORMULARIOS DEL EXAMEN:
   
        
        """                 

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
        
        """
        Nombre de la promoción: el nombre tiene que ser único.
        Descripción de la promoción: Debe tener al menos 100 caracteres
        Usuario al que se le aplica la promoción: Un usuario no puede usar la misma promoción dos veces
        Descuento que se le aplica: Tiene que ser un valor entero entre 0 y 100
        Fecha fin de la promoción: Esta fecha no puede inferior a la fecha actual
        """
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
    
    
    
    
    
    
    
    
    
    
    
    
   