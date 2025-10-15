import os
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.core.files.storage import default_storage

from core.models import Education
from core.serializers import EducationSerializer


class EducationViewSet(viewsets.ModelViewSet):
    queryset = Education.objects.all().order_by('-annee_fin')
    serializer_class = EducationSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        return [IsAuthenticated()]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        old_image = instance.image
        new_image = request.data.get('image')
        response = super().update(request, *args, **kwargs)
        if new_image and old_image and old_image.name != new_image:
            if default_storage.exists(old_image.path):
                os.remove(old_image.path)
        return response

    def perform_destroy(self, instance):
        if instance.image and default_storage.exists(instance.image.path):
            os.remove(instance.image.path)
        instance.delete()


