from rest_framework.serializers import ModelSerializer
from uf_app.models import UF
from uf_app.constants import *


class UFSerializer(ModelSerializer):
    class Meta:
        model = UF
        fields = (DATE_FIELD, VALUE_FIELD)
