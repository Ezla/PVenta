from decimal import Decimal
from rest_framework import serializers
from .models import SalesAccount, SalesProduct
from .validators import validateAccount


class SalesAccountSerialiser(serializers.ModelSerializer):
    class Meta:
        model = SalesAccount
        fields = (
            'pk', 'ticket', 'subtotal', 'cash', 'change_due', 'discount')

    def validate(self, data):
        errors = validateAccount(dict(data))

        if errors:
            raise serializers.ValidationError(errors)
        return data


class ChangeProductSerialiser(serializers.Serializer):
    code = serializers.CharField()
    quantity = serializers.DecimalField(max_digits=8, decimal_places=2)
    with_discount = serializers.BooleanField()

    def validate_quantity(self, value):
        if not value % Decimal(0.5) == Decimal(0):
            msg = 'Solo se aceptan multiplos de 0.5'
            raise serializers.ValidationError(msg)
        return value


class SalesProductSerialiser(serializers.ModelSerializer):
    price_up = serializers.DecimalField(max_digits=8, decimal_places=2)
    price_down = serializers.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        model = SalesProduct
        fields = (
            'code', 'name', 'with_discount', 'price', 'quantity',
            'sales_account', 'price_up', 'price_down')


class SalesCartSerialiser(SalesProductSerialiser):
    price_up = serializers.DecimalField(max_digits=8, decimal_places=2,
                                        read_only=True)
    price_down = serializers.DecimalField(max_digits=8, decimal_places=2,
                                          read_only=True)
