from rest_framework import serializers

from .models import Producto
from .validators import validate_product


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ('code39', 'codigo', 'descripcion', 'vunidad', 'punitario',
                  'pmayoreo', 'inventario', 'cantidad', 'minimo', 'marca')

    def validate(self, data):
        valid, errores = validate_product(dict(data))

        if valid == 1:
            raise serializers.ValidationError(errores)
        return data
