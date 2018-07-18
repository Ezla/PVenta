from django.db.models.signals import pre_save

from .models import SalesAccount
from Apps.Producto.utils import random_string


def pre_save_sales_account(sender, instance, **kwargs):
    """
    Generamos un codigo aleatorio unico para el ticket de la cuenta a
    guardar.
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    # Si el codigo del ticket es None, entonces lo pasamos como cadena
    # vacia para poder medir su longitud.
    if instance.ticket is None:
        instance.ticket = ''

    length = len(instance.ticket) != 10
    pk_is_non = instance.pk is None
    invalid_ticket = True

    # validamos si el codigo de ticket ya existe en otra venta
    while invalid_ticket:
        new_ticket = random_string(length=10, uppercase=True)
        invalid_ticket = SalesAccount.objects.filter(
            ticket=new_ticket).exists()

    # asignamos codigo de ticket a la instancia si se requiere
    if pk_is_non:
        # create
        instance.ticket = new_ticket
    elif not pk_is_non and length:
        # update
        instance.ticket = new_ticket


pre_save.connect(pre_save_sales_account, sender=SalesAccount)
