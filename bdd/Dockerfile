FROM mysql:8.0

# Variables d'environnement MySQL
ENV MYSQL_ROOT_PASSWORD=root_password
ENV MYSQL_DATABASE=app_db
ENV MYSQL_USER=app_user
ENV MYSQL_PASSWORD=app_password

# Copie des scripts d'initialisation
# Tous les fichiers .sql et .sh dans initdb/ seront exécutés au démarrage
COPY initdb/ /docker-entrypoint-initdb.d/

# Port exposé
EXPOSE 3306

# Commande par défaut
CMD ["mysqld"]
