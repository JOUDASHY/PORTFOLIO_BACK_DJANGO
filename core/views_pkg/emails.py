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
        subject = "Demande de stage"
        message = f'''Cher(e) Monsieur/Madame le/la responsable {nom_entreprise},
Je me permets de vous contacter afin de postuler pour un stage au sein de votre entreprise {nom_entreprise} . Je suis actuellement étudiant 3 ème année de licence en Informatique à l'ENI, et je suis très intéressé par l'opportunité de rejoindre votre entreprise pour compléter ma formation pratique.

Je suis particulièrement attiré par le développement Web Django, devops et administration Système et réseaux, et je suis convaincu que ce stage me permettrait d'acquérir des compétences précieuses dans le domaine.Voilà ainsi de suite mon CV et ma lettre de motivation'''
        from_email = settings.EMAIL_HOST_USER
        to_mail = email_entreprise
        pdf_file = self.generate_pdf(nom_entreprise, email_entreprise, lieu_entreprise)
        email = EmailMessage(subject, message, from_email, [to_mail])
        email.attach("LM_Eddy_Nilsen.pdf", pdf_file, "application/pdf")
        email.attach_file("CV_Eddy_Nilsen.pdf")
        email.send()
        HistoricMail.objects.create(
            nom_entreprise=nom_entreprise,
            email_entreprise=email_entreprise,
            lieu_entreprise=lieu_entreprise
        )
        return Response({"message": "Email envoyé avec succès"}, status=status.HTTP_200_OK)

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


