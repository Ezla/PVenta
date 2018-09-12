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
    name = models.CharField(verbose_name='Nombre', max_length=100,
                            unique=True)
    number = models.IntegerField(verbose_name='Numero de lista', default=0)
    type = models.CharField(verbose_name='Tipo de producto',
                            choices=TYPE_CHOICES, max_length=1)
    active = models.BooleanField(verbose_name='Activar para listar',
                                 default=True)

    def __str__(self):
        return self.name
