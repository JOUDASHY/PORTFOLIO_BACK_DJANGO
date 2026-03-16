from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail, EmailMessage
from django.template.loader import get_template
from weasyprint import HTML
from django.conf import settings

from core.models import Email, EmailResponse, HistoricMail
from core.serializers import EmailSerializer, EmailResponseSerializer, HistoricMailSerializer


class HistoricMailListView(APIView):
    def get(self, request):
        emails = HistoricMail.objects.all().order_by('-date_envoi', '-heure_envoi')
        serializer = HistoricMailSerializer(emails, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SendEmailView(APIView):
    def post(self, request):
        nom_entreprise = request.data.get('nomEntreprise')
        email_entreprise = request.data.get('emailEntreprise')
        lieu_entreprise = request.data.get('lieuEntreprise')
        
        # Optionnel: Utiliser un template
        template_id = request.data.get('template_id')
        custom_subject = request.data.get('custom_subject')
        custom_body = request.data.get('custom_body')
        custom_cover_letter_html = request.data.get('custom_cover_letter_html')  # NOUVEAU
        
        subject = "Demande de stage"
        message = None
        cover_letter_html = None  # Pour générer le PDF dynamiquement
        
        # Si template fourni, charger et personnaliser
        if template_id:
            from core.models import MessageTemplate
            try:
                template = MessageTemplate.objects.get(pk=template_id, usage_type='internship')
                
                # Variables à remplacer
                variables = {
                    '{company_name}': nom_entreprise or '',
                    '{contact_name}': request.data.get('contact_name', ''),
                    '{city}': lieu_entreprise or '',
                    '{student_name}': request.data.get('student_name', 'Eddy Nilsen'),
                    '{school_name}': request.data.get('school_name', 'ENI'),
                    '{internship_type}': request.data.get('internship_type', 'développement web'),
                    '{internship_duration}': request.data.get('internship_duration', '3 mois'),
                    '{internship_start_date}': request.data.get('internship_start_date', ''),
                    '{email}': request.data.get('user_email', ''),
                    '{phone}': request.data.get('user_phone', ''),
                }
                
                # Utiliser custom ou template
                subject = custom_subject or template.subject
                message = custom_body or template.body
                cover_letter_html = custom_cover_letter_html or template.cover_letter_html  # Priorité au custom
                
                # Remplacer les variables dans le body ET le HTML
                for var, value in variables.items():
                    subject = subject.replace(var, str(value))
                    message = message.replace(var, str(value))
                    if cover_letter_html:
                        cover_letter_html = cover_letter_html.replace(var, str(value))
                    
            except MessageTemplate.DoesNotExist:
                pass
        
        # Fallback: utiliser l'ancien message statique
        if not message:
            subject = custom_subject or "Demande de stage"
            message = custom_body or f'''Cher(e) Monsieur/Madame le/la responsable {nom_entreprise},
Je me permets de vous contacter afin de postuler pour un stage au sein de votre entreprise {nom_entreprise}...'''
        
        from_email = settings.EMAIL_HOST_USER
        to_mail = email_entreprise
        
        # Générer le PDF avec le template dynamique OU le template fixe
        if cover_letter_html:
            pdf_file = self.generate_pdf_from_html(cover_letter_html)
        else:
            pdf_file = self.generate_pdf(nom_entreprise, email_entreprise, lieu_entreprise)
        
        # Créer l'email avec les pièces jointes
        email = EmailMessage(subject, message, from_email, [to_mail])
        email.attach("LM_Eddy_Nilsen.pdf", pdf_file, "application/pdf")
        
        # ✨ NOUVEAU: Récupérer le CV depuis l'API (modèle CV) ✨
        cv_file = self.get_cv_from_database()
        if cv_file:
            email.attach_file(cv_file.file.path)
        else:
            # Fallback: ancien fichier statique
            email.attach_file("CV_Eddy_Nilsen.pdf")
        
        # Envoyer l'email avec gestion d'erreur
        try:
            email.send(fail_silently=False)
            print(f"✅ Email sent successfully to {to_mail}")
            print(f"   Subject: {subject}")
            print(f"   Attachments: LM_Eddy_Nilsen.pdf + CV")
        except Exception as e:
            print(f"❌ Failed to send email: {str(e)}")
            return Response(
                {"detail": f"Failed to send email: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        HistoricMail.objects.create(
            nom_entreprise=nom_entreprise,
            email_entreprise=email_entreprise,
            lieu_entreprise=lieu_entreprise
        )
        return Response({"message": "Email envoyé avec succès"}, status=status.HTTP_200_OK)
    
    def get_cv_from_database(self):
        """Récupérer le CV actif depuis la base de données"""
        from core.models import CV
        cv = CV.objects.filter(is_active=True).first()
        
        # Si pas de CV actif, prendre le plus récent
        if not cv:
            cv = CV.objects.order_by('-uploaded_at').first()
        
        return cv
    
    def generate_pdf_from_html(self, html_content):
        """Generate PDF from dynamic HTML string"""
        pdf_file = HTML(string=html_content).write_pdf()
        return pdf_file

    def generate_pdf(self, nom_entreprise, email_entreprise, lieu_entreprise):
        context = {'nom_entreprise': nom_entreprise,'email_entreprise': email_entreprise,'lieu_entreprise': lieu_entreprise}
        template = get_template('app/LM.html')
        html_content = template.render(context)
        pdf_file = HTML(string=html_content).write_pdf()
        return pdf_file


class EmailViewSet(viewsets.ModelViewSet):
    queryset = Email.objects.all().order_by('-date', 'heure')
    serializer_class = EmailSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]
        
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            client_email = request.data.get('email')
            if client_email:
                send_mail(
                    subject="Confirmation de réception de votre message",
                    message="Merci d'avoir envoyé votre message. Nous allons vous répondre dans les plus brefs délais.",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client_email],
                    fail_silently=True,
                )
        return response


class EmailResponseViewSet(viewsets.ModelViewSet):
    queryset = EmailResponse.objects.all()
    serializer_class = EmailResponseSerializer

    def get_queryset(self):
        email_id = self.kwargs.get('email_id')
        if email_id:
            return EmailResponse.objects.filter(email__id=email_id)
        return super().get_queryset()

    def create(self, request, *args, **kwargs):
        email_id = self.kwargs.get('email_id')
        if not email_id:
            return Response({'error': 'Email ID is required in the URL'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            email = Email.objects.get(id=email_id)
        except Email.DoesNotExist:
            return Response({'error': 'Email not found'}, status=status.HTTP_404_NOT_FOUND)
        data = request.data.copy()
        data['email'] = email.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        response_message = data.get('response')
        send_mail(
            subject="Réponse à votre email",
            message=response_message,
            from_email="no-reply@votre-domaine.com",
            recipient_list=[email.email],
            fail_silently=False,
        )
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


