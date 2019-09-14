from rest_framework import serializers
from .models import Listed


class ListedSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Listed
        fields = (
            'pk', 'name', 'number', 'type', 'reference_number', 'provider',
            'active')
