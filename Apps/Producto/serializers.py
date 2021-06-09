from rest_framework import serializers

from .models import Producto, Marca
from .validators import validate_product


class ProductoExistsSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source='marca.marca')

    class Meta:
        model = Producto
        fields = ('pk', 'codigo', 'descripcion', 'brand_name')


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ('pk', 'code39', 'codigo', 'descripcion', 'vunidad',
                  'punitario', 'pmayoreo', 'inventario', 'cantidad',
                  'minimo', 'marca')

    def validate(self, data):
        valid, errores = validate_product(dict(data))

        if valid == 1:
            raise serializers.ValidationError(errores)
        return data


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = ('marca', 'pk')
