from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from core.models import Experience
from core.serializers import ExperienceSerializer


class ExperienceViewSet(viewsets.ModelViewSet):
    queryset = Experience.objects.all().order_by('-date_fin')
    serializer_class = ExperienceSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        return [IsAuthenticated()]


