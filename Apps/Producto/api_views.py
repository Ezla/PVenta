from rest_framework import viewsets

from .serializers import ProductoSerializer, BrandSerializer
from .models import Producto, Marca


class ProductoApiView(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer


class BrandApiView(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = BrandSerializer
