from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from core.models import Langue
from core.serializers import LangueSerializer


class LangueViewSet(viewsets.ModelViewSet):
    queryset = Langue.objects.all()
    serializer_class = LangueSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        return [IsAuthenticated()]


