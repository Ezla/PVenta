from django.db import models
from django.core.exceptions import ValidationError

from .validators import validate_product


class Marca(models.Model):
    marca = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.marca


class Producto(models.Model):
    code39 = models.BooleanField(default=False)
    codigo = models.CharField(max_length=48, unique=True, null=True,
                              blank=True)
    descripcion = models.CharField(max_length=100)
    marca = models.ForeignKey(Marca, on_delete=models.SET_NULL, null=True)
    vunidad = models.BooleanField(default=True)
    punitario = models.DecimalField(max_digits=8, decimal_places=2)
    pmayoreo = models.DecimalField(max_digits=8, decimal_places=2)
    inventario = models.BooleanField(default=False)
    cantidad = models.IntegerField(null=True, blank=True)
    minimo = models.IntegerField(null=True, blank=True)
    modificado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.descripcion

    def clean(self):
        data = {'code39': self.code39, 'codigo': self.codigo,
                'punitario': self.punitario, 'pmayoreo': self.pmayoreo,
                'inventario': self.inventario, 'cantidad': self.cantidad,
                'minimo': self.minimo, 'marca': self.marca}

        cont, errores = validate_product(data=data)

        if cont == 1:
            raise ValidationError(errores)
