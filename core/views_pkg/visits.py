from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpRequest
from django.utils import timezone
from dateutil.relativedelta import relativedelta

from core.models import Visit


class MonthlyVisitStats(APIView):
    def get(self, request):
        today = timezone.now()
        current_month_start = today.replace(day=1)
        stats = []
        for i in range(12):
            month_start = current_month_start - relativedelta(months=i)
            month_end = month_start + relativedelta(months=1)
            visit_count = Visit.objects.filter(
                timestamp__gte=month_start, timestamp__lt=month_end
            ).count()
            stats.append({"month": month_start.strftime('%B %Y'), "count": visit_count})
        return Response(stats)


class RecordVisit(APIView):
    permission_classes = [AllowAny]

    def post(self, request: HttpRequest):
        ip_address = request.META.get('REMOTE_ADDR', '')
        Visit.objects.create(ip_address=ip_address)
        return Response({"message": "Visit recorded successfully"}, status=status.HTTP_201_CREATED)


class TotalVisits(APIView):
    def get(self, request):
        total_visits = Visit.objects.count()
        return Response({"total_visits": total_visits})


