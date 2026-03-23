import hashlib
import json

from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from webauthn import (
    generate_authentication_options,
    generate_registration_options,
    options_to_json,
    verify_authentication_response,
    verify_registration_response,
)
from webauthn.helpers import base64url_to_bytes, bytes_to_base64url
from webauthn.helpers.structs import (
    AuthenticationCredential,
    AuthenticatorAssertionResponse,
    AuthenticatorAttachment,
    AuthenticatorAttestationResponse,
    AuthenticatorSelectionCriteria,
    PublicKeyCredentialDescriptor,
    RegistrationCredential,
    ResidentKeyRequirement,
    UserVerificationRequirement,
)

from core.models import WebAuthnCredential

# ─────────────────────────────────────────────
#  ENREGISTREMENT  (Register Face ID)
# ─────────────────────────────────────────────


class WebAuthnRegisterBeginView(APIView):
    """
    Étape 1 – Enregistrement :
    Génère les options WebAuthn (challenge + config authenticator).
    L'utilisateur DOIT être déjà connecté avec son mot de passe.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        # Exclure les credentials déjà enregistrés pour éviter les doublons
        existing = WebAuthnCredential.objects.filter(user=user)
        exclude_credentials = [
            PublicKeyCredentialDescriptor(id=base64url_to_bytes(c.credential_id))
            for c in existing
        ]

        options = generate_registration_options(
            rp_id=settings.WEBAUTHN_RP_ID,
            rp_name=settings.WEBAUTHN_RP_NAME,
            user_id=str(user.id).encode("utf-8"),
            user_name=user.username,
            user_display_name=(
                f"{user.first_name} {user.last_name}".strip() or user.username
            ),
            authenticator_selection=AuthenticatorSelectionCriteria(
                # PLATFORM → Face ID / Touch ID / Windows Hello (biométrie locale)
                authenticator_attachment=AuthenticatorAttachment.PLATFORM,
                user_verification=UserVerificationRequirement.REQUIRED,
                resident_key=ResidentKeyRequirement.PREFERRED,
            ),
            exclude_credentials=exclude_credentials,
        )

        # Stocker le challenge en cache pendant 2 minutes
        cache.set(
            f"webauthn_reg_{user.id}",
            bytes_to_base64url(options.challenge),
            120,
        )

        return Response(json.loads(options_to_json(options)), status=status.HTTP_200_OK)


class WebAuthnRegisterCompleteView(APIView):
    """
    Étape 2 – Enregistrement :
    Vérifie la réponse de l'appareil et sauvegarde la clé publique en BDD.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        # Récupérer le challenge stocké
        challenge_b64 = cache.get(f"webauthn_reg_{user.id}")
        if not challenge_b64:
            return Response(
                {
                    "error": (
                        "Challenge expiré ou introuvable. "
                        "Veuillez recommencer l'enregistrement."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        expected_challenge = base64url_to_bytes(challenge_b64)

        try:
            data = request.data

            credential = RegistrationCredential(
                id=data.get("id"),
                raw_id=base64url_to_bytes(data.get("rawId", data.get("id", ""))),
                response=AuthenticatorAttestationResponse(
                    client_data_json=base64url_to_bytes(
                        data["response"]["clientDataJSON"]
                    ),
                    attestation_object=base64url_to_bytes(
                        data["response"]["attestationObject"]
                    ),
                ),
                type=data.get("type", "public-key"),
            )

            verification = verify_registration_response(
                credential=credential,
                expected_challenge=expected_challenge,
                expected_rp_id=settings.WEBAUTHN_RP_ID,
                expected_origin=settings.WEBAUTHN_ORIGIN,
                require_user_verification=True,
            )

        except Exception as exc:
            return Response(
                {"error": f"Vérification échouée : {str(exc)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        device_name = request.data.get("device_name", "Face ID / Biometric")

        WebAuthnCredential.objects.create(
            user=user,
            credential_id=bytes_to_base64url(verification.credential_id),
            public_key=bytes_to_base64url(verification.credential_public_key),
            sign_count=verification.sign_count,
            aaguid=str(verification.aaguid) if verification.aaguid else "",
            device_name=device_name,
        )

        # Nettoyer le cache
        cache.delete(f"webauthn_reg_{user.id}")

        return Response(
            {"message": f"✅ Face ID '{device_name}' enregistré avec succès !"},
            status=status.HTTP_201_CREATED,
        )


# ─────────────────────────────────────────────
#  AUTHENTIFICATION  (Login Face ID)
# ─────────────────────────────────────────────


class WebAuthnLoginBeginView(APIView):
    """
    Étape 1 – Authentification :
    Génère un challenge pour l'utilisateur identifié par email ou username.
    Endpoint public (pas besoin d'être connecté).
    """

    permission_classes = [AllowAny]

    def post(self, request):
        identifier = request.data.get("email") or request.data.get("username")
        if not identifier:
            return Response(
                {"error": "Champ 'email' ou 'username' requis."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Résoudre l'utilisateur (email ou username)
        try:
            if "@" in identifier:
                user = User.objects.get(email=identifier)
            else:
                user = User.objects.get(username=identifier)
        except User.DoesNotExist:
            return Response(
                {"error": "Utilisateur introuvable."},
                status=status.HTTP_404_NOT_FOUND,
            )

        credentials = WebAuthnCredential.objects.filter(user=user)
        if not credentials.exists():
            return Response(
                {
                    "error": (
                        "Aucun Face ID enregistré pour cet utilisateur. "
                        "Connectez-vous avec votre mot de passe puis enregistrez votre Face ID."
                    )
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        allow_credentials = [
            PublicKeyCredentialDescriptor(id=base64url_to_bytes(c.credential_id))
            for c in credentials
        ]

        options = generate_authentication_options(
            rp_id=settings.WEBAUTHN_RP_ID,
            allow_credentials=allow_credentials,
            user_verification=UserVerificationRequirement.REQUIRED,
        )

        # Stocker challenge + mapping identifier → user_id en cache (2 min)
        cache.set(
            f"webauthn_auth_{user.id}",
            bytes_to_base64url(options.challenge),
            120,
        )
        cache.set(f"webauthn_auth_uid_{identifier}", user.id, 120)

        return Response(json.loads(options_to_json(options)), status=status.HTTP_200_OK)


class WebAuthnLoginCompleteView(APIView):
    """
    Étape 2 – Authentification :
    Vérifie la signature biométrique de l'appareil.
    Retourne les tokens JWT en cas de succès.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        identifier = request.data.get("email") or request.data.get("username")
        if not identifier:
            return Response(
                {"error": "Champ 'email' ou 'username' requis."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Retrouver l'utilisateur via le cache
        user_id = cache.get(f"webauthn_auth_uid_{identifier}")
        if not user_id:
            return Response(
                {"error": "Session expirée. Veuillez recommencer l'authentification."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "Utilisateur introuvable."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Récupérer le challenge
        challenge_b64 = cache.get(f"webauthn_auth_{user.id}")
        if not challenge_b64:
            return Response(
                {"error": "Challenge expiré. Veuillez recommencer l'authentification."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        expected_challenge = base64url_to_bytes(challenge_b64)

        # Retrouver le credential stocké en BDD via le hash SHA-256 (compatible MySQL)
        credential_id_b64 = request.data.get("id")
        if not credential_id_b64:
            return Response(
                {"error": "Champ 'id' (credential_id) manquant dans la requête."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        credential_hash = hashlib.sha256(credential_id_b64.encode("utf-8")).hexdigest()
        try:
            stored = WebAuthnCredential.objects.get(
                user=user, credential_id_hash=credential_hash
            )
        except WebAuthnCredential.DoesNotExist:
            return Response(
                {"error": "Credential inconnu ou non autorisé."},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            data = request.data

            credential = AuthenticationCredential(
                id=data.get("id"),
                raw_id=base64url_to_bytes(data.get("rawId", data.get("id", ""))),
                response=AuthenticatorAssertionResponse(
                    client_data_json=base64url_to_bytes(
                        data["response"]["clientDataJSON"]
                    ),
                    authenticator_data=base64url_to_bytes(
                        data["response"]["authenticatorData"]
                    ),
                    signature=base64url_to_bytes(data["response"]["signature"]),
                    user_handle=(
                        base64url_to_bytes(data["response"]["userHandle"])
                        if data["response"].get("userHandle")
                        else None
                    ),
                ),
                type=data.get("type", "public-key"),
            )

            verification = verify_authentication_response(
                credential=credential,
                expected_challenge=expected_challenge,
                expected_rp_id=settings.WEBAUTHN_RP_ID,
                expected_origin=settings.WEBAUTHN_ORIGIN,
                credential_public_key=base64url_to_bytes(stored.public_key),
                credential_current_sign_count=stored.sign_count,
                require_user_verification=True,
            )

        except Exception as exc:
            return Response(
                {"error": f"Authentification échouée : {str(exc)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Mettre à jour le compteur de signature (sécurité replay-attack)
        stored.sign_count = verification.new_sign_count
        stored.last_used_at = timezone.now()
        stored.save(update_fields=["sign_count", "last_used_at"])

        # Nettoyer le cache
        cache.delete(f"webauthn_auth_{user.id}")
        cache.delete(f"webauthn_auth_uid_{identifier}")

        # Générer les tokens JWT (même format que le LoginView existant)
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "message": "✅ Authentification Face ID réussie !",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                },
            },
            status=status.HTTP_200_OK,
        )


# ─────────────────────────────────────────────
#  GESTION DES CREDENTIALS
# ─────────────────────────────────────────────


class WebAuthnCredentialListView(APIView):
    """
    GET  → Liste tous les credentials Face ID de l'utilisateur connecté.
    DELETE /<pk>/ → Supprime un credential spécifique.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        credentials = WebAuthnCredential.objects.filter(user=request.user).order_by(
            "-created_at"
        )
        data = [
            {
                "id": c.id,
                "device_name": c.device_name,
                "aaguid": c.aaguid,
                "created_at": c.created_at,
                "last_used_at": c.last_used_at,
            }
            for c in credentials
        ]
        return Response(data, status=status.HTTP_200_OK)

    def delete(self, request, pk=None):
        if pk is None:
            return Response(
                {"error": "ID du credential requis."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            cred = WebAuthnCredential.objects.get(pk=pk, user=request.user)
            device_name = cred.device_name
            cred.delete()
            return Response(
                {"message": f"🗑️ Credential '{device_name}' supprimé avec succès."},
                status=status.HTTP_200_OK,
            )
        except WebAuthnCredential.DoesNotExist:
            return Response(
                {"error": "Credential introuvable ou non autorisé."},
                status=status.HTTP_404_NOT_FOUND,
            )
