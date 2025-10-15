from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from core.models import Award
from core.serializers import AwardSerializer


class AwardViewSet(viewsets.ModelViewSet):
    queryset = Award.objects.all()
    serializer_class = AwardSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        return [IsAuthenticated()]


