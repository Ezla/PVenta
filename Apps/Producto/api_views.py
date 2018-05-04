from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.views import APIView
from .serializers import ProductoSerializer, ProductoExistsSerializer, BrandSerializer
from .models import Producto, Marca


class ProductExistsView(APIView):

    def get(self, request, code=None):
        queryset = Producto.objects.all()
        user = get_object_or_404(queryset, codigo=code)
        serializer = ProductoExistsSerializer(user)
        return Response(serializer.data)


class ProductoApiView(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    def generate_code39(self):
        code = str(self.product.pk)
        while len(code) < 10:
            code = '0' + code
        return code

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.product = serializer.save()
            if self.product.code39:
                code39 = self.generate_code39()
                self.product.codigo = code39
                self.product.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response( serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        self.product = self.get_object()
        serializer = self.get_serializer(self.product, data=request.data)
        if serializer.is_valid():
            self.product = serializer.save()
            if self.product.code39:
                code39 = self.generate_code39()
                self.product.codigo = code39
                self.product.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BrandApiView(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = BrandSerializer
