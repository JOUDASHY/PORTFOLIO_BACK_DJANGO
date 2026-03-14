from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now
from django.db.models import Sum, Count, Avg

from core.models import Prospect, ProspectNote, ProspectMessage, MessageTemplate
from core.serializers import (
    ProspectSerializer, ProspectListSerializer, ProspectNoteSerializer,
    ProspectMessageSerializer, MessageTemplateSerializer, ProspectStatsSerializer
)


class ProspectViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing prospects
    - GET: List prospects (light serializer)
    - POST: Create new prospect
    - GET /{id}/: Get prospect details (full serializer)
    - PUT /{id}/: Update prospect
    - DELETE /{id}/: Delete prospect
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Prospect.objects.all()
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by source
        source_filter = self.request.query_params.get('source')
        if source_filter:
            queryset = queryset.filter(source=source_filter)
        
        # Search by company name
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(company_name__icontains=search)
        
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProspectListSerializer
        return ProspectSerializer


class ProspectStatusView(APIView):
    """Update prospect status only"""
    permission_classes = [IsAuthenticated]
    
    def patch(self, request, pk):
        try:
            prospect = Prospect.objects.get(pk=pk)
        except Prospect.DoesNotExist:
            return Response(
                {"detail": "Prospect not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        new_status = request.data.get('status')
        if new_status not in dict(Prospect.STATUS_CHOICES).keys():
            return Response(
                {"detail": "Invalid status."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        prospect.status = new_status
        prospect.save()
        serializer = ProspectSerializer(prospect)
        return Response(serializer.data)


class ProspectStatsView(APIView):
    """Dashboard statistics for prospects"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        total = Prospect.objects.count()
        
        # Count by status
        status_counts = {}
        for status_key, _ in Prospect.STATUS_CHOICES:
            status_counts[status_key] = Prospect.objects.filter(status=status_key).count()
        
        # Calculate revenues
        estimated_revenue = Prospect.objects.filter(
            status__in=['interested', 'proposal_sent', 'negotiation']
        ).aggregate(total=Sum('estimated_value'))['total'] or 0
        
        won_revenue = Prospect.objects.filter(
            status='won'
        ).aggregate(total=Sum('estimated_value'))['total'] or 0
        
        # Conversion rate (won / total contacted)
        contacted = status_counts.get('contacted', 0) + \
                    status_counts.get('interested', 0) + \
                    status_counts.get('proposal_sent', 0) + \
                    status_counts.get('negotiation', 0) + \
                    status_counts.get('won', 0) + \
                    status_counts.get('lost', 0)
        
        if contacted > 0:
            conversion_rate = f"{(status_counts.get('won', 0) / contacted * 100):.1f}%"
        else:
            conversion_rate = "0%"
        
        # Average deal value
        avg_deal = Prospect.objects.filter(status='won').aggregate(
            avg=Avg('estimated_value')
        )['avg'] or 0
        
        data = {
            'total_prospects': total,
            **status_counts,
            'conversion_rate': conversion_rate,
            'estimated_revenue': estimated_revenue,
            'won_revenue': won_revenue,
            'average_deal_value': avg_deal,
        }
        
        serializer = ProspectStatsSerializer(data)
        return Response(serializer.data)


class ProspectNoteViewSet(viewsets.ModelViewSet):
    """ViewSet for prospect notes"""
    permission_classes = [IsAuthenticated]
    serializer_class = ProspectNoteSerializer
    
    def get_queryset(self):
        prospect_id = self.kwargs.get('prospect_pk')
        return ProspectNote.objects.filter(prospect_id=prospect_id)
    
    def perform_create(self, serializer):
        prospect_id = self.kwargs.get('prospect_pk')
        serializer.save(prospect_id=prospect_id)


class ProspectMessageView(APIView):
    """List messages for a prospect"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, prospect_id):
        try:
            prospect = Prospect.objects.get(pk=prospect_id)
        except Prospect.DoesNotExist:
            return Response(
                {"detail": "Prospect not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        messages = prospect.messages.all()
        serializer = ProspectMessageSerializer(messages, many=True)
        return Response(serializer.data)


class ProspectMessageSendView(APIView):
    """Send/Log a message to a prospect"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, prospect_id):
        try:
            prospect = Prospect.objects.get(pk=prospect_id)
        except Prospect.DoesNotExist:
            return Response(
                {"detail": "Prospect not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        template_id = request.data.get('template_id')
        subject = request.data.get('subject', '')
        body = request.data.get('body', '')
        
        # If template provided, use it
        template = None
        if template_id:
            try:
                template = MessageTemplate.objects.get(pk=template_id)
                subject = template.subject
                body = template.body
            except MessageTemplate.DoesNotExist:
                pass
        
        # Replace variables
        subject = self._replace_variables(subject, prospect)
        body = self._replace_variables(body, prospect)
        
        # Create message record
        message = ProspectMessage.objects.create(
            prospect=prospect,
            template=template,
            subject=subject,
            body=body,
            status='sent',
            sent_at=now()
        )
        
        # Update prospect status to contacted if new
        if prospect.status == 'new':
            prospect.status = 'contacted'
            prospect.save()
        
        serializer = ProspectMessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def _replace_variables(self, text, prospect):
        """Replace template variables with prospect data"""
        if not text:
            return text
        
        replacements = {
            '{company_name}': prospect.company_name or '',
            '{contact_name}': prospect.contact_name or '',
            '{email}': prospect.email or '',
            '{phone}': prospect.phone or '',
            '{address}': prospect.address or '',
            '{city}': prospect.city or '',
            '{estimated_value}': str(prospect.estimated_value),
        }
        
        for var, value in replacements.items():
            text = text.replace(var, value)
        
        return text


class ProspectMessagePreviewView(APIView):
    """Preview message with variables replaced"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, prospect_id):
        try:
            prospect = Prospect.objects.get(pk=prospect_id)
        except Prospect.DoesNotExist:
            return Response(
                {"detail": "Prospect not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        template_id = request.data.get('template_id')
        
        if not template_id:
            return Response(
                {"detail": "template_id is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            template = MessageTemplate.objects.get(pk=template_id)
        except MessageTemplate.DoesNotExist:
            return Response(
                {"detail": "Template not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Replace variables
        subject = self._replace_variables(template.subject, prospect)
        body = self._replace_variables(template.body, prospect)
        
        return Response({
            'subject': subject,
            'body': body
        })
    
    def _replace_variables(self, text, prospect):
        """Replace template variables with prospect data"""
        if not text:
            return text
        
        replacements = {
            '{company_name}': prospect.company_name or '',
            '{contact_name}': prospect.contact_name or '',
            '{email}': prospect.email or '',
            '{phone}': prospect.phone or '',
            '{address}': prospect.address or '',
            '{city}': prospect.city or '',
            '{estimated_value}': str(prospect.estimated_value),
        }
        
        for var, value in replacements.items():
            text = text.replace(var, value)
        
        return text


class MessageTemplateViewSet(viewsets.ModelViewSet):
    """ViewSet for managing message templates (prospecting AND internship)"""
    permission_classes = [IsAuthenticated]
    serializer_class = MessageTemplateSerializer
    
    def get_queryset(self):
        queryset = MessageTemplate.objects.all()
        
        # Filter by language
        language = self.request.query_params.get('language')
        if language:
            queryset = queryset.filter(language=language)
        
        # Filter by stage
        stage = self.request.query_params.get('stage')
        if stage:
            queryset = queryset.filter(stage=stage)
        
        # Filter by usage_type (NEW)
        usage_type = self.request.query_params.get('usage_type')
        if usage_type:
            queryset = queryset.filter(usage_type=usage_type)
        
        return queryset
