# 🚀 Facebook Messenger Bot - Guide de Déploiement

## ✅ État Actuel (Local)

### Fichiers Créés ✓
Tous les fichiers nécessaires sont présents localement :

```
core/messenger/
├── __init__.py           ✓
├── admin.py              ✓
├── ai_service.py         ✓ (intégration Groq)
├── apps.py               ✓
├── messenger.py          ✓ (traitement des événements)
├── models.py             ✓
├── services.py           ✓ (Facebook Graph API)
├── urls.py               ✓
├── views.py              ✓ (webhook GET/POST)
└── README.md             ✓

core/models.py            ✓ (MessengerConversation, MessengerMessage ajoutés)
core/urls.py              ✓ (routes /api/facebook/)
core/migrations/0049_messenger_models.py  ✓
back_django_portfolio_me/settings.py      ✓ (logging, FB config)
.env.example              ✓ (variables Facebook documentées)
```

### Configuration ✓
- Logging détaillé configuré (console + fichier `messenger_debug.log`)
- Module `core.messenger` ajouté dans `INSTALLED_APPS`
- Variables d'environnement Facebook dans settings.py
- Routes webhook configurées : `/api/facebook/webhook/`

---

## 🎯 Étapes de Déploiement sur le Serveur

### Étape 1: Pousser le Code sur Git

```bash
# Sur votre machine locale (C:\Users\Nilsen Un-it\PORTFOLIO_BACK_DJANGO)
git add .
git commit -m "Add Facebook Messenger bot integration with Groq AI"
git push origin main
```

### Étape 2: Mettre à Jour le Serveur

```powershell
# Sur le serveur (C:\inetpub\wwwroot\test_py)
cd C:\inetpub\wwwroot\test_py
git pull
```

### Étape 3: Appliquer la Migration

```powershell
# Activer l'environnement virtuel
.\venv\Scripts\activate

# Appliquer les migrations
python manage.py migrate

# Vérifier que les tables sont créées
python manage.py dbshell
# Puis dans MySQL:
SHOW TABLES LIKE 'core_messenger%';
# Devrait afficher:
#   core_messengerconversation
#   core_messengermessage
EXIT;
```

### Étape 4: Configurer les Variables d'Environnement

Éditer le fichier `.env` sur le serveur :

```env
# Ajouter ces lignes (obtenir les valeurs depuis Facebook Developers)
FACEBOOK_PAGE_ACCESS_TOKEN=EAABxxxxxxxxxxxxxxxx
FACEBOOK_VERIFY_TOKEN=THE_BEAST_VERIFY
FACEBOOK_PAGE_ID=123456789012345

# Vérifier que Groq est configuré
GROQ_API_KEY=gsk_your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

**Comment obtenir ces valeurs :**

1. **FACEBOOK_PAGE_ACCESS_TOKEN** :
   - Aller sur https://developers.facebook.com/apps
   - Sélectionner votre app (ou créer une nouvelle)
   - Aller dans "Messenger" > "Settings"
   - Générer un token pour votre Page

2. **FACEBOOK_VERIFY_TOKEN** :
   - Choisir une chaîne sécurisée (ex: `THE_BEAST_VERIFY_2026`)
   - Vous devrez l'utiliser lors de la configuration du webhook

3. **FACEBOOK_PAGE_ID** :
   - Aller sur votre Page Facebook
   - Paramètres > À propos > ID de la Page

### Étape 5: Redémarrer le Serveur

```powershell
# Redémarrer IIS ou le pool d'application
iisreset
# OU redémarrer le pool d'application spécifique depuis IIS Manager
```

### Étape 6: Tester le Webhook Localement

```powershell
# Tester la vérification GET
curl "https://test-back.unityfianar.site/api/facebook/webhook/?hub.mode=subscribe&hub.verify_token=THE_BEAST_VERIFY&hub.challenge=TEST123"
# Devrait retourner: TEST123

# Vérifier les logs
type messenger_debug.log
```

### Étape 7: Configurer le Webhook sur Facebook

1. Aller sur https://developers.facebook.com/apps
2. Sélectionner votre app
3. Aller dans "Messenger" > "Settings"
4. Section "Webhooks"
5. Cliquer "Add Callback URL"
6. Entrer :
   - **Callback URL**: `https://test-back.unityfianar.site/api/facebook/webhook/`
   - **Verify Token**: `THE_BEAST_VERIFY` (celui dans votre .env)
7. Sélectionner les événements à recevoir :
   - ✅ `messages`
   - ✅ `messaging_postbacks`
8. Cliquer "Verify and Save"

### Étape 8: Abonner la Page aux Webhooks

1. Dans la même section "Webhooks"
2. Cliquer "Add Subscriptions"
3. Sélectionner votre Page Facebook
4. Cocher les événements souhaités
5. Sauvegarder

### Étape 9: Tester avec un Vrai Message

1. Ouvrir Facebook Messenger
2. Envoyer un message à votre Page
3. Vérifier les logs sur le serveur :

```powershell
# Voir les logs en temps réel
type messenger_debug.log
```

**Logs attendus :**
```
[INFO] 📨 WEBHOOK POST REQUEST - EVENT RECEIVED
[INFO] Method: POST
[INFO] Path: /api/facebook/webhook/
[INFO] Parsed data: {...}
[INFO] 🔧 Initializing MessengerEventHandler...
[INFO] 🤖 Calling Groq AI...
[INFO] 📤 Sending response to Facebook...
[INFO] ✅ Event processed successfully
```

---

## 🔍 Vérification et Tests

### Test 1: Vérifier les Tables de Base de Données

```powershell
python manage.py dbshell
```

```sql
-- Vérifier la structure des tables
DESCRIBE core_messengerconversation;
DESCRIBE core_messengermessage;

-- Compter les enregistrements
SELECT COUNT(*) FROM core_messengerconversation;
SELECT COUNT(*) FROM core_messengermessage;
```

### Test 2: Vérifier l'Endpoint Webhook

```powershell
# Test GET (vérification)
curl "https://test-back.unityfianar.site/api/facebook/webhook/?hub.mode=subscribe&hub.verify_token=THE_BEAST_VERIFY&hub.challenge=HELLO"
# Devrait retourner: HELLO

# Test POST (simuler un événement)
curl -X POST https://test-back.unityfianar.site/api/facebook/webhook/ `
  -H "Content-Type: application/json" `
  -d '{\"object\":\"page\",\"entry\":[{\"messaging\":[{\"sender\":{\"id\":\"12345\"},\"recipient\":{\"id\":\"67890\"},\"message\":{\"mid\":\"test_mid_123\",\"text\":\"Bonjour\"}}]}]}'
```

### Test 3: Tester l'Admin Django

1. Aller sur : `https://test-back.unityfianar.site/admin/`
2. Se connecter
3. Vérifier que les sections apparaissent :
   - Messenger Conversations
   - Messenger Messages

### Test 4: Script de Test Python

Créer `test_messenger_local.py` :

```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back_django_portfolio_me.settings')
django.setup()

from core.models import MessengerConversation, MessengerMessage

# Test création conversation
conv = MessengerConversation.objects.create(
    facebook_user_id="test_user_12345",
    page_id="test_page_67890"
)
print(f"✅ Conversation créée: {conv}")

# Test création message
msg = MessengerMessage.objects.create(
    conversation=conv,
    message_id="test_mid_001",
    role="user",
    content="Test message"
)
print(f"✅ Message créé: {msg}")

# Test récupération
messages = conv.messages.all()
print(f"✅ Messages dans la conversation: {messages.count()}")

# Nettoyage
conv.delete()
print("✅ Test terminé et nettoyé")
```

Exécuter :
```powershell
python test_messenger_local.py
```

---

## 🐛 Dépannage

### Erreur: "No migrations to apply"

**Symptôme :**
```
Your models in app(s): 'core' have changes that are not yet reflected in a migration
```

**Solution :**
```powershell
# Vérifier que le fichier de migration existe
dir core\migrations\0049_messenger_models.py

# Si absent, le copier depuis local vers serveur
# Ou régénérer:
python manage.py makemigrations core
python manage.py migrate
```

### Erreur: "Conflicting migrations detected"

**Symptôme :**
```
CommandError: Conflicting migrations detected; multiple leaf nodes
```

**Solution :**
```powershell
python manage.py makemigrations --merge
python manage.py migrate
```

### Erreur: "Webhook verification failed"

**Symptôme :**
Logs montrent : `❌ Webhook verification failed`

**Solutions :**
1. Vérifier que `FACEBOOK_VERIFY_TOKEN` est bien dans `.env`
2. Vérifier que le token correspond exactement à celui configuré sur Facebook
3. Vérifier les logs : `type messenger_debug.log`

### Erreur: "No response from webhook"

**Symptôme :**
Message envoyé sur Messenger, mais pas de réponse

**Checklist :**
1. ✅ Le webhook GET retourne 200 ?
2. ✅ Le webhook POST apparaît dans les logs ?
3. ✅ `FACEBOOK_PAGE_ACCESS_TOKEN` est valide ?
4. ✅ `GROQ_API_KEY` est configuré ?
5. ✅ Les tables existent en base de données ?

**Vérifier les logs :**
```powershell
# Voir les dernières lignes
Get-Content messenger_debug.log -Tail 50

# Surveiller en temps réel
Get-Content messenger_debug.log -Wait -Tail 20
```

### Avertissement: "UnicodeEncodeError" dans les logs

**Symptôme :**
```
UnicodeEncodeError: 'charmap' codec can't encode character '🔍'
```

**Explication :**
Ceci est cosmétique. Les emojis ne s'affichent pas correctement dans la console Windows CMD, mais le fichier `messenger_debug.log` les enregistre correctement.

**Solution (optionnelle) :**
Utiliser PowerShell au lieu de CMD pour un meilleur support Unicode.

---

## 📊 Monitoring en Production

### Logs à Surveiller

```powershell
# Voir les logs du webhook
type messenger_debug.log | findstr "WEBHOOK"

# Voir les erreurs
type messenger_debug.log | findstr "ERROR"

# Voir les appels Groq
type messenger_debug.log | findstr "Groq"

# Compter les messages traités aujourd'hui
type messenger_debug.log | findstr "Event processed successfully" | find /c /v ""
```

### Requêtes SQL Utiles

```sql
-- Conversations actives
SELECT * FROM core_messengerconversation 
ORDER BY updated_at DESC 
LIMIT 10;

-- Messages récents
SELECT 
    m.created_at,
    m.role,
    LEFT(m.content, 50) as content_preview,
    c.facebook_user_id
FROM core_messengermessage m
JOIN core_messengerconversation c ON m.conversation_id = c.id
ORDER BY m.created_at DESC
LIMIT 20;

-- Statistiques
SELECT 
    DATE(created_at) as date,
    COUNT(*) as message_count,
    SUM(CASE WHEN role='user' THEN 1 ELSE 0 END) as user_messages,
    SUM(CASE WHEN role='assistant' THEN 1 ELSE 0 END) as bot_messages
FROM core_messengermessage
GROUP BY DATE(created_at)
ORDER BY date DESC;
```

---

## 🎓 Utilisation du Bot

### Fonctionnalités Actuelles

✅ Réception de messages texte Messenger
✅ Traitement via Groq AI (contexte portfolio)
✅ Réponses automatiques avec historique de conversation
✅ Déduplication des messages (via `message_id`)
✅ Logging détaillé de chaque étape
✅ Gestion d'erreurs robuste

### Contexte Fourni à l'IA

Le bot dispose automatiquement du contexte suivant :
- Nom : Nilsen Un-it
- Rôle : Développeur Full Stack
- Technologies : Django, React, MySQL, etc.
- Portfolio : https://portfolio.unityfianar.site

### Personnalisation

Pour modifier le contexte IA, éditer :
`core/messenger/ai_service.py` → méthode `_build_system_message()`

---

## 📚 Documentation Supplémentaire

- **Architecture** : `core/messenger/README.md`
- **API Facebook** : https://developers.facebook.com/docs/messenger-platform
- **Groq API** : https://console.groq.com/docs

---

## ✅ Checklist Finale

Avant de déclarer l'intégration terminée :

- [ ] Code poussé sur Git
- [ ] Serveur mis à jour (`git pull`)
- [ ] Migration appliquée (`migrate`)
- [ ] Variables `.env` configurées
- [ ] Tables créées en base de données
- [ ] Webhook GET retourne 200
- [ ] Webhook configuré sur Facebook
- [ ] Page abonnée aux webhooks
- [ ] Test d'un message réel réussi
- [ ] Logs montrent le flux complet
- [ ] Admin Django accessible
- [ ] Documentation lue et comprise

---

**Date de création :** 2026-07-17
**Dernière mise à jour :** 2026-07-17
**Statut :** Prêt pour déploiement 🚀
