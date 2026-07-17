# 🤖 Facebook Messenger Bot - Intégration Complète

## 📋 Vue d'Ensemble

Ce projet intègre un bot Facebook Messenger alimenté par l'IA Groq dans votre backend Django existant. Le bot peut recevoir des messages via Facebook Messenger, les traiter avec l'IA Groq (qui a déjà le contexte de votre portfolio), et répondre automatiquement.

### Architecture

```
Facebook Messenger
       │
       ▼
Meta Webhook (GET/POST)
       │
       ▼
Django Backend (core/messenger/)
       │
       ├─── Vérification Webhook
       ├─── Réception Message
       ├─── Sauvegarde Conversation
       ├─── Appel Groq AI
       └─── Envoi Réponse
       │
       ▼
Facebook Messenger
```

---

## 📁 Structure des Fichiers

### Fichiers Créés

```
PORTFOLIO_BACK_DJANGO/
│
├── core/
│   ├── messenger/                          # 🆕 Module Messenger
│   │   ├── __init__.py                     # Configuration module
│   │   ├── admin.py                        # Interface admin Django
│   │   ├── ai_service.py                   # ⭐ Intégration Groq AI
│   │   ├── apps.py                         # Configuration app
│   │   ├── messenger.py                    # ⭐ Traitement événements
│   │   ├── models.py                       # (Modèles dans core/models.py)
│   │   ├── services.py                     # ⭐ Facebook Graph API
│   │   ├── urls.py                         # Routes webhook
│   │   ├── views.py                        # ⭐ Webhook GET/POST
│   │   └── README.md                       # Documentation architecture
│   │
│   ├── models.py                           # 🔄 Modifié : +MessengerConversation/Message
│   ├── urls.py                             # 🔄 Modifié : +routes /api/facebook/
│   └── migrations/
│       └── 0049_messenger_models.py        # 🆕 Migration tables
│
├── back_django_portfolio_me/
│   └── settings.py                         # 🔄 Modifié : +logging, +FB vars, +core.messenger
│
├── .env.example                            # 🔄 Modifié : +variables Facebook
├── test_messenger_integration.py           # 🆕 Script de test complet
├── MESSENGER_DEPLOYMENT_GUIDE.md           # 🆕 Guide de déploiement détaillé
├── MESSENGER_QUICK_REFERENCE.md            # 🆕 Référence rapide
├── MESSENGER_DEPLOYMENT_CHECKLIST.md       # 🆕 Checklist de déploiement
└── README_MESSENGER.md                     # 🆕 Ce fichier
```

### Fichiers Clés

| Fichier | Rôle |
|---------|------|
| `core/messenger/views.py` | Gère le webhook Facebook (GET=vérification, POST=événements) |
| `core/messenger/messenger.py` | Traite les événements Messenger et orchestre le flux |
| `core/messenger/ai_service.py` | Appelle Groq AI avec le contexte portfolio |
| `core/messenger/services.py` | Envoie les réponses via Facebook Graph API |
| `core/models.py` | Modèles BDD (`MessengerConversation`, `MessengerMessage`) |
| `core/migrations/0049_messenger_models.py` | Crée les tables en base de données |

---

## 🚀 Déploiement

### Démarrage Rapide (TL;DR)

```powershell
# 1. Local
git add .
git commit -m "Add Facebook Messenger bot"
git push

# 2. Serveur
cd C:\inetpub\wwwroot\test_py
git pull
.\venv\Scripts\activate
python manage.py migrate
iisreset

# 3. Configurer .env (voir section Variables)

# 4. Tester
python test_messenger_integration.py

# 5. Configurer Facebook (voir section Facebook)
```

### Documentation Détaillée

Pour un déploiement complet avec toutes les étapes, voir :
👉 **[MESSENGER_DEPLOYMENT_GUIDE.md](MESSENGER_DEPLOYMENT_GUIDE.md)**

Pour une référence rapide des commandes :
👉 **[MESSENGER_QUICK_REFERENCE.md](MESSENGER_QUICK_REFERENCE.md)**

Pour suivre le déploiement étape par étape :
👉 **[MESSENGER_DEPLOYMENT_CHECKLIST.md](MESSENGER_DEPLOYMENT_CHECKLIST.md)**

---

## 🔧 Configuration

### Variables d'Environnement

Ajouter dans `.env` (local et serveur) :

```env
# Facebook Messenger
FACEBOOK_PAGE_ACCESS_TOKEN=EAABxxxxxxxxxxxxxxxx
FACEBOOK_VERIFY_TOKEN=THE_BEAST_VERIFY_YOUR_SECURE_TOKEN
FACEBOOK_PAGE_ID=123456789012345

# Groq AI (déjà présent normalement)
GROQ_API_KEY=gsk_your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

#### Comment Obtenir les Tokens

**1. FACEBOOK_PAGE_ACCESS_TOKEN**
- Aller sur https://developers.facebook.com/apps
- Sélectionner votre app (ou créer une nouvelle)
- Menu : "Messenger" > "Settings"
- Section "Access Tokens"
- Sélectionner votre Page Facebook
- Cliquer "Generate Token"
- Copier le token

**2. FACEBOOK_VERIFY_TOKEN**
- Choisir une chaîne sécurisée aléatoire
- Exemple : `THE_BEAST_VERIFY_2026`
- La stocker dans `.env`
- L'utiliser lors de la configuration du webhook sur Facebook

**3. FACEBOOK_PAGE_ID**
- Aller sur votre Page Facebook
- Menu : "Paramètres" > "À propos"
- Copier "ID de la Page"

### Configuration Facebook

**Étape 1 : Créer/Configurer l'App**
1. https://developers.facebook.com/apps
2. Créer une app (ou utiliser existante)
3. Ajouter le produit "Messenger"

**Étape 2 : Configurer le Webhook**
1. Menu : "Messenger" > "Settings" > "Webhooks"
2. Cliquer "Add Callback URL"
3. Entrer :
   - **Callback URL** : `https://test-back.unityfianar.site/api/facebook/webhook/`
   - **Verify Token** : Votre `FACEBOOK_VERIFY_TOKEN` du `.env`
4. Cliquer "Verify and Save"
5. ✅ Devrait afficher "Success" si tout est configuré

**Étape 3 : Abonner la Page**
1. Toujours dans "Webhooks"
2. Section "Add Subscriptions"
3. Sélectionner votre Page
4. Cocher :
   - ✅ `messages`
   - ✅ `messaging_postbacks`
5. Sauvegarder

---

## 🧪 Tests

### Test Automatique Complet

```powershell
python test_messenger_integration.py
```

**Teste :**
- ✅ Variables d'environnement
- ✅ Modèles de base de données
- ✅ Service Facebook API
- ✅ Service Groq AI
- ✅ Configuration Django
- ✅ Configuration logging

### Test Webhook Manuellement

**Test GET (vérification) :**
```powershell
curl "https://test-back.unityfianar.site/api/facebook/webhook/?hub.mode=subscribe&hub.verify_token=THE_BEAST_VERIFY&hub.challenge=HELLO"
# Devrait retourner : HELLO
```

**Test POST (simuler un événement) :**
```powershell
curl -X POST https://test-back.unityfianar.site/api/facebook/webhook/ `
  -H "Content-Type: application/json" `
  -d '{\"object\":\"page\",\"entry\":[{\"messaging\":[{\"sender\":{\"id\":\"12345\"},\"recipient\":{\"id\":\"67890\"},\"message\":{\"mid\":\"test_mid\",\"text\":\"Bonjour\"}}]}]}'
```

### Test Réel

1. Ouvrir Facebook Messenger
2. Chercher votre Page Facebook
3. Envoyer un message : "Bonjour"
4. Vérifier les logs : `type messenger_debug.log`
5. Attendre la réponse du bot (2-5 secondes)

---

## 📊 Monitoring

### Logs

**Voir les logs :**
```powershell
type messenger_debug.log
```

**Suivre en temps réel :**
```powershell
Get-Content messenger_debug.log -Wait -Tail 20
```

**Chercher des erreurs :**
```powershell
type messenger_debug.log | findstr "ERROR"
```

### Base de Données

**Conversations actives :**
```sql
SELECT * FROM core_messengerconversation 
ORDER BY updated_at DESC LIMIT 10;
```

**Messages récents :**
```sql
SELECT * FROM core_messengermessage 
ORDER BY created_at DESC LIMIT 20;
```

**Statistiques :**
```sql
SELECT 
    DATE(created_at) as date,
    COUNT(*) as total_messages,
    SUM(CASE WHEN role='user' THEN 1 ELSE 0 END) as user_messages,
    SUM(CASE WHEN role='assistant' THEN 1 ELSE 0 END) as bot_responses
FROM core_messengermessage
GROUP BY DATE(created_at)
ORDER BY date DESC;
```

### Admin Django

Accéder à : `https://test-back.unityfianar.site/admin/`

Sections disponibles :
- **Messenger Conversations** : Liste des conversations
- **Messenger Messages** : Historique complet des messages

---

## 🔍 Dépannage

### Le bot ne répond pas

**Checklist :**
1. ✅ Les migrations sont appliquées ? → `python manage.py migrate`
2. ✅ Les variables `.env` sont configurées ? → `python test_messenger_integration.py`
3. ✅ Le webhook est vérifié sur Facebook ? → Tester GET endpoint
4. ✅ Les logs montrent des POST ? → `type messenger_debug.log`
5. ✅ Groq répond ? → Vérifier logs pour "Groq AI"
6. ✅ Le serveur est redémarré ? → `iisreset`

### Erreur : "No migrations to apply"

```powershell
# Vérifier que le fichier existe
dir core\migrations\0049_messenger_models.py

# Si absent, le recréer
python manage.py makemigrations core

# Appliquer
python manage.py migrate
```

### Erreur : "Webhook verification failed"

- Vérifier que `FACEBOOK_VERIFY_TOKEN` est dans `.env`
- Vérifier qu'il correspond à celui sur Facebook
- Tester : `curl "URL?hub.mode=subscribe&hub.verify_token=TOKEN&hub.challenge=TEST"`

### Avertissement : "UnicodeEncodeError" dans la console

C'est cosmétique (emojis dans logs). Le fichier `messenger_debug.log` enregistre correctement.

**Solution (optionnelle) :**
Utiliser PowerShell au lieu de CMD pour meilleur support Unicode.

---

## 🎓 Fonctionnalités

### Actuelles ✅

- ✅ Réception de messages texte Messenger
- ✅ Traitement via Groq AI avec contexte portfolio
- ✅ Réponses automatiques intelligentes
- ✅ Historique de conversation persistant
- ✅ Déduplication des messages (via `message_id`)
- ✅ Logging détaillé à chaque étape
- ✅ Gestion d'erreurs robuste
- ✅ Interface admin Django

### Contexte IA

Le bot connaît automatiquement :
- 👤 Nom : Nilsen Un-it
- 💼 Rôle : Développeur Full Stack
- 💻 Technologies : Django, React, MySQL, etc.
- 🌐 Portfolio : https://portfolio.unityfianar.site

**Personnaliser le contexte :**
Éditer `core/messenger/ai_service.py` → méthode `_build_system_message()`

### Futures Améliorations 🚀

- [ ] Support des images/pièces jointes
- [ ] Boutons interactifs (Quick Replies)
- [ ] Intégration RAG pour réponses basées sur documents
- [ ] Notifications proactives
- [ ] Dashboard analytics
- [ ] Multi-langue (FR/EN)
- [ ] Support WhatsApp Business (réutiliser même backend)

---

## 📚 Documentation Supplémentaire

### Ce Projet
- [Guide de Déploiement Complet](MESSENGER_DEPLOYMENT_GUIDE.md)
- [Référence Rapide](MESSENGER_QUICK_REFERENCE.md)
- [Checklist de Déploiement](MESSENGER_DEPLOYMENT_CHECKLIST.md)
- [Architecture Détaillée](core/messenger/README.md)

### Ressources Externes
- [Facebook Messenger Platform](https://developers.facebook.com/docs/messenger-platform)
- [Groq API Documentation](https://console.groq.com/docs)
- [Django REST Framework](https://www.django-rest-framework.org/)

---

## 🤝 Support

### Problème Technique

1. Vérifier les logs : `type messenger_debug.log`
2. Exécuter les tests : `python test_messenger_integration.py`
3. Consulter la section Dépannage ci-dessus
4. Vérifier la documentation Facebook

### Contact

Pour toute question sur l'intégration :
- 📧 Email : [votre-email]
- 📱 WhatsApp : [votre-numéro]
- 💬 Messenger : [votre-page]

---

## 📄 Licence

Ce projet est une intégration privée pour le portfolio de Nilsen Un-it.

---

**Version :** 1.0.0  
**Date :** 2026-07-17  
**Statut :** ✅ Prêt pour production  
**Dernière mise à jour :** 2026-07-17
