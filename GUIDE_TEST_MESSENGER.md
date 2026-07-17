# 🧪 Guide de Test - Bot Facebook Messenger

## 📋 Tests à Faire (Dans l'Ordre)

### ✅ TEST 1 : Vérifier les Fichiers Localement

```powershell
# Vérifier que tous les fichiers existent
dir core\messenger
dir core\migrations\0049_messenger_models.py
```

**Résultat attendu :** Tous les fichiers sont présents

---

### ✅ TEST 2 : Test Automatique Local

```powershell
# Dans votre dossier local
cd "C:\Users\Nilsen Un-it\PORTFOLIO_BACK_DJANGO"

# Activer l'environnement virtuel (si vous en avez un)
# .\venv\Scripts\activate

# Lancer le script de test
python test_messenger_integration.py
```

**Résultat attendu :**
```
🎉 TOUS LES TESTS SONT PASSÉS !
Score: 6/6 tests réussis
```

**Si un test échoue :**
- Test "Variables d'environnement" → Vérifier votre `.env` local
- Test "Modèles BDD" → Faire `python manage.py migrate`
- Test "Groq AI" → Vérifier `GROQ_API_KEY` dans `.env`

---

### ✅ TEST 3 : Pousser sur Git

```bash
git add .
git commit -m "Add Facebook Messenger bot integration"
git push origin main
```

**Résultat attendu :** Code poussé sans erreur

---

### ✅ TEST 4 : Déployer sur le Serveur

```powershell
# Connexion au serveur de production
cd C:\inetpub\wwwroot\test_py

# Récupérer le code
git pull

# Vérifier que les fichiers sont arrivés
dir core\messenger
dir core\migrations\0049_messenger_models.py
```

**Résultat attendu :** Tous les fichiers présents sur le serveur

---

### ✅ TEST 5 : Migration Base de Données

```powershell
# Toujours sur le serveur
cd C:\inetpub\wwwroot\test_py
.\venv\Scripts\activate

# Appliquer la migration
python manage.py migrate
```

**Résultat attendu :**
```
Running migrations:
  Applying core.0049_messenger_models... OK
```

**Vérifier les tables :**
```powershell
python manage.py dbshell
```

```sql
SHOW TABLES LIKE 'core_messenger%';
-- Devrait afficher :
--   core_messengerconversation
--   core_messengermessage

EXIT;
```

---

### ✅ TEST 6 : Configurer les Variables d'Environnement

**IMPORTANT :** Avant de continuer, vous devez obtenir les tokens Facebook.

#### 6.1. Obtenir le Page Access Token

1. Aller sur https://developers.facebook.com/apps
2. Sélectionner votre application (ou en créer une)
3. Dans le menu gauche : **Messenger** → **Settings**
4. Section **"Access Tokens"**
5. Sélectionner votre Page Facebook
6. Cliquer **"Generate Token"**
7. **Copier le token** (commence par `EAAB...`)

#### 6.2. Choisir un Verify Token

Choisir une chaîne sécurisée, par exemple :
```
THE_BEAST_VERIFY_2026
```

#### 6.3. Obtenir le Page ID

1. Aller sur votre Page Facebook
2. Menu **Paramètres** → **À propos**
3. Copier l'**ID de la Page**

#### 6.4. Éditer le fichier .env sur le serveur

```powershell
# Sur le serveur
notepad C:\inetpub\wwwroot\test_py\.env
```

**Ajouter ces lignes :**
```env
# Facebook Messenger Bot
FACEBOOK_PAGE_ACCESS_TOKEN=EAAB_votre_token_ici
FACEBOOK_VERIFY_TOKEN=THE_BEAST_VERIFY_2026
FACEBOOK_PAGE_ID=123456789012345

# Vérifier que Groq est déjà là
GROQ_API_KEY=gsk_votre_cle_ici
```

**Sauvegarder et fermer**

---

### ✅ TEST 7 : Redémarrer le Serveur

```powershell
iisreset
```

**Attendre 30 secondes** que le serveur redémarre.

---

### ✅ TEST 8 : Test Automatique sur le Serveur

```powershell
cd C:\inetpub\wwwroot\test_py
.\venv\Scripts\activate
python test_messenger_integration.py
```

**Résultat attendu :**
```
🎉 TOUS LES TESTS SONT PASSÉS !
Score: 6/6 tests réussis
```

**Si ça échoue :**
- Vérifier que les tokens sont bien dans `.env`
- Vérifier qu'il n'y a pas d'espace avant/après les tokens
- Relancer `iisreset`

---

### ✅ TEST 9 : Test Webhook GET (Vérification)

Ce test vérifie que Facebook peut valider votre webhook.

```powershell
curl "https://test-back.unityfianar.site/api/facebook/webhook/?hub.mode=subscribe&hub.verify_token=THE_BEAST_VERIFY_2026&hub.challenge=HELLO"
```

**Résultat attendu :**
```
HELLO
```

**Si ça ne marche pas :**
- Vérifier que le `verify_token` correspond à celui dans `.env`
- Vérifier les logs : `type C:\inetpub\wwwroot\test_py\messenger_debug.log`
- Vérifier que le serveur a bien redémarré

---

### ✅ TEST 10 : Configurer le Webhook sur Facebook

Maintenant on configure Facebook pour qu'il envoie les messages à votre serveur.

#### 10.1. Ajouter le Callback URL

1. Aller sur https://developers.facebook.com/apps
2. Sélectionner votre app
3. Menu gauche : **Messenger** → **Settings**
4. Section **Webhooks**
5. Cliquer **"Add Callback URL"**
6. Remplir :
   - **Callback URL :** `https://test-back.unityfianar.site/api/facebook/webhook/`
   - **Verify Token :** `THE_BEAST_VERIFY_2026` (celui dans votre `.env`)
7. Cliquer **"Verify and Save"**

**Résultat attendu :**
- ✅ Message "Success" ou "Verified"
- Le webhook apparaît maintenant dans la liste

**Si la vérification échoue :**
- Vérifier que le TEST 9 fonctionne (curl)
- Vérifier que le token est exactement le même
- Regarder les logs sur le serveur

#### 10.2. Sélectionner les Événements

Toujours dans **Webhooks** :
1. Cocher :
   - ✅ **messages**
   - ✅ **messaging_postbacks**
2. Cliquer **"Save"**

#### 10.3. Abonner la Page

1. Section **"Add Subscriptions"** ou **"Subscribe"**
2. Sélectionner votre **Page Facebook**
3. Cocher les événements
4. Sauvegarder

**Résultat attendu :**
- Status : **"Subscribed"** ✅

---

### ✅ TEST 11 : Test avec un Vrai Message (LE TEST FINAL !)

C'est le moment de vérité ! 🎉

#### 11.1. Envoyer un Message

1. Ouvrir **Facebook Messenger** (mobile ou https://www.facebook.com/messages)
2. Chercher votre **Page Facebook**
3. Envoyer un message : **"Bonjour"**

#### 11.2. Vérifier les Logs en Temps Réel

Sur le serveur, ouvrir une fenêtre PowerShell et suivre les logs :

```powershell
cd C:\inetpub\wwwroot\test_py
Get-Content messenger_debug.log -Wait -Tail 30
```

**Ce que vous devriez voir défiler :**
```
[INFO] ===============================================
[INFO] 📨 WEBHOOK POST REQUEST - EVENT RECEIVED
[INFO] ===============================================
[INFO] Method: POST
[INFO] Path: /api/facebook/webhook/
[INFO] Parsed data: {...}
[INFO] 🔧 Initializing MessengerEventHandler...
[INFO] Processing message from user...
[INFO] 🤖 Calling Groq AI...
[INFO] Groq response received
[INFO] 📤 Sending response to Facebook...
[INFO] ✅ Response sent successfully
[INFO] ✅ Event processed successfully
```

#### 11.3. Vérifier la Réponse

Dans Messenger, vous devriez recevoir une réponse du bot en **2-5 secondes**.

**Exemple de réponse attendue :**
```
Bonjour ! Je suis l'assistant virtuel de Nilsen Un-it, 
développeur Full Stack. Comment puis-je vous aider ?
```

---

### ✅ TEST 12 : Vérifier la Base de Données

```powershell
python manage.py dbshell
```

```sql
-- Voir les conversations
SELECT * FROM core_messengerconversation;

-- Voir les messages
SELECT * FROM core_messengermessage ORDER BY created_at DESC LIMIT 5;

-- Compter les messages
SELECT COUNT(*) FROM core_messengermessage;

EXIT;
```

**Résultat attendu :**
- Au moins 1 conversation
- Au moins 2 messages (1 user + 1 assistant)

---

### ✅ TEST 13 : Test de Conversation

Envoyez plusieurs messages pour tester l'historique :

1. **"Bonjour"** → Le bot répond
2. **"Quelles sont tes compétences ?"** → Le bot répond avec contexte
3. **"Tu connais Django ?"** → Le bot répond en utilisant l'historique
4. **"Merci"** → Le bot répond

**Vérifier que :**
- ✅ Toutes les réponses arrivent
- ✅ Le bot se souvient du contexte (historique)
- ✅ Les réponses sont cohérentes
- ✅ Temps de réponse < 5 secondes

---

### ✅ TEST 14 : Vérifier l'Admin Django

1. Aller sur : `https://test-back.unityfianar.site/admin/`
2. Se connecter avec vos identifiants admin
3. Vérifier les sections :
   - **Messenger Conversations** → Vos conversations apparaissent
   - **Messenger Messages** → Tous les messages sont là

---

## 🐛 Tests de Dépannage

### Si le bot ne répond pas :

#### Test A : Vérifier que le POST arrive

```powershell
type C:\inetpub\wwwroot\test_py\messenger_debug.log | findstr "WEBHOOK POST"
```

**Si rien n'apparaît :**
- Le webhook Facebook n'est pas configuré correctement
- Retourner au TEST 10

#### Test B : Vérifier les erreurs

```powershell
type C:\inetpub\wwwroot\test_py\messenger_debug.log | findstr "ERROR"
```

**Si des erreurs apparaissent :**
- Lire l'erreur et la corriger
- Erreurs communes :
  - `FACEBOOK_PAGE_ACCESS_TOKEN not found` → Vérifier `.env`
  - `Groq API error` → Vérifier `GROQ_API_KEY`
  - `Database error` → Vérifier migration (TEST 5)

#### Test C : Test Manuel du Webhook POST

```powershell
curl -X POST https://test-back.unityfianar.site/api/facebook/webhook/ `
  -H "Content-Type: application/json" `
  -d '{\"object\":\"page\",\"entry\":[{\"messaging\":[{\"sender\":{\"id\":\"12345\"},\"recipient\":{\"id\":\"67890\"},\"message\":{\"mid\":\"test_123\",\"text\":\"Test\"}}]}]}'
```

**Vérifier les logs immédiatement après.**

---

## 📊 Checklist Finale de Validation

Cochez chaque test réussi :

- [ ] TEST 1 : Fichiers présents localement ✓
- [ ] TEST 2 : Script de test local passe ✓
- [ ] TEST 3 : Code poussé sur Git ✓
- [ ] TEST 4 : Code déployé sur serveur ✓
- [ ] TEST 5 : Migration appliquée ✓
- [ ] TEST 6 : Variables .env configurées ✓
- [ ] TEST 7 : Serveur redémarré ✓
- [ ] TEST 8 : Script de test serveur passe ✓
- [ ] TEST 9 : Webhook GET fonctionne ✓
- [ ] TEST 10 : Webhook configuré sur Facebook ✓
- [ ] TEST 11 : Message test reçu une réponse ✓
- [ ] TEST 12 : BDD contient les messages ✓
- [ ] TEST 13 : Conversation avec historique OK ✓
- [ ] TEST 14 : Admin Django affiche les données ✓

**Si tous les tests sont cochés : 🎉 LE BOT EST OPÉRATIONNEL !**

---

## 📝 Exemple de Session de Test Complète

```powershell
# Sur le serveur de production
cd C:\inetpub\wwwroot\test_py

# 1. Déployer
git pull

# 2. Migrer
.\venv\Scripts\activate
python manage.py migrate

# 3. Tester
python test_messenger_integration.py

# 4. Vérifier webhook
curl "https://test-back.unityfianar.site/api/facebook/webhook/?hub.mode=subscribe&hub.verify_token=THE_BEAST_VERIFY_2026&hub.challenge=TEST"

# 5. Suivre les logs en temps réel
Get-Content messenger_debug.log -Wait -Tail 30

# 6. Dans une autre fenêtre, envoyer un message via Messenger
# 7. Observer les logs défiler
# 8. Vérifier la réponse dans Messenger
```

---

## 🎯 Temps Estimé pour Tous les Tests

- Tests automatiques : **5 minutes**
- Configuration Facebook : **5 minutes**
- Tests manuels : **5 minutes**
- **TOTAL : environ 15 minutes**

---

## 💡 Conseils

1. **Gardez les logs ouverts** pendant les tests avec `Get-Content -Wait`
2. **Testez d'abord le GET** (TEST 9) avant de configurer Facebook
3. **Utilisez votre propre compte** Messenger pour tester
4. **Attendez 2-5 secondes** entre chaque message (temps de traitement Groq)
5. **Sauvegardez les logs** de la première réussite pour référence

---

**Bon test ! 🚀**
