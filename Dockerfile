FROM python:3.11-slim

# Empêcher la création de fichiers pyc et activer le buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Installer les dépendances système nécessaires
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       pkg-config \
       libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*

# Créer et positionner le répertoire de travail
WORKDIR /app

# Copier et installer les dépendances Python
COPY requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copier le reste du code de l'application
COPY . /app/

# Définir le module de configuration Django
ENV DJANGO_SETTINGS_MODULE=back_django_portfolio_me.settings.production

# Exposer le port HTTP de Django
EXPOSE 8000

# Commande par défaut : appliquer les migrations, collectstatic, puis lancer Gunicorn
CMD ["sh", "-c", "python manage.py migrate --no-input && python manage.py collectstatic --no-input && gunicorn back_django_portfolio_me.wsgi:application --bind 0.0.0.0:8000 --workers 3"]
