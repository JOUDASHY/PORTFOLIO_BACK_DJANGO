FROM python:3.11-slim

# Empêcher la création de fichiers pyc et activer le buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Installer les dépendances système nécessaires
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*

# Créer et positionner le répertoire de travail
WORKDIR /app

# Copier et installer les dépendances Python
COPY requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copier le reste du code de l'application
COPY . /app/

# Charger les variables d'environnement à partir du fichier .env
# (Assurez-vous que python-dotenv est dans requirements.txt)
ENV DJANGO_SETTINGS_MODULE=monprojet.settings.production

# Exposer le port HTTP de Django
EXPOSE 8000

# Commande par défaut : appliquer les migrations, collectstatic, puis lancer Gunicorn
CMD ["sh", "-c", "python manage.py migrate --no-input && python manage.py collectstatic --no-input && gunicorn monprojet.wsgi:application --bind 0.0.0.0:8000 --workers 3"]
