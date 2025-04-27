FROM python:3.11-slim

# Empêcher la création de fichiers .pyc et activer le buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Installer les dépendances système nécessaires (libmariadb-dev pour MariaDB/MySQL)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       pkg-config \
       libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier et installer uniquement les dépendances Python d'abord (pour profiter du cache Docker)
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copier le reste de l’application
COPY . .

# Pointer vers votre settings.py existant
ENV DJANGO_SETTINGS_MODULE=back_django_portfolio_me.settings

# Exposer le port HTTP
EXPOSE 8000

# Lancer les migrations, collectstatic, puis Gunicorn
CMD ["sh", "-c", "\
    python manage.py migrate --no-input && \
    python manage.py collectstatic --no-input && \
    gunicorn back_django_portfolio_me.wsgi:application \
      --bind 0.0.0.0:8000 --workers 3 \
"]
