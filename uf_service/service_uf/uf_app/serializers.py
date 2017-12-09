from rest_framework.serializers import ModelSerializer
from uf_app.models import UF


class UFSerializer(ModelSerializer):

    class Meta:
        model = UF
        fields = ('date', 'value')
