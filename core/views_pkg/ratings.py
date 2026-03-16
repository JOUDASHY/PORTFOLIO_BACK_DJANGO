from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg

from core.models import Rating


class RatingView(APIView):
    def post(self, request):
        project_id = request.data.get('project_id')
        score = request.data.get('score')
        ip_address = self.get_client_ip(request)

        # Validate score
        if not score or score < 1 or score > 5:
            return Response(
                {"message": "Le score doit être entre 1 et 5."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Use update_or_create to handle unique constraint
        rating, created = Rating.objects.update_or_create(
            project_id=project_id,
            ip_address=ip_address,
            defaults={'score': score}
        )
        
        if created:
            return Response({
                "message": "Merci pour votre note !", 
                "score": rating.score, 
                "ip_address": ip_address,
                "updated": False
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "message": "Votre note a été mise à jour !", 
                "score": rating.score, 
                "ip_address": ip_address,
                "updated": True
            }, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request, project_id):
        ratings = Rating.objects.filter(project_id=project_id)
        average_score = ratings.aggregate(Avg('score'))['score__avg']
        ratings_count = ratings.count()
        ratings_details = list(ratings.values('score', 'ip_address'))
        return Response({
            "project_id": project_id,
            "average_score": round(average_score or 0, 2),
            "ratings_count": ratings_count,
            "ratings_details": ratings_details
        })

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')


