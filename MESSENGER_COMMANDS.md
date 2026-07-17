# 🔧 Commandes Messenger Bot

## Installation & Configuration

```bash
# 1. Migrer la base de données
python manage.py migrate

# 2. Tester la configuration
python test_messenger.py

# 3. Créer un superuser (si nécessaire)
python manage.py createsuperuser

# 4. Démarrer le serveur
python manage.py runserver
```

---

## Tests & Diagnostic

```bash
# Test complet de l'intégration
python test_messenger.py

# Tester uniquement Groq AI
python -c "from core.messenger.ai_service import GroqAIService; s = GroqAIService(); print(s.chat([{'role':'user','content':'Bonjour'}]))"

# Tester uniquement Facebook Graph API
python -c "from core.messenger.services import FacebookGraphAPI; api = FacebookGraphAPI(); print('OK')"

# Vérifier les migrations
python manage.py showmigrations core

# Vérifier les modèles
python manage.py shell
>>> from core.messenger.models import MessengerConversation, MessengerMessage
>>> print(MessengerConversation.objects.count())
>>> print(MessengerMessage.objects.count())
```

---

## Base de données

```bash
# Voir les conversations
python manage.py shell
>>> from core.messenger.models import MessengerConversation
>>> for conv in MessengerConversation.objects.all():
...     print(f"{conv.facebook_user_id}: {conv.messages.count()} messages")

# Supprimer les conversations anciennes (> 30 jours)
python manage.py shell
>>> from core.messenger.models import MessengerConversation
>>> from django.utils import timezone
>>> from datetime import timedelta
>>> old_date = timezone.now() - timedelta(days=30)
>>> MessengerConversation.objects.filter(updated_at__lt=old_date).delete()

# Supprimer toutes les conversations (ATTENTION!)
python manage.py shell
>>> from core.messenger.models import MessengerConversation
>>> MessengerConversation.objects.all().delete()
```

---

## Admin Django

```bash
# Accéder à l'admin
# URL: http://localhost:8000/admin/
# Section: CORE → Messenger conversations

# Créer un superuser si nécessaire
python manage.py createsuperuser
```

---

## Développement

```bash
# Activer l'environnement virtuel
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Démarrer le serveur en mode debug
python manage.py runserver

# Démarrer avec un port spécifique
python manage.py runserver 8080
```

---

## Logs & Debug

```bash
# Voir les logs en temps réel (pendant runserver)
# Les logs Messenger s'affichent automatiquement dans la console

# Pour augmenter le niveau de détail:
# Éditez settings.py:
# 'core.messenger': {'level': 'DEBUG'}  # Au lieu de INFO
```

---

## Test du Webhook

```bash
# Test GET (verification)
curl "http://localhost:8000/api/facebook/webhook/?hub.mode=subscribe&hub.verify_token=THE_BEAST_VERIFY&hub.challenge=test123"
# Devrait retourner: test123

# Test POST (événement simulé)
curl -X POST http://localhost:8000/api/facebook/webhook/ \
  -H "Content-Type: application/json" \
  -d '{
    "object": "page",
    "entry": [{
      "messaging": [{
        "sender": {"id": "123456"},
        "recipient": {"id": "789012"},
        "message": {
          "mid": "test_mid",
          "text": "Bonjour"
        }
      }]
    }]
  }'
```

---

## Statistiques

```python
# Dans manage.py shell
from core.messenger.models import MessengerConversation, MessengerMessage

# Nombre total de conversations
print(f"Conversations: {MessengerConversation.objects.count()}")

# Nombre total de messages
print(f"Messages: {MessengerMessage.objects.count()}")

# Messages par role
from django.db.models import Count
stats = MessengerMessage.objects.values('role').annotate(count=Count('id'))
for stat in stats:
    print(f"{stat['role']}: {stat['count']}")

# Conversations les plus actives
for conv in MessengerConversation.objects.all():
    count = conv.messages.count()
    print(f"{conv.facebook_user_id[:10]}...: {count} messages")

# Dernier message reçu
last = MessengerMessage.objects.filter(role='user').order_by('-created_at').first()
if last:
    print(f"Dernier message: {last.content[:50]}... ({last.created_at})")
```

---

## Maintenance

```bash
# Backup de la base de données
python manage.py dumpdata core.messengerconversation core.messengermessage > messenger_backup.json

# Restaurer depuis un backup
python manage.py loaddata messenger_backup.json

# Supprimer les anciens messages (garder seulement les 1000 derniers)
python manage.py shell
>>> from core.messenger.models import MessengerMessage
>>> old_messages = MessengerMessage.objects.all().order_by('-created_at')[1000:]
>>> old_messages.delete()
```

---

## Variables d'environnement

```bash
# Vérifier les variables (Windows)
echo %GROQ_API_KEY%
echo %FACEBOOK_PAGE_ACCESS_TOKEN%
echo %FACEBOOK_VERIFY_TOKEN%
echo %FACEBOOK_PAGE_ID%

# Vérifier les variables (Linux/Mac)
echo $GROQ_API_KEY
echo $FACEBOOK_PAGE_ACCESS_TOKEN
echo $FACEBOOK_VERIFY_TOKEN
echo $FACEBOOK_PAGE_ID

# Ou dans Django shell
python manage.py shell
>>> import os
>>> print(os.getenv('GROQ_API_KEY'))
>>> print(os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN'))
```

---

## Déploiement

```bash
# Collecter les fichiers statiques
python manage.py collectstatic --noinput

# Avec Gunicorn
gunicorn back_django_portfolio_me.wsgi:application --bind 0.0.0.0:8000

# Avec Uvicorn (si ASGI)
uvicorn back_django_portfolio_me.asgi:application --host 0.0.0.0 --port 8000
```

---

## Utilitaires

```bash
# Générer un nouveau token de vérification aléatoire
python -c "import secrets; print(secrets.token_urlsafe(16))"

# Vérifier la version de Groq
pip show groq

# Vérifier les dépendances
pip list | grep -E "groq|django|requests"

# Mettre à jour Groq
pip install --upgrade groq
```

---

## Documentation

```bash
# Ouvrir la documentation
# Windows:
start MESSENGER_QUICK_START.md
start MESSENGER_INTEGRATION.md

# Linux/Mac:
xdg-open MESSENGER_QUICK_START.md
open MESSENGER_QUICK_START.md

# Ou éditez directement:
code core/messenger/ai_service.py
```

---

## Aide rapide

| Commande | Description |
|----------|-------------|
| `python manage.py migrate` | Créer les tables |
| `python test_messenger.py` | Tester la config |
| `python manage.py runserver` | Démarrer serveur |
| `python manage.py shell` | Console Django |
| `python manage.py createsuperuser` | Créer admin |

---

## Raccourcis Shell

```python
# Créer un fichier shortcuts.py à la racine
# Puis: python manage.py shell < shortcuts.py

from core.messenger.models import MessengerConversation, MessengerMessage

def stats():
    """Afficher les statistiques"""
    print(f"Conversations: {MessengerConversation.objects.count()}")
    print(f"Messages: {MessengerMessage.objects.count()}")

def last_conversations(n=5):
    """Afficher les N dernières conversations"""
    for conv in MessengerConversation.objects.all()[:n]:
        count = conv.messages.count()
        print(f"{conv.facebook_user_id}: {count} messages")

def clear_old(days=30):
    """Supprimer les conversations > N jours"""
    from django.utils import timezone
    from datetime import timedelta
    old_date = timezone.now() - timedelta(days=days)
    deleted = MessengerConversation.objects.filter(updated_at__lt=old_date).delete()
    print(f"Supprimé: {deleted[0]} conversations")

# Utilisation:
# >>> stats()
# >>> last_conversations(10)
# >>> clear_old(60)
```

---

**💡 Conseil** : Bookmarkez ce fichier pour y accéder rapidement !
