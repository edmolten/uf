from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from uf_app.serializers import UserSerializer, GroupSerializer
from uf_app.models import UF
from uf_app.serializers import UFSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics

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


class UFList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    # TODO, allways get a list of ufs to add
    def post(self, request, format=None):
        serializer = UFSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UFtoCLP(APIView):

    def get_object(self, pk):
        try:
            return UF.objects.get(pk=pk)
        except UF.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        date = request.GET('date')
        value = request.GET('value')
        uf = self.get_object(date)
        clp = uf.getCLP(value)
        return Response(clp)

