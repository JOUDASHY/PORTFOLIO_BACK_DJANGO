from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import FileResponse
from django.shortcuts import get_object_or_404

from core.models import CV
from core.serializers import CVSerializer


class CVView(APIView):
    """
    API View for CV upload and download
    - GET: Download the active CV (public)
    - POST: Upload a new CV (authenticated only)
    - PUT/PATCH: Update the active CV (authenticated only)
    """

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request):
        """Get the active CV info or download it"""
        cv = CV.objects.filter(is_active=True).first()
        
        # If no active CV but CVs exist, activate the most recent one
        if not cv:
            cv = CV.objects.order_by('-uploaded_at').first()
            if cv:
                cv.is_active = True
                cv.save()
        
        # Check if user wants to download the file
        download = request.query_params.get('download', 'false').lower() == 'true'
        
        if download:
            if not cv:
                return Response(
                    {"detail": "No CV available for download. Please upload a CV first."},
                    status=status.HTTP_404_NOT_FOUND
                )
            return FileResponse(
                cv.file.open(),
                as_attachment=True,
                filename='CV_Eddy_Nilsen.pdf'
            )
        
        # Return CV info or empty state
        if not cv:
            return Response({
                "id": None,
                "file": None,
                "file_url": None,
                "uploaded_at": None,
                "is_active": False,
                "message": "No CV uploaded yet. Use POST /api/cv/ to upload a CV."
            })
        
        serializer = CVSerializer(cv, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        """Upload a new CV"""
        # Check if file is provided
        if 'file' not in request.FILES:
            return Response(
                {"detail": "No file provided."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        file = request.FILES['file']
        
        # Validate file type
        if not file.name.endswith('.pdf'):
            return Response(
                {"detail": "Only PDF files are allowed."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = CVSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(is_active=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """Update the active CV (replace it)"""
        cv = CV.objects.filter(is_active=True).first()
        
        if not cv:
            # If no active CV, create a new one
            return self.post(request)
        
        # Check if file is provided
        if 'file' not in request.FILES:
            return Response(
                {"detail": "No file provided."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        file = request.FILES['file']
        
        # Validate file type
        if not file.name.endswith('.pdf'):
            return Response(
                {"detail": "Only PDF files are allowed."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Delete old file
        if cv.file:
            cv.file.delete(save=False)
        
        serializer = CVSerializer(cv, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CVListView(APIView):
    """
    List all CVs (authenticated only)
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get list of all CVs"""
        cvs = CV.objects.all().order_by('-uploaded_at')
        serializer = CVSerializer(cvs, many=True, context={'request': request})
        return Response(serializer.data)
