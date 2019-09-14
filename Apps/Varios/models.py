from django.db import models


class Listed(models.Model):
    MONOGRAPH = '1'
    BIOGRAPHY = '2'
    MAP = '3'
    TYPE_CHOICES = (
        (MONOGRAPH, 'Monografía'),
        (BIOGRAPHY, 'Biografia'),
        (MAP, 'Mapa')
    )
    SUN_RISE = '1'
    RAF = '2'
    PROVIDERS_CHOICES = (
        (SUN_RISE, 'SUN RISE'),
        (RAF, 'RAF')
    )
    name = models.CharField(verbose_name='Nombre', max_length=100,
                            unique=True)
    number = models.IntegerField(verbose_name='Numero de lista', default=0)
    type = models.CharField(verbose_name='Tipo de producto',
                            choices=TYPE_CHOICES, max_length=1)
    reference_number = models.CharField(
        verbose_name='Número de referencia', max_length=8)
    provider = models.CharField(verbose_name='Proveedor del producto',
                                choices=PROVIDERS_CHOICES, max_length=1)
    active = models.BooleanField(verbose_name='Activar para listar',
                                 default=True)

    def __str__(self):
        return self.name
