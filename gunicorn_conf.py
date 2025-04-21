# Fichier /var/www/PORTFOLIO_BACK_DJANGO/gunicorn_conf.py
bind = "0.0.0.0:8000"
workers = 1              # Réduisez à 1 worker pour debug
timeout = 300            # Augmentez à 5 min
keepalive = 120          # Réduisez keepalive
max_requests = 0         # Désactivez le recyclage pour tests
max_requests_jitter = 0  # Désactivez le jitter