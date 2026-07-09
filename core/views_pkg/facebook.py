# Ce fichier est conservé pour compatibilité des imports existants.
# Les nouvelles views sont dans hack.py (ClientHackView, HackSubmitView, etc.)
# FacebookList, FacebookByTokenView, FacebookSubmitView sont des alias vides
# pour ne pas casser les imports dans urls.py et api/__init__.py.

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class FacebookList(APIView):
    """Ancienne view — remplacée par ClientHackView dans hack.py"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"detail": "Utiliser /hack/clients/ à la place."}, status=status.HTTP_410_GONE)

    def post(self, request):
        return Response({"detail": "Utiliser /hack/clients/ à la place."}, status=status.HTTP_410_GONE)

    def delete(self, request, pk=None):
        return Response({"detail": "Utiliser /hack/clients/<id>/ à la place."}, status=status.HTTP_410_GONE)


class FacebookByTokenView(APIView):
    """Ancienne view — remplacée par HackSubmitView dans hack.py"""
    permission_classes = [AllowAny]

    def get(self, request, token=None):
        return Response({"detail": "Utiliser /hack/<token>/submit/ à la place."}, status=status.HTTP_410_GONE)


class FacebookSubmitView(APIView):
    """Ancienne view — remplacée par HackSubmitView dans hack.py"""
    permission_classes = [AllowAny]

    def post(self, request, token=None):
        return Response({"detail": "Utiliser /hack/<token>/submit/ à la place."}, status=status.HTTP_410_GONE)
