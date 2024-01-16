from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .forms import *


@api_view(['GET'])
def ejercicio_list(request):
    
    ejercicios = Ejercicio.objects.all()
    serializer = EjercicioSerializer(ejercicios, many=True)
    return Response(serializer.data)