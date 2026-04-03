import qrcode
import io
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User


class PortfolioQRCodeView(APIView):
    """
    Génère un QR code PNG pointant vers le lien du portfolio (FRONTEND_BASE_URL ou profile link).

    GET /api/qrcode/
        - Paramètre optionnel : ?url=https://... pour encoder une URL custom
        - Sinon utilise FRONTEND_BASE_URL depuis les settings, ou le lien_github du profil user id=1
        - Retourne une image PNG directement (Content-Type: image/png)
    """
    permission_classes = [AllowAny]

    def get(self, request):
        # Priorité : param ?url > FRONTEND_BASE_URL settings > lien profil
        url = request.query_params.get('url')

        if not url:
            from django.conf import settings
            url = getattr(settings, 'FRONTEND_BASE_URL', None)

        if not url:
            try:
                profile = User.objects.get(id=1).profile
                url = profile.link_github or ''
            except Exception:
                url = ''

        if not url:
            from rest_framework.response import Response
            from rest_framework import status
            return Response({'error': 'Aucune URL disponible pour le QR code.'}, status=status.HTTP_400_BAD_REQUEST)

        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)

        return HttpResponse(buffer, content_type='image/png')
