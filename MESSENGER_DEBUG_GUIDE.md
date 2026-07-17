# 🔍 Guide de débogage Facebook Messenger

## Logs détaillés ajoutés

J'ai ajouté des logs **très détaillés** à tous les niveaux pour tracer le flux complet.

### Où voir les logs ?

1. **Console** : Si vous utilisez `python manage.py runserver`
2. **Fichier** : `messenger_debug.log` à la racine du projet
3. **IIS Logs** : Dans les logs IIS de votre serveur

### Flux de logs attendu

Quand un message est envoyé à votre Page Facebook, vous devriez voir :

```
================================================================================
📨 WEBHOOK POST REQUEST - EVENT RECEIVED
================================================================================
[INFO] Method: POST
[INFO] Path: /api/facebook/webhook/
[INFO] Content-Type: application/json
[INFO] Headers: {...}
[INFO] Raw body length: XXX bytes
[INFO] Raw body: {"object":"page",...}
[INFO] Parsed data: {...}

🔧 Initializing MessengerEventHandler...
✅ FacebookGraphAPI initialized
✅ GroqAIService initialized

⚙️ Processing webhook event...
🔄 handle_webhook_event() called
[INFO] Object type: page
[INFO] Number of entries: 1

📋 Processing entry 1/1
[INFO] Number of messaging events: 1

💬 Processing messaging event 1/1
🔍 _process_messaging_event() called
[INFO] Sender ID: 123456789
[INFO] Recipient ID (Page ID): 987654321

📨 Message event detected
================================================================================
📬 _handle_message() called
================================================================================
[INFO] Message ID: mid.xxxxx
[INFO] Message text: Bonjour

[INFO] Duplicate check for mid.xxxxx: False
✅ Processing NEW message from 123456789: Bonjour

👁️ Marking message as seen...
✅ Message marked as seen

⌨️ Showing typing indicator...
✅ Typing indicator shown

💾 Getting/creating conversation...
✅ Found existing conversation (ID: 1) for user 123456789

💾 Saving user message to database...
✅ Message saved with DB ID: 42

📚 Retrieving conversation history...
📚 Retrieved 3 messages from conversation history

================================================================================
🤖 GroqAIService.chat() called
================================================================================
✅ System prompt added (length: 300)
📤 Calling Groq API with 4 messages
[INFO] Model: llama-3.3-70b-versatile
⏳ Sending request to Groq...
✅ Response received from Groq
📥 Groq response length: 150 characters
📥 Groq response preview: Bonjour ! Comment puis-je vous aider...
================================================================================

💾 Saving AI response to database (ID: ai_mid.xxxxx)...
✅ Message saved with DB ID: 43

⌨️ Hiding typing indicator...
✅ Typing indicator hidden

================================================================================
📤 send_text_message() called
================================================================================
[INFO] Recipient ID: 123456789
[INFO] Message text: Bonjour ! Comment puis-je vous aider...
[INFO] API URL: https://graph.facebook.com/v23.0/me/messages
⏳ Sending POST request to Facebook Graph API...
[INFO] Response status code: 200
✅ Message sent successfully to 123456789
================================================================================

✅ Successfully responded to 123456789
================================================================================

✅ Event processed successfully
```

## Points de contrôle

### 1. Le webhook reçoit-il le POST ?

**Cherchez** : `📨 WEBHOOK POST REQUEST - EVENT RECEIVED`

- ✅ **Si présent** : Django reçoit bien les requêtes de Facebook
- ❌ **Si absent** : Le problème est entre Facebook et IIS/Django
  - Vérifiez les logs IIS
  - Vérifiez que l'URL webhook est correcte
  - Vérifiez les pare-feu

### 2. Les données sont-elles correctes ?

**Cherchez** : `Parsed data:`

- ✅ **Si présent** : Les données JSON sont bien reçues
- ❌ **Si vide/erreur** : Problème de parsing JSON

### 3. L'initialisation fonctionne-t-elle ?

**Cherchez** :
- `✅ FacebookGraphAPI initialized`
- `✅ GroqAIService initialized`

- ❌ **Si absent** : Problème de tokens/config
  - Vérifiez `FACEBOOK_PAGE_ACCESS_TOKEN`
  - Vérifiez `GROQ_API_KEY`

### 4. Le message est-il traité ?

**Cherchez** : `📬 _handle_message() called`

- ✅ **Si présent** : Le message est bien extrait
- ❌ **Si absent** : Le format de l'événement Facebook est incorrect

### 5. Groq répond-il ?

**Cherchez** :
- `⏳ Sending request to Groq...`
- `✅ Response received from Groq`

- ❌ **Si erreur** : Problème avec l'API Groq
  - Vérifiez `GROQ_API_KEY`
  - Vérifiez la connectivité internet

### 6. L'envoi à Facebook fonctionne-t-il ?

**Cherchez** :
- `📤 send_text_message() called`
- `✅ Message sent successfully`

- ❌ **Si erreur** : Problème avec l'API Facebook
  - Vérifiez `FACEBOOK_PAGE_ACCESS_TOKEN`
  - Regardez le message d'erreur détaillé

## Commandes utiles

### Voir les logs en temps réel (console)

```bash
# Si vous utilisez runserver
python manage.py runserver

# Les logs s'afficheront dans la console
```

### Voir les logs fichier

```bash
# Windows
type messenger_debug.log

# Suivre en temps réel (avec tail si disponible)
Get-Content messenger_debug.log -Wait -Tail 50
```

### Filtrer les logs

```bash
# Chercher les erreurs
findstr /C:"ERROR" messenger_debug.log
findstr /C:"❌" messenger_debug.log

# Chercher les POST reçus
findstr /C:"WEBHOOK POST REQUEST" messenger_debug.log

# Chercher les messages Groq
findstr /C:"Groq" messenger_debug.log

# Chercher les appels Facebook API
findstr /C:"send_text_message" messenger_debug.log
```

## En cas de problème

### Aucun log POST n'apparaît

**Diagnostic** : Facebook n'envoie pas les événements à Django

**Solutions** :
1. Vérifiez les logs IIS
2. Testez manuellement avec curl :
   ```bash
   curl -X POST https://test-back.unityfianar.site/api/facebook/webhook/ \
     -H "Content-Type: application/json" \
     -d '{"object":"page","entry":[{"messaging":[{"sender":{"id":"123"},"recipient":{"id":"456"},"message":{"mid":"test","text":"Test"}}]}]}'
   ```
3. Vérifiez la configuration du webhook sur Facebook
4. Vérifiez que la page est bien abonnée aux événements

### Erreur lors de l'initialisation

**Cherchez** : `❌ Failed to initialize`

**Solutions** :
1. Vérifiez les variables d'environnement dans `.env`
2. Redémarrez le serveur
3. Vérifiez que les tokens sont valides

### Groq ne répond pas

**Cherchez** : `❌ GROQ API ERROR`

**Solutions** :
1. Vérifiez `GROQ_API_KEY`
2. Testez avec `python test_messenger.py`
3. Vérifiez la connectivité internet
4. Vérifiez les quotas Groq

### Facebook API erreur

**Cherchez** : `❌ FACEBOOK API HTTP ERROR`

**Solutions** :
1. Regardez le `Response text` dans les logs
2. Vérifiez `FACEBOOK_PAGE_ACCESS_TOKEN`
3. Vérifiez que le token n'est pas expiré
4. Vérifiez les permissions de la page

## Test manuel complet

### 1. Test GET (vérification)

```bash
curl "https://test-back.unityfianar.site/api/facebook/webhook/?hub.mode=subscribe&hub.verify_token=VOTRE_TOKEN&hub.challenge=test123"
```

**Attendu** : `test123`

### 2. Test POST (événement)

```bash
curl -X POST https://test-back.unityfianar.site/api/facebook/webhook/ \
  -H "Content-Type: application/json" \
  -d '{
    "object": "page",
    "entry": [{
      "messaging": [{
        "sender": {"id": "123456789"},
        "recipient": {"id": "987654321"},
        "message": {
          "mid": "test_mid_123",
          "text": "Test message"
        }
      }]
    }]
  }'
```

**Attendu** : Status 200 + logs détaillés

### 3. Vérifier la base de données

```bash
python manage.py shell
```

```python
from core.messenger.models import MessengerConversation, MessengerMessage

# Voir les conversations
for conv in MessengerConversation.objects.all():
    print(f"User: {conv.facebook_user_id}, Messages: {conv.messages.count()}")

# Voir les derniers messages
for msg in MessengerMessage.objects.order_by('-created_at')[:5]:
    print(f"[{msg.role}] {msg.content[:50]}...")
```

## Niveaux de logs

Les logs utilisent ces émojis pour faciliter la lecture :

- 🔍 = Début d'analyse
- 📨 = Requête reçue
- 🔧 = Initialisation
- ✅ = Succès
- ❌ = Erreur
- ⚠️ = Avertissement
- 📤 = Envoi
- 📥 = Réception
- 💬 = Message
- 🤖 = Groq AI
- 👁️ = Mark as seen
- ⌨️ = Typing indicator
- 💾 = Base de données
- 📚 = Historique
- 🔄 = Traitement
- ⏳ = En attente

## Après vos tests

Une fois que tout fonctionne, **n'oubliez pas de** :

1. Partager les logs avec moi pour analyse
2. Vérifier que le bot répond bien sur Messenger
3. Consulter `messenger_debug.log` pour l'historique complet

Les logs me permettront de voir **exactement** où le flux s'arrête ! 🔍
