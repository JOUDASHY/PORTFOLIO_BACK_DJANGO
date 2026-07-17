# Facebook Messenger Integration Module

Module d'intégration Facebook Messenger avec Groq AI pour le backend Django Portfolio.

## 📦 Contenu du module

- `models.py` - Modèles de données (Conversations, Messages)
- `services.py` - Service Facebook Graph API
- `ai_service.py` - Service Groq AI
- `messenger.py` - Handler principal des événements
- `views.py` - Endpoints webhook (GET/POST)
- `urls.py` - Routes
- `admin.py` - Interface admin Django

## 🚀 Utilisation rapide

### 1. Configuration

Variables d'environnement dans `.env` :
```env
GROQ_API_KEY=gsk_xxx
FACEBOOK_PAGE_ACCESS_TOKEN=EAABxxx
FACEBOOK_VERIFY_TOKEN=YOUR_TOKEN
FACEBOOK_PAGE_ID=123456789
```

### 2. Migration

```bash
python manage.py migrate
```

### 3. Test

```bash
python test_messenger.py
```

## 📚 Documentation

Voir les fichiers à la racine du projet :
- `MESSENGER_INTEGRATION.md` - Documentation complète
- `MESSENGER_QUICK_START.md` - Guide rapide
- `MESSENGER_FILES.md` - Liste des fichiers

## 🔧 Architecture

```
Message Messenger
    ↓
Facebook → Webhook POST
    ↓
MessengerEventHandler
    ↓
    ├─→ Déduplication (message.mid)
    ├─→ Récupération conversation (BDD)
    ├─→ Appel Groq AI
    ├─→ Sauvegarde réponse (BDD)
    └─→ Envoi via Graph API
```

## 🎯 Fonctionnalités

- ✅ Messages texte
- ✅ Déduplication automatique
- ✅ Historique conversationnel
- ✅ Typing indicators
- ✅ Mark as seen
- ✅ Support postbacks
- ✅ Gestion d'erreurs
- ✅ Admin Django

## 🔒 Sécurité

- Tokens dans variables d'environnement
- Webhook verification
- Déduplication messages
- Logs sans exposition tokens
- HTTPS obligatoire

## 📝 Personnalisation

### Modifier le système prompt

`ai_service.py` → `get_system_prompt()` :

```python
def get_system_prompt(self) -> str:
    return """Ton prompt personnalisé ici..."""
```

### Ajouter du contexte

```python
from core.models import Profile, Projet

def get_system_prompt(self) -> str:
    profile = Profile.objects.first()
    # Utiliser profile.about, etc.
    return f"Tu es {profile.user.get_full_name()}..."
```

## 🐛 Débogage

Logs dans la console Django (niveau INFO) :
- Réception messages
- Appels Groq
- Envois Facebook
- Erreurs

Pour logs détaillés, modifier `settings.py` :
```python
'loggers': {
    'core.messenger': {
        'level': 'DEBUG',  # Au lieu de INFO
    }
}
```

## 📊 Base de données

### MessengerConversation
- `facebook_user_id` - PSID Facebook
- `page_id` - ID de la page
- `created_at`, `updated_at`

### MessengerMessage
- `conversation` - FK vers Conversation
- `message_id` - ID unique Facebook (déduplication)
- `role` - user | assistant | system
- `content` - Texte du message
- `created_at`

## 🛠️ Maintenance

### Nettoyer les anciennes conversations

```python
from core.messenger.models import MessengerConversation
from django.utils import timezone
from datetime import timedelta

# Supprimer conversations > 30 jours
old_date = timezone.now() - timedelta(days=30)
MessengerConversation.objects.filter(updated_at__lt=old_date).delete()
```

### Statistiques

```python
from core.messenger.models import MessengerConversation, MessengerMessage

# Nombre de conversations
print(f"Conversations: {MessengerConversation.objects.count()}")

# Nombre de messages
print(f"Messages: {MessengerMessage.objects.count()}")

# Messages par utilisateur
for conv in MessengerConversation.objects.all():
    count = conv.messages.count()
    print(f"{conv.facebook_user_id[:10]}...: {count} messages")
```

## 🚀 Extensions futures

- [ ] Support images/fichiers
- [ ] Quick replies
- [ ] Templates (cartes, boutons)
- [ ] Webhook signature verification
- [ ] RAG avec documents
- [ ] Multi-langue
- [ ] Analytics

## 📞 Support

Consultez la documentation principale dans le dossier racine du projet.
