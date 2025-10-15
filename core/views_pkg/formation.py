from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from core.models import Formation
from core.serializers import FormationSerializer


class FormationViewSet(viewsets.ModelViewSet):
    queryset = Formation.objects.all()
    serializer_class = FormationSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        return [IsAuthenticated()]


