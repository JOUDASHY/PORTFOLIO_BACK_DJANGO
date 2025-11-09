import os
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.exceptions import NotFound
from django.core.files.storage import default_storage

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
            profile, created = Profile.objects.get_or_create(user=request.user)
            # Save old image info before update
            old_image = profile.image
            old_image_path = None
            old_image_name = None
            if old_image:
                old_image_path = old_image.path
                old_image_name = old_image.name
            
            serializer = ProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                # Reload profile to get updated image
                profile.refresh_from_db()
                
                # Delete old image if a new one was uploaded and it's different
                if old_image_path and old_image_name:
                    new_image_name = profile.image.name if profile.image else None
                    # If image changed (new image uploaded or image was removed)
                    if old_image_name != new_image_name:
                        if default_storage.exists(old_image_path):
                            os.remove(old_image_path)
                
                return Response({"message": "Profil mis à jour avec succès", "data": serializer.data}, status=status.HTTP_200_OK)
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Une erreur s'est produite: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NilsenProfileView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        try:
            user = User.objects.get(id=1)
        except User.DoesNotExist:
            raise NotFound("User with id=1 does not exist.")

        # Use serializer to get absolute URL for image
        if hasattr(user, 'profile'):
            profile_data = ProfileSerializer(user.profile).data
            data = {
                "username": user.username,
                "email": user.email,
                "id": user.id,
                **profile_data
            }
        else:
            data = {
                "username": user.username,
                "email": user.email,
                "id": user.id,
                "image": None,
                "about": 'No description available',
                "date_of_birth": None,
                "link_facebook": None,
                "link_github": None,
                "link_linkedin": None,
                "phone_number": None,
                "address": None,
            }
        return Response(data, status=status.HTTP_200_OK)


