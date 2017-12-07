from django.contrib.auth.models import User, Group
from rest_framework import serializers
from uf_app.models import UF


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class UFSerializer(serializers.ModelSerializer):
    class Meta:
        model = UF
        fields = ('date', 'value')
