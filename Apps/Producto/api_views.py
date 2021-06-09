from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.views import APIView

from .serializers import ProductoSerializer, ProductoExistsSerializer, \
    BrandSerializer
from .models import Producto, Marca


class ProductExistsView(APIView):

    def get(self, request, code=None):
        queryset = Producto.objects.all()
        user = get_object_or_404(queryset, codigo=code)
        serializer = ProductoExistsSerializer(user)
        return Response(serializer.data)


class ProductSearchSuggestionsView(APIView):

    def get(self, request, word=None):
        productsCode39 = Producto.objects.filter(code39=True)
        queryset = productsCode39.filter(Q(codigo__icontains=word) |
                                         Q(descripcion__icontains=word))
        serializer = ProductoExistsSerializer(queryset, many=True)
        return Response(serializer.data)


class ProductoApiView(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer


class BrandApiView(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = BrandSerializer
