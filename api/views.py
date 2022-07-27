from django.shortcuts import render, get_object_or_404
from fac.models import Cliente

#Librerias de rest_framework
from rest_framework.views import APIView
from rest_framework.response import Response

#Importacion de los Serializer creados
from .serializers import ProductoSerializer, ClienteSerializer

from inv.models import Producto
from django.db.models import Q

class ProductoList(APIView):
    def get(self,request):
        prod = Producto.objects.all()
        data = ProductoSerializer(prod,many=True).data
        return Response(data)


class ProductoDetalle(APIView):
    def get(self, request, codigo):
        #Busquedad de un solo producto usando el objeto q para filtrar por dos variables
        prod = get_object_or_404(Producto, Q(codigo = codigo) | Q(codigo_barras = codigo))
        #Serializacion del producto traido de la base de datos
        data = ProductoSerializer(prod).data
        return Response(data)

class ClienteList(APIView):
    def get(self,request):
        obj = Cliente.objects.all()
        data = ClienteSerializer(obj,many=True).data
        return Response(data)
