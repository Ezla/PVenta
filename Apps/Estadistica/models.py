from django.db import models


class Provider(models.Model):
    name = models.CharField(verbose_name='Nombre del proveedor',
                            max_length=45,
                            unique=True)
    phone = models.CharField(verbose_name='Número de teléfono',
                             max_length=12)

    def __str__(self):
        return self.name


class ForeignInvoice(models.Model):
    PAID = '1'
    SLOPE = '2'
    CANCELLED = '3'

    INVOICE_STATUS_CHOICES = (
        (PAID, 'Pagada'),
        (SLOPE, 'Pendiente'),
        (CANCELLED, 'Cancelada')
    )

    folio = models.CharField(verbose_name='Folio de la factura',
                             max_length=12)
    amount = models.DecimalField(verbose_name='Monto a pagar',
                                 max_digits=8,
                                 decimal_places=2)
    provider = models.ForeignKey(to=Provider, on_delete=models.CASCADE)
    discount = models.PositiveIntegerField(
        verbose_name='Porcentaje de descuento')
    discount_applied = models.BooleanField(
        verbose_name='Descuento aplicado',
        default=False)
    status = models.CharField(verbose_name='Estado de la factura',
                              choices=INVOICE_STATUS_CHOICES, max_length=1)
    invoice_date = models.DateField(verbose_name='Fecha de la factura')
    settlement_date = models.DateField(verbose_name='Fecha de liquidación')


class Payment(models.Model):
    CASH = '1'
    DEPOSIT = '2'
    TRANSFER = '3'
    CHECK = '4'

    PAYMENT_METHOD_CHOICES = (
        (CASH, 'Efectivo'),
        (DEPOSIT, 'Deposito'),
        (TRANSFER, 'Transferencia'),
        (CHECK, 'Cheque ')
    )

    invoice = models.ForeignKey(to=ForeignInvoice,
                                on_delete=models.CASCADE)
    reference = models.CharField(verbose_name='Referencia del pago',
                                 max_length=20)
    amount = models.DecimalField(verbose_name='Monto pagado', max_digits=8,
                                 decimal_places=2)
    payment_method = models.CharField(verbose_name='Método de pago',
                                      choices=PAYMENT_METHOD_CHOICES,
                                      max_length=1)
    payment_date = models.DateField(verbose_name='Fecha del pago')
