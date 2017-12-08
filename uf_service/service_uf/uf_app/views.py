from uf_app.models import UF
from uf_app.serializers import UFSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.db import transaction


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
        amount = int(request.query_params['value'])
        uf = self.get_object(date)
        clp = uf.getCLP(amount)
        return Response(float(clp))

