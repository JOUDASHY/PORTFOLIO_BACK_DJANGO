from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import MyLogin
from core.serializers import MyLoginSerializer


class MyLoginViewSet(viewsets.ModelViewSet):
    queryset = MyLogin.objects.all()
    serializer_class = MyLoginSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        logins = self.get_queryset().order_by('site')
        serializer = self.get_serializer(logins, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


