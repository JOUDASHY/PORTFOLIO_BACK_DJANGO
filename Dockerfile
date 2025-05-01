FROM ubuntu:22.04

# Empêcher la création de fichiers .pyc, buffering et définir TZ
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=UTC

# Installer tzdata + autres dépendances système, puis nettoyer
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       tzdata \
       python3.11 \
       python3.11-venv \
       python3-pip \
       python3.11-dev \
       build-essential \
       pkg-config \
       libmariadb-dev \
       libgirepository1.0-dev \
       libcairo2-dev \
       libpango1.0-dev \
       libglib2.0-0 \
       shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

# Répondre automatiquement au prompt de configuration de tzdata
RUN ln -fs /usr/share/zoneinfo/UTC /etc/localtime && dpkg-reconfigure --frontend noninteractive tzdata

WORKDIR /app

# Installer Python et créer le venv
COPY requirements.txt /app/
RUN python3.11 -m venv /venv \
    && /venv/bin/pip install --upgrade pip \
    && /venv/bin/pip install -r requirements.txt

# Copier l’application
COPY . /app/

# Pointer vers le module settings de Django
ENV DJANGO_SETTINGS_MODULE=back_django_portfolio_me.settings

EXPOSE 8000

# Lancer migrations, collectstatic puis Gunicorn
CMD [ "sh", "-c", "\
    /venv/bin/python -m pip install gunicorn && \
    /venv/bin/python manage.py migrate --no-input && \
    /venv/bin/python manage.py collectstatic --no-input && \
    /venv/bin/gunicorn back_django_portfolio_me.wsgi:application \
      --bind 0.0.0.0:8000 --workers 3" ]
