from rest_framework import serializers
from .models import ForeignInvoice


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForeignInvoice
        fields = ('__all__')
