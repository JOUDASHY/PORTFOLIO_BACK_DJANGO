from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.conf import settings
from django.core.mail import send_mail

from core.serializers import UserRegistrationSerializer, PasswordResetRequestSerializer, PasswordResetSerializer
from core.models import Profile


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            Profile.objects.get_or_create(user=user)
            refresh = RefreshToken.for_user(user)
            return Response({
                'username': user.username,
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'message': 'User registered successfully!'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)

        user = authenticate(username=user.username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "message": "Login successful!",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        if not user.check_password(old_password):
            return Response({"error": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response({"error": "New password and confirm password do not match."}, status=status.HTTP_400_BAD_REQUEST)

        if len(new_password) < 8:
            return Response({"error": "New password must be at least 8 characters long."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({"message": "Password changed successfully!"}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            return Response({'status': 'success', 'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'error', 'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                refresh = RefreshToken.for_user(user)
                token = str(refresh.access_token)
                frontend_base_url = settings.FRONTEND_BASE_URL
                reset_url = f"{frontend_base_url}/password-reset/{token}?email={email}"
                send_mail(
                    subject="Réinitialisation de votre mot de passe",
                    message=f"Utilisez ce lien pour réinitialiser votre mot de passe : {reset_url}",
                    from_email="noreply@example.com",
                    recipient_list=[email],
                )
                return Response({"message": "Email envoyé pour la réinitialisation."}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "Utilisateur introuvable avec cet email."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


import jwt
from datetime import datetime


class PasswordResetConfirmView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']
            try:
                decoded_token = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
                exp = datetime.utcfromtimestamp(decoded_token['exp'])
                if exp < datetime.utcnow():
                    return Response({"error": "Token expiré."}, status=status.HTTP_400_BAD_REQUEST)
                user_id = decoded_token['user_id']
                user = User.objects.get(id=user_id)
                user.set_password(new_password)
                user.save()
                return Response({"message": "Mot de passe réinitialisé avec succès."}, status=status.HTTP_200_OK)
            except jwt.ExpiredSignatureError:
                return Response({"error": "Token expiré."}, status=status.HTTP_400_BAD_REQUEST)
            except jwt.DecodeError:
                return Response({"error": "Token invalide."}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({"error": "Utilisateur non trouvé."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


