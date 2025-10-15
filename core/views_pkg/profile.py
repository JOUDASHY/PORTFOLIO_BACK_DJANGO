from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.exceptions import NotFound

from core.models import Profile
from core.serializers import ProfileSerializer


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile, created = Profile.objects.get_or_create(user=request.user)
            user_data = {"username": request.user.username, "email": request.user.email}
            profile_data = ProfileSerializer(profile).data
            response_data = {**user_data, **profile_data}
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        try:
            profile = request.user.profile
            old_image_path = profile.image.path if profile.image else None
            serializer = ProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                new_image_path = profile.image.path if profile.image else None
                if old_image_path and old_image_path != new_image_path:
                    from django.core.files.storage import default_storage
                    default_storage.delete(old_image_path)
                return Response({"message": "Profil mis à jour avec succès", "data": serializer.data}, status=status.HTTP_200_OK)
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Profile.DoesNotExist:
            return Response({"error": "Profil introuvable"}, status=status.HTTP_404_NOT_FOUND)


class NilsenProfileView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        try:
            user = User.objects.get(id=1)
        except User.DoesNotExist:
            raise NotFound("User with id=1 does not exist.")

        data = {
            "username": user.username,
            "email": user.email,
            "id": user.id,
            "image": user.profile.image.url if hasattr(user, 'profile') and user.profile.image else None,
            "about": getattr(user.profile, 'about', 'No description available'),
            "date_of_birth": getattr(user.profile, 'date_of_birth', None),
            "link_facebook": getattr(user.profile, 'link_facebook', None),
            "link_github": getattr(user.profile, 'link_github', None),
            "link_linkedin": getattr(user.profile, 'link_linkedin', None),
            "phone_number": getattr(user.profile, 'phone_number', None),
            "address": getattr(user.profile, 'address', None),
        }
        return Response(data, status=status.HTTP_200_OK)


