from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
import os
from django.core.files.storage import default_storage

from core.models import Projet, ImageProjet
from core.serializers import ProjetSerializer, ImageProjetSerializer


class ProjetViewSet(viewsets.ModelViewSet):
    """
    ViewSet CRUD pour les projets du portfolio.

    Endpoints standards (ModelViewSet) :
        GET    /api/projets/              Liste tous les projets          [public]
        POST   /api/projets/              Crée un projet                  [auth]
        GET    /api/projets/{id}/         Détail d'un projet              [public]
        PUT    /api/projets/{id}/         Mise à jour complète            [auth]
        PATCH  /api/projets/{id}/         Mise à jour partielle           [auth]
        DELETE /api/projets/{id}/         Supprime un projet              [auth]

    Endpoints custom :
        GET    /api/projets/featured/           Projets marqués is_featured=True  [public]
        PATCH  /api/projets/{id}/toggle-featured/  Bascule is_featured True<->False  [auth]

    Champ is_featured :
        Booléen (défaut False). Quand True, le projet apparaît dans les
        templates de prospection (premier contact). Peut être passé dans
        le body lors du create ou update :
            { "nom": "...", "is_featured": true, ... }
    """

    queryset = Projet.objects.all()
    serializer_class = ProjetSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve', 'featured'):
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['get'], url_path='featured')
    def featured(self, request):
        """
        Retourne uniquement les projets marqués is_featured=True.
        Utilisé par les templates de prospection pour afficher des exemples de réalisations.
        """
        projets = Projet.objects.filter(is_featured=True)
        serializer = self.get_serializer(projets, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'], url_path='toggle-featured')
    def toggle_featured(self, request, pk=None):
        """
        Bascule is_featured d'un projet (True -> False ou False -> True).
        Réponse : { "id": <int>, "is_featured": <bool> }
        """
        projet = self.get_object()
        projet.is_featured = not projet.is_featured
        projet.save()
        return Response({'id': projet.id, 'is_featured': projet.is_featured})


class ImageProjetViewSet(viewsets.ModelViewSet):
    """
    ViewSet CRUD pour les images associées aux projets.

    Endpoints :
        GET    /api/images-projet/          Liste toutes les images     [public]
        POST   /api/images-projet/          Ajoute une image            [auth]
        GET    /api/images-projet/{id}/     Détail                      [auth]
        PUT    /api/images-projet/{id}/     Mise à jour                 [auth]
        DELETE /api/images-projet/{id}/     Supprime (fichier inclus)   [auth]

    La suppression efface aussi le fichier physique du disque.
    """

    queryset = ImageProjet.objects.all()
    serializer_class = ImageProjetSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_destroy(self, instance):
        """Supprime le fichier image du disque avant de supprimer l'entrée BDD."""
        if instance.image and default_storage.exists(instance.image.path):
            os.remove(instance.image.path)
        instance.delete()
