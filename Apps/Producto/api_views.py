from rest_framework import viewsets

from .serializers import ProductoSerializer
from .models import Producto


class ProductoApiView(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
