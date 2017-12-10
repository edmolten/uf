from django.http import Http404
from uf_app.models import UF
from uf_app.serializers import UFSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from uf_app.constants import *


class UFList(APIView):
    def get(self, _):
        data = UF.objects.all()
        serializer = UFSerializer(data, many=True)
        return Response(serializer.data)


class UFCreateMany(APIView):
    def post(self, request):
        data = UF.filter(request.data)
        serializer = UFSerializer(data=data, many=True)
        if serializer.is_valid():
            self.save_all(serializer.data)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def save_all(self, data):
        for uf in data:
            entry = UF(date=uf[DATE_FIELD],
                       value=uf[VALUE_FIELD])
            entry.save()


class UFtoCLP(APIView):
    def get(self, request):
        date = request.query_params[DATE_FIELD]
        amount = int(request.query_params[VALUE_FIELD])
        uf = UF.get(date)
        if uf:
            clp = uf.get_price(amount)
            return Response(float(clp))
        else:
            raise Http404

