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
