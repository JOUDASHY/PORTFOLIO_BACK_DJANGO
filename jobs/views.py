from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Prospect

from .models import JobOffer, JobSearchQuery
from .serializers import (
    JobOfferSerializer,
    JobSearchQuerySerializer,
    RunSearchSerializer,
)
from .services import run_search


class JobOfferViewSet(viewsets.ModelViewSet):
    """Liste / détail / mise à jour du statut des offres collectées.

    Filtres : ?status= &source= &remote=true &search=mot
    Seul le champ `status` est modifiable (PATCH).
    """

    serializer_class = JobOfferSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "patch", "delete", "head", "options"]

    def get_queryset(self):
        qs = JobOffer.objects.all()
        params = self.request.query_params
        if params.get("status"):
            qs = qs.filter(status=params["status"])
        if params.get("source"):
            qs = qs.filter(source=params["source"])
        if params.get("remote") in ("true", "1"):
            qs = qs.filter(is_remote=True)
        search = params.get("search")
        if search:
            qs = qs.filter(
                Q(title__icontains=search)
                | Q(company__icontains=search)
                | Q(location__icontains=search)
            )
        return qs

    @action(detail=True, methods=["post"], url_path="to-prospect")
    def to_prospect(self, request, pk=None):
        """Convertit une offre en Prospect (réutilise le CRM existant)."""
        offer = self.get_object()
        if offer.prospect_id:
            return Response(
                {"detail": "Offre déjà convertie.", "prospect_id": offer.prospect_id},
                status=status.HTTP_200_OK,
            )
        prospect = Prospect.objects.create(
            company_name=offer.company or offer.title[:255],
            website_url=offer.url[:200] if offer.url else "",
            source="other",
            notes=f"Offre importée ({offer.get_source_display()})\n"
                  f"Poste : {offer.title}\n"
                  f"Lieu : {offer.location}\n"
                  f"Lien : {offer.url}",
        )
        offer.prospect = prospect
        offer.status = "applied" if offer.status == "new" else offer.status
        offer.save(update_fields=["prospect", "status"])
        return Response(
            {"detail": "Prospect créé.", "prospect_id": prospect.id},
            status=status.HTTP_201_CREATED,
        )


class JobSearchQueryViewSet(viewsets.ModelViewSet):
    queryset = JobSearchQuery.objects.all()
    serializer_class = JobSearchQuerySerializer
    permission_classes = [IsAuthenticated]


class RunFetchView(APIView):
    """POST /api/jobs/fetch/ — lance une collecte à la demande (synchrone)."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = RunSearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        recap = run_search(
            keywords=data["keywords"],
            location=data["location"],
            remote=data["remote"],
            sources=data["sources"] or None,
            category=data["category"],
        )
        return Response(recap, status=status.HTTP_200_OK)
