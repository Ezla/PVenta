from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models


class Discount(models.Model):
    percentage = models.PositiveSmallIntegerField(unique=True)

    def __str__(self):
        return 'Descuento del {}%'.format(self.percentage)

    def clean(self):
        if self.percentage > 100:
            msg = 'Este campo no puede contener numeros mayores a 100.'
            raise ValidationError({'descuento': msg})


class SalesAccount(models.Model):
    ticket = models.CharField(max_length=30, blank=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    cash = models.DecimalField(max_digits=10, decimal_places=2)
    change_due = models.DecimalField(max_digits=8, decimal_places=2)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ticket

    @property
    def discount_amount(self):
        return (self.subtotal * Decimal(
            self.discount.percentage)) / Decimal(100)

    @property
    def total(self):
        return self.subtotal - self.discount_amount


class SalesProduct(models.Model):
    code = models.CharField(max_length=48)
    name = models.CharField(max_length=100)
    with_discount = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField()
    sales_account = models.ForeignKey(SalesAccount,
                                      on_delete=models.CASCADE,
                                      related_name='products',
                                      blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def total(self):
        return self.price * self.quantity
