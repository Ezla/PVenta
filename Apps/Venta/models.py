from django.db import models


class Cuenta(models.Model):
    tiket = models.CharField(max_length=30, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    efectivo = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    cambio = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    creado = models.DateTimeField(auto_now_add=True, null=True)
    modificado = models.DateTimeField(auto_now=True, null=True)

    def __unicode__(self):
        return self.tiket


class Venta(models.Model):
    codigo = models.CharField(max_length=48, null=True)
    nombre = models.CharField(max_length=100, null=True)
    descuento = models.BooleanField(default=False)
    precio = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    cantidad = models.IntegerField(null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    cuenta = models.ForeignKey(Cuenta, null=True)

    def __unicode__(self):
        return unicode(self.nombre)
