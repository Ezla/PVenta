from rest_framework import serializers
from .models import ForeignInvoice


class InvoiceSerializer(serializers.ModelSerializer):
    provider_name = serializers.CharField(source='provider.name',
                                          read_only=True)
    status_name = serializers.SerializerMethodField()

    class Meta:
        model = ForeignInvoice
        fields = ('__all__')

    def get_status_name(self, obj):
        return obj.get_status_display()
