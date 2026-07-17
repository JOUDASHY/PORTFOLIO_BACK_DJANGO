# 📁 Fichiers créés pour l'intégration Facebook Messenger

## Structure du module

```
core/messenger/
├── __init__.py              # Module init
├── models.py                # MessengerConversation, MessengerMessage
├── services.py              # FacebookGraphAPI (envoi messages)
├── ai_service.py            # GroqAIService (Groq AI)
├── messenger.py             # MessengerEventHandler (logique métier)
├── views.py                 # FacebookWebhookView (GET/POST)
├── urls.py                  # Routes webhook
└── admin.py                 # Admin Django
```

## Fichiers de configuration

```
core/
├── migrations/
│   └── 0041_messenger_models.py    # Migration pour les tables
└── urls.py                         # Routes ajoutées

back_django_portfolio_me/
└── settings.py                     # INSTALLED_APPS + config
```

## Documentation

```
.
├── MESSENGER_INTEGRATION.md        # Documentation complète
├── MESSENGER_QUICK_START.md        # Guide rapide 5 minutes
├── MESSENGER_FILES.md              # Ce fichier
├── API_DOCUMENTATION.md            # Mise à jour avec endpoints
├── .env.example                    # Variables d'environnement exemple
└── test_messenger.py               # Script de test
```

## Modifications dans les fichiers existants

### `core/urls.py`
Ajout de la route :
```python
path("api/facebook/", include("core.messenger.urls")),
```

### `back_django_portfolio_me/settings.py`
Ajouts :
```python
INSTALLED_APPS = [
    ...
    "core.messenger",  # Nouveau
]

# Variables d'environnement
FACEBOOK_PAGE_ACCESS_TOKEN = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN")
FACEBOOK_VERIFY_TOKEN = os.getenv("FACEBOOK_VERIFY_TOKEN")
FACEBOOK_PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")

# Logging
LOGGING = { ... }  # Configuration pour core.messenger
```

### `API_DOCUMENTATION.md`
Ajout de la section **Facebook Messenger Bot** avec :
- Endpoints GET/POST `/api/facebook/webhook/`
- Configuration requise
- Modèles de données
- Fonctionnalités

## Tables de base de données

Deux nouvelles tables créées par la migration `0041` :

1. **`core_messengerconversation`**
   - `id` (PK)
   - `facebook_user_id` (VARCHAR, indexed)
   - `page_id` (VARCHAR)
   - `created_at` (DATETIME)
   - `updated_at` (DATETIME)
   - Contrainte unique : `(facebook_user_id, page_id)`

2. **`core_messengermessage`**
   - `id` (PK)
   - `conversation_id` (FK → core_messengerconversation)
   - `message_id` (VARCHAR, unique) — pour déduplication
   - `role` (ENUM: user, assistant, system)
   - `content` (TEXT)
   - `created_at` (DATETIME)
   - Index : `message_id`, `(conversation_id, created_at)`

## Dépendances

Aucune nouvelle dépendance requise ! Utilise les packages déjà présents :
- ✅ `groq>=0.13.0` (déjà dans requirements.txt)
- ✅ `requests` (déjà dans requirements.txt)
- ✅ `Django` (déjà dans requirements.txt)
- ✅ `djangorestframework` (déjà dans requirements.txt)

## Routes API ajoutées

| Méthode | URL | Usage | Auth |
|---------|-----|-------|------|
| GET | `/api/facebook/webhook/` | Vérification webhook par Facebook | AllowAny |
| POST | `/api/facebook/webhook/` | Réception événements Messenger | AllowAny |

## Admin Django

Deux nouveaux modèles visibles dans l'admin :
- **Messenger Conversations** (lecture seule)
- **Messenger Messages** (lecture seule)

Accessible via : `http://localhost:8000/admin/`

## Variables d'environnement requises

À ajouter dans `.env` :

```env
# Déjà configuré (Groq)
GROQ_API_KEY=gsk_xxx

# Nouveau (Facebook)
FACEBOOK_PAGE_ACCESS_TOKEN=EAABxxx
FACEBOOK_VERIFY_TOKEN=YOUR_SECURE_TOKEN
FACEBOOK_PAGE_ID=123456789
```

## Scripts utiles

### `test_messenger.py`
Script de diagnostic qui vérifie :
- ✅ Configuration Groq
- ✅ Configuration Facebook
- ✅ Tables de base de données
- ✅ Affiche l'URL du webhook

Usage :
```bash
python test_messenger.py
```

## Prochaines étapes

1. ✅ **Installer** : Déjà fait — tous les fichiers créés
2. 📝 **Configurer** : Ajouter les variables dans `.env`
3. 🔄 **Migrer** : `python manage.py migrate`
4. 🧪 **Tester** : `python test_messenger.py`
5. 🚀 **Déployer** : Configurer le webhook sur Facebook
6. 💬 **Utiliser** : Envoyer un message à la Page Facebook

## Support

Documentation :
- 📖 Guide complet : `MESSENGER_INTEGRATION.md`
- 🚀 Guide rapide : `MESSENGER_QUICK_START.md`
- 📋 API : `API_DOCUMENTATION.md`

Logs :
- Console Django pendant le développement
- Configurable via `LOGGING` dans `settings.py`
