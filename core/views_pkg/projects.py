from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
import os
from django.core.files.storage import default_storage

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

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_destroy(self, instance):
        if instance.image and default_storage.exists(instance.image.path):
            os.remove(instance.image.path)
        instance.delete()


