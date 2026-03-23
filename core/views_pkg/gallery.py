import os

from django.core.files.storage import default_storage
from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from core.models import GalleryCategory, GalleryImage
from core.serializers import GalleryCategorySerializer, GalleryImageSerializer


class GalleryCategoryViewSet(viewsets.ModelViewSet):
    """
    CRUD complet pour les catégories de la galerie.
    - Lecture  : public
    - Écriture : authentifié
    """

    serializer_class = GalleryCategorySerializer

    def get_queryset(self):
        return GalleryCategory.objects.all().order_by("name")

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [AllowAny()]
        return [IsAuthenticated()]

    # ------------------------------------------------------------------ #
    #  GET /api/gallery/categories/<pk>/images/                           #
    #  Toutes les images d'une catégorie donnée                           #
    # ------------------------------------------------------------------ #
    @action(
        detail=True, methods=["get"], url_path="images", permission_classes=[AllowAny]
    )
    def images(self, request, pk=None):
        category = self.get_object()
        qs = GalleryImage.objects.filter(category=category).order_by(
            "order", "-created_at"
        )
        serializer = GalleryImageSerializer(qs, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class GalleryImageViewSet(viewsets.ModelViewSet):
    """
    CRUD complet pour les images de la galerie.

    Paramètres de filtre (query params) :
        ?category=<id>       → filtre par catégorie
        ?featured=true       → uniquement les images mises en avant
        ?search=<texte>      → recherche dans title / description / tags
        ?ordering=order      → tri (order, -created_at, title …)
    """

    serializer_class = GalleryImageSerializer

    def get_queryset(self):
        qs = GalleryImage.objects.select_related("category").order_by(
            "order", "-created_at"
        )

        # ── Filtre par catégorie ──────────────────────────────────────
        category_id = self.request.query_params.get("category")
        if category_id:
            qs = qs.filter(category_id=category_id)

        # ── Filtre featured ──────────────────────────────────────────
        featured = self.request.query_params.get("featured", "").lower()
        if featured == "true":
            qs = qs.filter(is_featured=True)

        # ── Recherche fulltext ───────────────────────────────────────
        search = self.request.query_params.get("search", "").strip()
        if search:
            qs = qs.filter(
                Q(title__icontains=search)
                | Q(description__icontains=search)
                | Q(tags__icontains=search)
            )

        # ── Tri dynamique ────────────────────────────────────────────
        ordering = self.request.query_params.get("ordering", "")
        allowed_orderings = {
            "order",
            "-order",
            "created_at",
            "-created_at",
            "title",
            "-title",
        }
        if ordering in allowed_orderings:
            qs = qs.order_by(ordering)

        return qs

    def get_permissions(self):
        if self.action in ("list", "retrieve", "featured"):
            return [AllowAny()]
        return [IsAuthenticated()]

    # ------------------------------------------------------------------ #
    #  Suppression du fichier physique lors d'un DELETE                   #
    # ------------------------------------------------------------------ #
    def perform_destroy(self, instance):
        # Supprimer le fichier image du disque / storage
        if instance.image:
            try:
                if default_storage.exists(instance.image.name):
                    default_storage.delete(instance.image.name)
            except Exception:
                pass  # Ne pas bloquer si le fichier est déjà absent
        instance.delete()

    # ------------------------------------------------------------------ #
    #  GET /api/gallery/images/featured/                                  #
    #  Raccourci pour les images mises en avant                           #
    # ------------------------------------------------------------------ #
    @action(
        detail=False,
        methods=["get"],
        url_path="featured",
        permission_classes=[AllowAny],
    )
    def featured(self, request):
        qs = GalleryImage.objects.filter(is_featured=True).order_by(
            "order", "-created_at"
        )
        serializer = self.get_serializer(qs, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    # ------------------------------------------------------------------ #
    #  PATCH /api/gallery/images/<pk>/toggle_featured/                    #
    #  Basculer le statut is_featured d'une image                         #
    # ------------------------------------------------------------------ #
    @action(
        detail=True,
        methods=["patch"],
        url_path="toggle_featured",
        permission_classes=[IsAuthenticated],
    )
    def toggle_featured(self, request, pk=None):
        image = self.get_object()
        image.is_featured = not image.is_featured
        image.save(update_fields=["is_featured"])
        return Response(
            {
                "id": image.id,
                "is_featured": image.is_featured,
                "message": (
                    "✅ Image mise en avant."
                    if image.is_featured
                    else "Image retirée des favoris."
                ),
            },
            status=status.HTTP_200_OK,
        )

    # ------------------------------------------------------------------ #
    #  PATCH /api/gallery/images/<pk>/reorder/                            #
    #  Modifier l'ordre d'affichage d'une image                           #
    # ------------------------------------------------------------------ #
    @action(
        detail=True,
        methods=["patch"],
        url_path="reorder",
        permission_classes=[IsAuthenticated],
    )
    def reorder(self, request, pk=None):
        image = self.get_object()
        new_order = request.data.get("order")
        if new_order is None:
            return Response(
                {"error": "Le champ 'order' est requis."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            image.order = int(new_order)
            image.save(update_fields=["order"])
        except (ValueError, TypeError):
            return Response(
                {"error": "'order' doit être un entier."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"id": image.id, "order": image.order, "message": "✅ Ordre mis à jour."},
            status=status.HTTP_200_OK,
        )
