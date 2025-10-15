from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.models import Facebook
from core.serializers import FacebookSerializer


class FacebookList(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        if self.request.method == 'DELETE':
            return [IsAuthenticated()]
        return [AllowAny()]

    def get(self, request):
        facebook_users = Facebook.objects.all()
        serializer = FacebookSerializer(facebook_users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FacebookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            facebook_user = Facebook.objects.get(pk=pk)
            facebook_user.delete()
            return Response({"message": "Utilisateur supprimé avec succès"}, status=status.HTTP_204_NO_CONTENT)
        except Facebook.DoesNotExist:
            return Response({"error": "Utilisateur non trouvé"}, status=status.HTTP_404_NOT_FOUND)


