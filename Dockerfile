FROM ubuntu:22.04

# Empêcher la création de fichiers .pyc et activer le buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Installer les dépendances système nécessaires
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       python3.11 \
       python3.11-venv \
       python3-pip \
       build-essential \
       pkg-config \
       libmariadb-dev \
       libgirepository1.0-dev \
       libcairo2-dev \
       libpango1.0-dev \
       libglib2.0-0 \
       shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier et installer uniquement les dépendances Python d'abord (pour profiter du cache Docker)
COPY requirements.txt .
RUN python3.11 -m venv /venv \
    && /venv/bin/pip install --upgrade pip \
    && /venv/bin/pip install -r requirements.txt

# Copier le reste de l’application
COPY . .

# Pointer vers votre settings.py existant
ENV DJANGO_SETTINGS_MODULE=back_django_portfolio_me.settings

# Exposer le port HTTP
EXPOSE 8000

# Lancer les migrations, collectstatic, puis Gunicorn
CMD ["sh", "-c", "\
    /venv/bin/python manage.py migrate --no-input && \
    /venv/bin/python manage.py collectstatic --no-input && \
    /venv/bin/gunicorn back_django_portfolio_me.wsgi:application \
      --bind 0.0.0.0:8000 --workers 3 \
"]
