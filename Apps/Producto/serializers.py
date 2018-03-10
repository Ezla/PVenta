from rest_framework import serializers

from .models import Producto


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ('code39', 'codigo', 'descripcion', 'vunidad', 'punitario',
                  'pmayoreo', 'inventario', 'cantidad', 'minimo', 'marca')
