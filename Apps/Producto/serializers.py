from rest_framework import serializers

from .models import Producto, Marca
from .validators import validate_product


class ProductoExistsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ('codigo', 'descripcion')


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ('pk', 'code39', 'codigo', 'descripcion', 'vunidad', 'punitario',
                  'pmayoreo', 'inventario', 'cantidad', 'minimo', 'marca')

    def validate(self, data):
        valid, errores = validate_product(dict(data))

        if valid == 1:
            raise serializers.ValidationError(errores)
        return data


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = ('marca', 'pk')
