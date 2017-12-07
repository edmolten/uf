from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from uf_app.serializers import UserSerializer, GroupSerializer
from uf_app.models import UF
from uf_app.serializers import UFSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.db import transaction

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class UFList(generics.ListCreateAPIView):
    queryset = UF.objects.all()
    serializer_class = UFSerializer


class UFCreateMany(APIView):
    def post(self, request):
        serializer = UFSerializer(data=request.data, many=True)
        if serializer.is_valid():
            self.save_all(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def save_all(self, data):
        for uf in data:
            entry = UF(date=uf['date'], value=uf['value'])
            entry.save()


class UFtoCLP(APIView):

    @staticmethod
    def get_object(pk):
        try:
            return UF.objects.get(pk=pk)
        except UF.DoesNotExist:
            raise Http404

    def get(self, request):
        date = request.query_params['date']
        value = int(request.query_params['value'])
        uf = self.get_object(date)
        clp = uf.getCLP(value)
        return Response(clp)

