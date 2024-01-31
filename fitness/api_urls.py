from django.urls import path
from .api_views import *

urlpatterns = [
    path('ejercicios',ejercicio_list),
    path('ejercicios/busqueda_simple',ejercicio_buscar),
<<<<<<< HEAD
   # path('ejercicios/busqueda_avanzada',ejercici)
]
=======
    #path('ejercicios/busqueda_avanzada',ejercici)
]
>>>>>>> 02f75532ba09a82c7b69fa3e4382ec774643e968
