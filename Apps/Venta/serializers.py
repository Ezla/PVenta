from rest_framework import serializers
from .models import SalesProduct


class SalesProductSerialiser(serializers.ModelSerializer):
    price_up = serializers.DecimalField(max_digits=8, decimal_places=2,)
    price_down = serializers.DecimalField(max_digits=8, decimal_places=2,)

    class Meta:
        model = SalesProduct
        fields = (
        'code', 'name', 'with_discount', 'price', 'quantity', 'sales_account', 'price_up', 'price_down')
