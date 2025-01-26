import random
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from core.models import Visit  # Remplace `core` par le nom de ton application

# Supprime les anciennes données (facultatif)
Visit.objects.all().delete()

# Génère les données de visites par mois entre janvier 2024 et janvier 2025
start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 1, 31)

current_date = start_date

while current_date <= end_date:
    # Calcule le début et la fin du mois
    month_start = current_date.replace(day=1)
    next_month = month_start + relativedelta(months=1)
    month_end = next_month - timedelta(seconds=1)  # Fin du mois

    # Génère un nombre aléatoire de visites pour le mois
    visits_per_month = random.randint(500, 1000)  # Ajuste les valeurs selon tes besoins

    for _ in range(visits_per_month):
        # Génère une date aléatoire dans le mois
        random_date = month_start + timedelta(seconds=random.randint(0, int((month_end - month_start).total_seconds())))

        # Crée une visite avec une adresse IP aléatoire
        Visit.objects.create(
            ip_address=f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
            timestamp=random_date
        )

    # Passe au mois suivant
    current_date = next_month

print("Monthly data inserted successfully!")
