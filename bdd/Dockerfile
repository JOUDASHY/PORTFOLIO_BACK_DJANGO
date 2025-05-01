FROM mysql:8.0

# Variables d'environnement MySQL
ENV MYSQL_ROOT_PASSWORD=4734
ENV MYSQL_DATABASE=u614166417_nil_port
ENV MYSQL_USER=server
ENV MYSQL_PASSWORD=4734

# Copie des scripts d'initialisation
# Tous les fichiers .sql et .sh dans initdb/ seront exécutés au démarrage
COPY initdb/ /docker-entrypoint-initdb.d/

# Port exposé
EXPOSE 3306

# Commande par défaut
CMD ["mysqld"]
