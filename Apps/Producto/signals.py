from django.db.models.signals import pre_save

from .models import Producto
from .utils import random_string


def pre_save_product(sender, instance, **kwargs):
    """
    Generamos un codigo39 aleatorio unico para el producto a guardar, si
    es que es requerido.
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    # Si el codigo es None, entonces lo pasamos como cadena vacia para
    # poder medir su longitud.
    if instance.codigo is None:
        instance.codigo = ''

    length = len(instance.codigo) != 10
    pk_is_non = instance.pk is None
    invalid_code = True

    # validamos si el codigo ya existe en otro producto
    while invalid_code:
        new_code39 = random_string(length=10, uppercase=True)
        invalid_code = Producto.objects.filter(codigo=new_code39).exists()

    # asignamos codigo 39 a la instancia si se requiere
    if instance.code39 and pk_is_non:
        # create
        instance.codigo = new_code39
    elif instance.code39 and not pk_is_non and length:
        # update
        instance.codigo = new_code39


pre_save.connect(pre_save_product, sender=Producto)
