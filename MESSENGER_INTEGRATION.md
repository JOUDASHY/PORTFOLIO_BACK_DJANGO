# 🤖 Intégration Facebook Messenger Bot

## Vue d'ensemble

Ce document explique comment configurer et utiliser le bot Facebook Messenger intégré à votre backend Django avec Groq AI.

## Architecture

```
Client Messenger
    ↓
Facebook Messenger Platform
    ↓
Meta Webhook (POST/GET)
    ↓
Django Backend (/api/facebook/webhook/)
    ↓
    ├── Authentification Webhook (GET)
    ├── Lecture du message (POST)
    ├── Appel IA Groq
    ├── Sauvegarde conversation (BDD)
    └── Envoi réponse Messenger
    ↓
Facebook Messenger (réponse à l'utilisateur)
```

## Structure du module

```
core/messenger/
├── __init__.py
├── models.py           # MessengerConversation, MessengerMessage
├── services.py         # FacebookGraphAPI (envoi messages)
├── ai_service.py       # GroqAIService (génération réponses IA)
├── messenger.py        # MessengerEventHandler (logique métier)
├── views.py            # FacebookWebhookView (endpoint webhook)
├── urls.py             # Routes (/api/facebook/webhook/)
└── admin.py            # Admin Django pour visualiser conversations
```

## Configuration

### 1. Variables d'environnement

Ajoutez ces variables dans votre fichier `.env` :

```env
# Groq AI (déjà configuré)
GROQ_API_KEY=gsk_your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile  # optionnel, défaut: llama-3.3-70b-versatile

# Facebook Messenger
FACEBOOK_PAGE_ACCESS_TOKEN=EAABxxxxxxxxxxxxxxxx
FACEBOOK_VERIFY_TOKEN=THE_BEAST_VERIFY
FACEBOOK_PAGE_ID=123456789
```

### 2. Obtenir les tokens Facebook

#### A. Créer une App Facebook

1. Allez sur [developers.facebook.com](https://developers.facebook.com)
2. Créez une nouvelle application
3. Ajoutez le produit **Messenger**

#### B. Obtenir le Page Access Token

1. Dans votre app, allez dans **Messenger** > **Settings**
2. Sélectionnez votre Page Facebook
3. Cliquez sur **Generate Token**
4. Copiez le token → `FACEBOOK_PAGE_ACCESS_TOKEN`

#### C. Créer le Verify Token

Choisissez n'importe quelle chaîne sécurisée (ex: `THE_BEAST_VERIFY_123`) → `FACEBOOK_VERIFY_TOKEN`

#### D. Obtenir le Page ID

1. Allez sur votre Page Facebook
2. Cliquez sur **About**
3. Copiez le **Page ID** → `FACEBOOK_PAGE_ID`

### 3. Configurer le Webhook Facebook

#### A. URL du Webhook

Votre URL webhook sera :
```
https://votre-domaine.com/api/facebook/webhook/
```

**Important** : Le webhook DOIT être en **HTTPS** (pas HTTP)

#### B. Dans Facebook Developers

1. Allez dans **Messenger** > **Settings** > **Webhooks**
2. Cliquez sur **Add Callback URL**
3. Entrez :
   - **Callback URL** : `https://votre-domaine.com/api/facebook/webhook/`
   - **Verify Token** : La valeur de `FACEBOOK_VERIFY_TOKEN`
4. Cliquez sur **Verify and Save**

#### C. S'abonner aux événements

Cochez ces événements :
- ✅ `messages`
- ✅ `messaging_postbacks`
- ✅ `messaging_optins` (optionnel)
- ✅ `message_deliveries` (optionnel)
- ✅ `message_reads` (optionnel)

Cliquez sur **Subscribe**

### 4. Migrations de base de données

Exécutez les migrations pour créer les tables nécessaires :

```bash
python manage.py migrate
```

Cela créera deux tables :
- `core_messengerconversation` : Conversations avec les utilisateurs
- `core_messengermessage` : Messages individuels

## Utilisation

### Tester le bot

1. Envoyez un message à votre Page Facebook via Messenger
2. Le bot devrait répondre automatiquement via Groq AI
3. L'historique des conversations est sauvegardé en BDD

### Visualiser les conversations (Admin Django)

1. Connectez-vous à l'admin Django : `/admin/`
2. Allez dans **CORE** > **Messenger conversations**
3. Vous pouvez voir :
   - Les conversations actives
   - L'historique des messages
   - Les utilisateurs qui ont interagi avec le bot

### Personnaliser le bot

#### Modifier le système prompt

Éditez `core/messenger/ai_service.py` :

```python
def get_system_prompt(self) -> str:
    return """Tu es un assistant virtuel qui...
    
    [Personnalisez le comportement ici]
    """
```

#### Modifier le modèle Groq

Dans `.env` :
```env
GROQ_MODEL=llama-3.3-70b-versatile  # ou autre modèle disponible
```

Modèles disponibles :
- `llama-3.3-70b-versatile` (par défaut, recommandé)
- `mixtral-8x7b-32768`
- `llama3-70b-8192`

#### Ajouter des contextes (RAG)

Si vous voulez que le bot utilise des informations de votre portfolio :

Éditez `core/messenger/ai_service.py` dans la méthode `get_system_prompt()` :

```python
def get_system_prompt(self) -> str:
    # Récupérer des infos depuis la BDD
    from core.models import Profile, Projet
    
    profile = Profile.objects.first()
    projets = Projet.objects.all()[:5]
    
    context = f"""Tu es l'assistant virtuel de {profile.user.get_full_name()}.
    
    Compétences principales :
    - {profile.about}
    
    Projets récents :
    {chr(10).join([f'- {p.nom}: {p.description}' for p in projets])}
    """
    
    return context
```

## Fonctionnalités

### ✅ Implémentées

- ✅ Webhook verification (GET)
- ✅ Réception des messages (POST)
- ✅ Déduplication des messages (via `message.mid`)
- ✅ Historique des conversations en BDD
- ✅ Intégration Groq AI
- ✅ Réponses automatiques
- ✅ Gestion des erreurs
- ✅ Typing indicators
- ✅ Mark as seen
- ✅ Support des postbacks (boutons)

### 🔄 À implémenter (optionnel)

- ⏳ Pièces jointes (images, audio)
- ⏳ Quick replies
- ⏳ Templates (cartes, boutons)
- ⏳ Localisation
- ⏳ RAG avec documents PDF
- ⏳ Webhook signature verification (sécurité renforcée)

## Sécurité

### ✅ Mesures en place

- ✅ Tokens stockés dans variables d'environnement
- ✅ HTTPS obligatoire pour le webhook
- ✅ Verify Token pour authentification webhook
- ✅ Logs sans exposition des tokens
- ✅ Déduplication des messages

### 🔒 Recommandations supplémentaires

1. **Vérifier la signature Facebook** (optionnel mais recommandé)
   
   Ajoutez cette vérification dans `views.py` :
   ```python
   import hmac
   import hashlib
   
   def verify_signature(self, request):
       signature = request.META.get('HTTP_X_HUB_SIGNATURE_256', '')
       if not signature:
           return False
       
       sha_name, signature = signature.split('=')
       mac = hmac.new(
           FACEBOOK_APP_SECRET.encode('utf-8'),
           msg=request.body,
           digestmod=hashlib.sha256
       )
       return hmac.compare_digest(mac.hexdigest(), signature)
   ```

2. **Rate limiting** : Limitez le nombre de requêtes par utilisateur

3. **Monitoring** : Surveillez les logs pour détecter les abus

## Débogage

### Logs

Les logs sont disponibles dans :
- Console Django (si DEBUG=True)
- Fichiers de logs (à configurer dans settings.py)

Activez les logs détaillés :
```python
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'core.messenger': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

### Tester le webhook localement

Utilisez **ngrok** pour exposer votre serveur local :

```bash
# Installer ngrok : https://ngrok.com/
ngrok http 8000
```

Copiez l'URL HTTPS fournie par ngrok et utilisez-la comme webhook dans Facebook.

### Erreurs courantes

#### ❌ "Webhook verification failed"
- Vérifiez que `FACEBOOK_VERIFY_TOKEN` correspond exactement
- Vérifiez que l'URL est en HTTPS

#### ❌ "GROQ_API_KEY not set"
- Ajoutez `GROQ_API_KEY` dans `.env`
- Redémarrez le serveur Django

#### ❌ Messages dupliqués
- C'est normal, Facebook peut renvoyer le même événement
- La déduplication via `message.mid` est déjà implémentée

#### ❌ Le bot ne répond pas
- Vérifiez les logs Django
- Vérifiez que le webhook est bien configuré dans Facebook
- Testez manuellement l'API Groq

## Tests

### Test manuel du webhook (GET)

```bash
curl "https://votre-domaine.com/api/facebook/webhook/?hub.mode=subscribe&hub.verify_token=THE_BEAST_VERIFY&hub.challenge=test123"
```

Résultat attendu : `test123`

### Test de l'intégration

1. Envoyez un message à votre Page Facebook
2. Vérifiez les logs Django
3. Vérifiez la réponse du bot
4. Vérifiez l'admin Django pour voir la conversation enregistrée

## Support

Pour toute question ou problème :
- Consultez les logs Django
- Vérifiez la [documentation Facebook Messenger](https://developers.facebook.com/docs/messenger-platform)
- Vérifiez la [documentation Groq](https://console.groq.com/docs)

## Extensions futures

### WhatsApp Business
La même architecture peut être réutilisée pour WhatsApp en créant un module `core/whatsapp/`

### Instagram Direct
Idem pour Instagram Direct Messages

### Telegram
Idem pour Telegram Bot API

Seuls les connecteurs de messagerie changent, la logique métier (IA, BDD) reste la même ! 🚀
