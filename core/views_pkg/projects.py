from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.conf import settings
import os

from core.models import Projet, ImageProjet
from core.serializers import ProjetSerializer, ImageProjetSerializer


class ProjetViewSet(viewsets.ModelViewSet):
    queryset = Projet.objects.all()
    serializer_class = ProjetSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        return [IsAuthenticated()]


class ImageProjetViewSet(viewsets.ModelViewSet):
    queryset = ImageProjet.objects.all()
    serializer_class = ImageProjetSerializer

    def destroy(self, request, pk=None):
        image_projet = ImageProjet.objects.filter(pk=pk).first()
        if image_projet:
            if image_projet.image:
                image_path = os.path.join(settings.MEDIA_ROOT, str(image_projet.image))
                if os.path.exists(image_path):
                    os.remove(image_path)
            image_projet.delete()
        return Response({"message": "Image supprimée avec succès."}, status=status.HTTP_204_NO_CONTENT)


