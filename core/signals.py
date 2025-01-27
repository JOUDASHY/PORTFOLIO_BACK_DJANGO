from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile
from django.dispatch import receiver
from django.utils.timezone import now
from datetime import timedelta
from .models import Rating, Visit, Notification
from django.contrib.auth.models import User



@receiver(post_save, sender=Rating)
def notify_on_rating(sender, instance, created, **kwargs):
    """
    Créer une notification pour l'utilisateur avec l'ID 2 lorsqu'un projet reçoit une note.
    """
    if created:
        try:
            project_owner = User.objects.get(id=1)  # Utilisateur avec l'ID 2
            Notification.objects.create(
                user=project_owner,
                title="Nouvelle note reçue",
                message=f"Votre projet a reçu une nouvelle note de {instance.score}/5."
            )
        except User.DoesNotExist:
            print("L'utilisateur avec l'ID 2 n'existe pas.")

@receiver(post_save, sender=Visit)
def notify_on_view_threshold(sender, instance, created, **kwargs):
    """
    Créer une notification pour l'utilisateur avec l'ID 2 lorsqu'un seuil de visites est atteint.
    """
    if created:
        try:
            yesterday = now() - timedelta(days=1)
            visits_count = Visit.objects.filter(timestamp__gte=yesterday).count()

            if visits_count == 5:  # Seuil atteint
                project_owner = User.objects.get(id=1)  # Utilisateur avec l'ID 2
                Notification.objects.create(
                    user=project_owner,
                    title="Seuil de vues atteint",
                    message=f"Votre projet a atteint {visits_count} visites en une journée."
                )
        except User.DoesNotExist:
            print("L'utilisateur avec l'ID 2 n'existe pas.")


            
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)  # Évite les doublons

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


