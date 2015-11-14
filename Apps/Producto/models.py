from django.db import models
from django.core.exceptions import ValidationError


class Marca(models.Model):
    marca = models.CharField(max_length=30, unique=True)

    def __unicode__(self):
        return self.marca


class Producto(models.Model):
    code39 = models.BooleanField(default=False)
    codigo = models.CharField(max_length=48, unique=True, null=True, blank=True)
    descripcion = models.CharField(max_length=100)
    marca = models.ForeignKey(Marca, null=True)
    vunidad = models.BooleanField(default=True)
    punitario = models.DecimalField(max_digits=8, decimal_places=2)
    pmayoreo = models.DecimalField(max_digits=8, decimal_places=2)
    inventario = models.BooleanField(default=False)
    cantidad = models.IntegerField(null=True, blank=True)
    minimo = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.descripcion

    def clean(self):
        errores = {}
        cont = 0
        if not self.code39:
            if len(self.codigo) == 0:
                errores.update({'codigo': 'Este campo es obligatorio.'})
                cont = 1
            if len(self.codigo) < 8:
                errores.update({'codigo': 'El codigo de barras debe contener al menos ocho caracteres.'})
                cont = 1
        # ---punitario---
        if self.punitario < self.pmayoreo:
            errores.update({'punitario': 'El precio unitario debe ser mayor que el precio  por mayoreo.'})
            cont = 1
        if self.punitario < 0:
            errores.update({'punitario': 'Este campo no puede contener numeros negativos.'})
            cont = 1
        # ---pmayoreo---
        if self.punitario < self.pmayoreo:
            errores.update({'pmayoreo': 'El precio por mayoreo debe ser menor al precio unitario.'})
            cont = 1
        if self.pmayoreo < 0:
            errores.update({'pmayoreo': 'Este campo no puede contener numeros negativos.'})
            cont = 1
        # ---inventario---
        if self.inventario:
            # ---cantidad---
            if self.cantidad is None:
                errores.update({'cantidad': 'Si activas la opcion de inventario. Este campo es obligatorio.'})
                cont = 1
            elif self.cantidad < 0:
                errores.update({'cantidad': 'Este campo no puede contener numeros negativos.'})
                cont = 1
            # ---minimo---
            if self.minimo is None:
                errores.update({'minimo': 'Si activas la opcion de inventario. Este campo es obligatorio.'})
                cont = 1
            elif self.minimo < 0:
                errores.update({'minimo': 'Este campo no puede contener numeros negativos.'})
                cont = 1

        if cont == 1:
            raise ValidationError(errores)
