from rest_framework import serializers
from .models import Listed


class ListedSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Listed
        fields = (
            'pk', 'name', 'number', 'type', 'reference_number', 'provider',
            'active')

    def validate(self, data):
        # Validate reference_number:
        # Obteneomos los campos enviados  para validar referencia
        reference_number = data.get('reference_number')
        provider = data.get('provider')
        type = data.get('type')
        # instance_pk None nos indica que es un nuevo registro (post)
        instance_pk = None
        # Si es una actualizacion obtenemos el id de la instancia a
        # actualizar
        if not self.instance is None:
            instance_pk = self.instance.pk
        try:
            # Comprobamos si hay algun producto existente con esa
            # referencia asociada a ese provedor y que sea el mismo tipo
            # de producto y obtenemos su id.
            listed = Listed.objects.get(reference_number=reference_number,
                                        provider=provider, type=type)
            listed_pk = listed.pk
            # Si la ID de la isntancia a actualizar es direfente que la del
            # egistro que tiene coincidencias, indicamos que ya esta registrada
            # esa referencia.
            if instance_pk != listed_pk:
                for key, value in Listed.PROVIDERS_CHOICES:
                    if key == provider:
                        provider = value
                        break
                msg = 'La referencia "{}" asociada al proveedor "{}" ya esta registrada.'.format(
                    reference_number, provider)
                raise serializers.ValidationError(
                    {'reference_number': msg})
        except Listed.DoesNotExist:
            # No existe producto con referencia igual
            pass
        return data
