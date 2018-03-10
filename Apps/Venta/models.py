from django.db import models
from django.core.exceptions import ValidationError


def default_descuento():
    descuento = Descuento.objects.get_or_create(descuento=0)
    return descuento[0].pk


class Descuento(models.Model):
    descuento = models.PositiveSmallIntegerField(unique=True)

    def __str__(self):
        return 'Descuento del {}%'.format(self.descuento)

    def clean(self):
        if self.descuento > 100:
            msg = 'Este campo no puede contener numeros mayores a 100.'
            raise ValidationError({'descuento': msg})


class Cuenta(models.Model):
    tiket = models.CharField(max_length=30, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    efectivo = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    cambio = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    creado = models.DateTimeField(auto_now_add=True, null=True)
    modificado = models.DateTimeField(auto_now=True, null=True)
    descuento = models.ForeignKey(Descuento, on_delete=models.CASCADE,
                                  default=default_descuento)

    def __str__(self):
        return self.tiket


class Venta(models.Model):
    codigo = models.CharField(max_length=48, null=True)
    nombre = models.CharField(max_length=100, null=True)
    descuento = models.BooleanField(default=False)
    precio = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    cantidad = models.IntegerField(null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    cuenta = models.ForeignKey(Cuenta, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nombre
