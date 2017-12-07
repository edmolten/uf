from rest_framework import serializers
from uf_app.models import UF


class UFSerializer(serializers.ModelSerializer):
    class Meta:
        model = UF
        fields = ('date', 'value')
