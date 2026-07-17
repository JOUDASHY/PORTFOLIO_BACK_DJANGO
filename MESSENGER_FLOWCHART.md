# 🔄 Facebook Messenger Bot - Diagrammes de flux

## Architecture globale

```
┌─────────────────┐
│  Utilisateur    │
│   Messenger     │
└────────┬────────┘
         │
         │ Message "Bonjour"
         ▼
┌─────────────────────────┐
│  Facebook Platform      │
│  (Meta Servers)         │
└────────┬────────────────┘
         │
         │ POST /api/facebook/webhook/
         ▼
┌──────────────────────────────────┐
│   Django Backend                 │
│                                  │
│  ┌───────────────────────────┐  │
│  │  FacebookWebhookView      │  │
│  │  (views.py)               │  │
│  └──────────┬────────────────┘  │
│             │                    │
│             │ handle_webhook     │
│             ▼                    │
│  ┌───────────────────────────┐  │
│  │  MessengerEventHandler    │  │
│  │  (messenger.py)           │  │
│  └──────────┬────────────────┘  │
│             │                    │
│             ├──→ Déduplication   │
│             │    (message.mid)   │
│             │                    │
│             ├──→ Get/Create      │
│             │    Conversation    │
│             │    (BDD)           │
│             │                    │
│             ├──→ Get History     │
│             │    (BDD)           │
│             │                    │
│             ▼                    │
│  ┌───────────────────────────┐  │
│  │  GroqAIService            │  │
│  │  (ai_service.py)          │  │
│  └──────────┬────────────────┘  │
│             │                    │
│             │ chat([messages])   │
│             ▼                    │
│  ┌───────────────────────────┐  │
│  │  Groq API                 │  │
│  │  (externe)                │  │
│  └──────────┬────────────────┘  │
│             │                    │
│             │ Réponse IA         │
│             ▼                    │
│  ┌───────────────────────────┐  │
│  │  Save Message             │  │
│  │  (BDD)                    │  │
│  └──────────┬────────────────┘  │
│             │                    │
│             ▼                    │
│  ┌───────────────────────────┐  │
│  │  FacebookGraphAPI         │  │
│  │  (services.py)            │  │
│  └──────────┬────────────────┘  │
│             │                    │
│             │ send_text_message  │
│             ▼                    │
└──────────────────────────────────┘
         │
         │ Réponse via Graph API
         ▼
┌─────────────────────────┐
│  Facebook Platform      │
└────────┬────────────────┘
         │
         │ Afficher réponse
         ▼
┌─────────────────┐
│  Utilisateur    │
│   Messenger     │
└─────────────────┘
```

---

## Flux de traitement d'un message

```
START
  │
  ▼
┌──────────────────────────┐
│ Facebook envoie POST     │
│ au webhook               │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│ Vérifier object=="page"  │
└──────────┬───────────────┘
           │
           ▼ Non
      [Ignorer]
           │
           ▼ Oui
┌──────────────────────────┐
│ Extraire sender.id       │
│ Extraire message.text    │
│ Extraire message.mid     │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│ Message déjà traité ?    │
│ (check message.mid)      │
└──────────┬───────────────┘
           │
           ▼ Oui
      [Ignorer - Doublon]
           │
           ▼ Non
┌──────────────────────────┐
│ Mark as seen             │
│ Show typing indicator    │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│ Get/Create Conversation  │
│ (facebook_user_id,       │
│  page_id)                │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│ Save user message        │
│ (role='user')            │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│ Get conversation history │
│ (last 10 messages)       │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│ Prepare messages for AI  │
│ [system, user1, asst1,   │
│  user2, ...]             │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│ Call Groq API            │
│ with conversation        │
└──────────┬───────────────┘
           │
           ▼ Error
      [Fallback message]
           │
           ▼ Success
┌──────────────────────────┐
│ Save AI response         │
│ (role='assistant')       │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│ Hide typing indicator    │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│ Send via Facebook        │
│ Graph API                │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│ Return 200 OK            │
│ to Facebook              │
└──────────┬───────────────┘
           │
           ▼
          END
```

---

## Webhook Verification (GET)

```
START
  │
  ▼
┌──────────────────────────┐
│ Facebook envoie GET      │
│ ?hub.mode=subscribe      │
│ ?hub.verify_token=XXX    │
│ ?hub.challenge=123       │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│ hub.mode == "subscribe"  │
│ ?                        │
└──────────┬───────────────┘
           │
           ▼ Non
      [Return 403]
           │
           ▼ Oui
┌──────────────────────────┐
│ hub.verify_token ==      │
│ FACEBOOK_VERIFY_TOKEN ?  │
└──────────┬───────────────┘
           │
           ▼ Non
      [Return 403]
           │
           ▼ Oui
┌──────────────────────────┐
│ Return hub.challenge     │
│ (200 OK)                 │
└──────────┬───────────────┘
           │
           ▼
          END
          
[Webhook vérifié ✓]
```

---

## Base de données - Relations

```
┌─────────────────────────────┐
│  MessengerConversation      │
├─────────────────────────────┤
│  id (PK)                    │
│  facebook_user_id           │◄─────┐
│  page_id                    │      │
│  created_at                 │      │ FK
│  updated_at                 │      │
└─────────────────────────────┘      │
                                     │
                                     │
                ┌────────────────────┘
                │
                │
┌─────────────────────────────┐
│  MessengerMessage           │
├─────────────────────────────┤
│  id (PK)                    │
│  conversation_id (FK) ──────┘
│  message_id (unique)        │ ◄── Déduplication
│  role (user|assistant)      │
│  content                    │
│  created_at                 │
└─────────────────────────────┘
```

---

## Exemple de conversation

```
Utilisateur: "Bonjour"
    ↓
[Sauvegarde en BDD]
    ↓
MessengerMessage {
  conversation_id: 1,
  message_id: "mid.xxx",
  role: "user",
  content: "Bonjour"
}
    ↓
[Envoi à Groq]
    ↓
Groq: "Bonjour ! Comment puis-je vous aider ?"
    ↓
[Sauvegarde en BDD]
    ↓
MessengerMessage {
  conversation_id: 1,
  message_id: "ai_mid.xxx",
  role: "assistant",
  content: "Bonjour ! Comment puis-je vous aider ?"
}
    ↓
[Envoi via Facebook]
    ↓
Utilisateur voit: "Bonjour ! Comment puis-je vous aider ?"
```

---

## Configuration - Flow

```
1. Créer App Facebook
   └─→ Obtenir Page Access Token
   
2. Ajouter dans .env:
   ├─→ FACEBOOK_PAGE_ACCESS_TOKEN
   ├─→ FACEBOOK_VERIFY_TOKEN
   ├─→ FACEBOOK_PAGE_ID
   └─→ GROQ_API_KEY (déjà fait)
   
3. Migrer BDD:
   └─→ python manage.py migrate
   
4. Tester config:
   └─→ python test_messenger.py
   
5. Configurer Webhook Facebook:
   ├─→ URL: https://domain.com/api/facebook/webhook/
   └─→ Verify Token: [même que .env]
   
6. Abonner aux événements:
   ├─→ messages ✓
   └─→ messaging_postbacks ✓
   
7. Tester:
   └─→ Envoyer message à Page Facebook
       └─→ Bot répond automatiquement ✓
```

---

## Gestion des erreurs

```
Message reçu
    │
    ▼
Try:
    │
    ├─→ Déduplication
    ├─→ BDD operations
    ├─→ Groq API call
    └─→ Facebook send
    │
    ▼ Exception caught
Except:
    │
    ├─→ Log error
    │   (sans exposer tokens)
    │
    ├─→ Try send fallback:
    │   "Désolé, une erreur..."
    │
    └─→ Return 200 OK
        (pour éviter retry Facebook)
```

---

## Déduplication

```
Message arrive (mid="abc123")
    │
    ▼
┌─────────────────────────┐
│ Check BDD:              │
│ MessengerMessage.       │
│   filter(               │
│     message_id="abc123" │
│   ).exists()            │
└──────────┬──────────────┘
           │
           ▼
    ┌─────┴──────┐
    │            │
   Oui          Non
    │            │
    ▼            ▼
[Ignorer]   [Traiter]
```

---

## Personnalisation - Flow

```
1. Éditer core/messenger/ai_service.py
   
2. Modifier get_system_prompt():
   │
   ├─→ Option A: Prompt statique
   │   return "Tu es..."
   │
   └─→ Option B: Prompt dynamique
       ├─→ Récupérer Profile
       ├─→ Récupérer Projets
       └─→ Générer contexte
       
3. Redémarrer serveur:
   python manage.py runserver
   
4. Tester:
   Envoyer message → Nouveau comportement ✓
```

---

## Monitoring

```
Logs Django (Console)
    │
    ├─→ INFO: Message received
    ├─→ INFO: Groq API called
    ├─→ INFO: Response sent
    └─→ ERROR: (si erreur)
    
Admin Django (/admin/)
    │
    └─→ Messenger Conversations
        │
        ├─→ Liste conversations
        ├─→ Détail messages
        └─→ Timestamps
        
BDD Stats (Shell)
    │
    ├─→ Count conversations
    ├─→ Count messages
    └─→ Messages par user
```

---

## Cycle de vie complet

```
Installation
    ↓
Configuration (.env)
    ↓
Migration BDD
    ↓
Test local
    ↓
Config Facebook
    ↓
Deploy HTTPS
    ↓
Config Webhook
    ↓
Test production
    ↓
Monitoring
    ↓
Personnalisation
    ↓
Maintenance
```

---

**💡 Conseil** : Imprimez ce diagramme pour référence rapide !
