from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth.models import User

from core.serializers import UserDetailSerializer


class KeepAliveView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return Response({"status": "alive"})


@api_view(['GET'])
def get_all_users(request):
    try:
        users = User.objects.all()
        serializer = UserDetailSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


