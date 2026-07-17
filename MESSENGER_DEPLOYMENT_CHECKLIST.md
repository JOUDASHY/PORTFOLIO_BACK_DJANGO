# ✅ Checklist de Déploiement - Facebook Messenger Bot

Date : _______________  
Déployé par : _______________

---

## 📦 Phase 1 : Préparation Locale

- [ ] Tous les fichiers `core/messenger/` sont présents (10 fichiers)
- [ ] Migration `0049_messenger_models.py` existe dans `core/migrations/`
- [ ] Models `MessengerConversation` et `MessengerMessage` dans `core/models.py`
- [ ] Routes ajoutées dans `core/urls.py`
- [ ] `core.messenger` dans `INSTALLED_APPS` (settings.py)
- [ ] Variables Facebook dans settings.py (FACEBOOK_PAGE_ACCESS_TOKEN, etc.)
- [ ] Logging configuré dans settings.py
- [ ] `.env.example` mis à jour avec variables Facebook
- [ ] Tests locaux passent : `python test_messenger_integration.py`
- [ ] Code committé : `git commit -m "Add Facebook Messenger bot"`
- [ ] Code poussé : `git push origin main`

**Notes :**
```




```

---

## 🚀 Phase 2 : Déploiement Serveur

### Mise à Jour du Code

- [ ] Connexion au serveur : `C:\inetpub\wwwroot\test_py`
- [ ] Environnement virtuel activé : `.\venv\Scripts\activate`
- [ ] Code mis à jour : `git pull`
- [ ] Vérifier que tous les fichiers sont présents :
  - [ ] `core\messenger\` directory exists
  - [ ] `core\migrations\0049_messenger_models.py` exists

**Commandes exécutées :**
```powershell
cd C:\inetpub\wwwroot\test_py
.\venv\Scripts\activate
git pull
dir core\messenger
dir core\migrations\0049_messenger_models.py
```

### Configuration Base de Données

- [ ] Migration exécutée : `python manage.py migrate`
- [ ] Aucune erreur de migration
- [ ] Tables créées vérifiées :
  ```sql
  SHOW TABLES LIKE 'core_messenger%';
  ```
- [ ] Table `core_messengerconversation` existe
- [ ] Table `core_messengermessage` existe

**Output de la migration :**
```




```

### Variables d'Environnement

- [ ] Fichier `.env` sur le serveur édité
- [ ] `FACEBOOK_PAGE_ACCESS_TOKEN` ajouté
- [ ] `FACEBOOK_VERIFY_TOKEN` ajouté
- [ ] `FACEBOOK_PAGE_ID` ajouté
- [ ] `GROQ_API_KEY` vérifié (déjà présent normalement)
- [ ] `GROQ_MODEL` vérifié (déjà présent normalement)

**Token de vérification choisi :**
```
FACEBOOK_VERIFY_TOKEN=___________________________
```

### Redémarrage

- [ ] IIS redémarré : `iisreset`
- [ ] OU Pool d'application redémarré via IIS Manager
- [ ] Site accessible : `https://test-back.unityfianar.site/`

---

## 🧪 Phase 3 : Tests Serveur

### Test d'Intégration

- [ ] Script de test exécuté : `python test_messenger_integration.py`
- [ ] Test 1 : Variables d'environnement ✅
- [ ] Test 2 : Modèles de BDD ✅
- [ ] Test 3 : API Facebook ✅
- [ ] Test 4 : Service Groq ✅
- [ ] Test 5 : Apps installées ✅
- [ ] Test 6 : Logging ✅
- [ ] **Score : ___ / 6 tests réussis**

**Notes d'erreurs :**
```




```

### Test Webhook GET

- [ ] Commande curl exécutée :
  ```powershell
  curl "https://test-back.unityfianar.site/api/facebook/webhook/?hub.mode=subscribe&hub.verify_token=THE_BEAST_VERIFY&hub.challenge=HELLO"
  ```
- [ ] Réponse reçue : `HELLO`
- [ ] Status code : 200

**Output :**
```




```

### Vérification Logs

- [ ] Fichier `messenger_debug.log` créé
- [ ] Logs de vérification GET visibles
- [ ] Pas d'erreur dans les logs

**Dernières lignes du log :**
```powershell
Get-Content messenger_debug.log -Tail 20
```

---

## 🔗 Phase 4 : Configuration Facebook

### Obtention des Tokens

#### Page Access Token
- [ ] Connecté à https://developers.facebook.com/apps
- [ ] App sélectionnée : _______________________
- [ ] Navigué vers "Messenger" > "Settings"
- [ ] Page sélectionnée : _______________________
- [ ] Token généré et copié

**Page ID :** _______________________

#### Verify Token
- [ ] Token de vérification choisi : _______________________
- [ ] Ajouté dans `.env` sur le serveur
- [ ] Correspond à celui dans le curl de test

### Configuration Webhook

- [ ] Navigé vers "Messenger" > "Settings" > "Webhooks"
- [ ] Cliqué "Add Callback URL"
- [ ] URL entrée : `https://test-back.unityfianar.site/api/facebook/webhook/`
- [ ] Verify Token entré : _______________________
- [ ] "Verify and Save" cliqué
- [ ] ✅ Vérification réussie (message de succès de Facebook)

**Événements abonnés :**
- [ ] `messages`
- [ ] `messaging_postbacks`
- [ ] (Optionnel) `message_deliveries`
- [ ] (Optionnel) `message_reads`

### Abonnement de la Page

- [ ] Section "Webhooks" > "Add Subscriptions"
- [ ] Page Facebook sélectionnée
- [ ] Événements cochés et sauvegardés
- [ ] Status : **Subscribed** ✅

---

## 🎯 Phase 5 : Tests Réels

### Test avec Messenger

- [ ] Ouvert Facebook Messenger sur mobile/desktop
- [ ] Cherché la Page : _______________________
- [ ] Message envoyé : "Bonjour"

**Résultat attendu :**
- [ ] Message reçu par le webhook (visible dans les logs)
- [ ] Appel à Groq effectué
- [ ] Réponse envoyée au user
- [ ] Réponse reçue dans Messenger

**Message de réponse reçu :**
```




```

### Vérification Logs Production

- [ ] Logs consultés : `type messenger_debug.log`
- [ ] Entrée POST visible : `📨 WEBHOOK POST REQUEST`
- [ ] Event processing visible
- [ ] Appel Groq visible : `🤖 Calling Groq AI`
- [ ] Envoi réponse visible : `📤 Sending response`
- [ ] Success confirmé : `✅ Event processed successfully`

**Extrait des logs :**
```




```

### Vérification Base de Données

```sql
-- Conversations créées
SELECT COUNT(*) FROM core_messengerconversation;
-- Résultat : ___________

-- Messages enregistrés
SELECT COUNT(*) FROM core_messengermessage;
-- Résultat : ___________

-- Dernier message
SELECT * FROM core_messengermessage ORDER BY created_at DESC LIMIT 1;
```

- [ ] Au moins 1 conversation créée
- [ ] Au moins 2 messages (1 user + 1 assistant)
- [ ] `facebook_user_id` correctement enregistré

---

## 🎉 Phase 6 : Validation Finale

### Checklist Fonctionnelle

- [ ] ✅ Le bot répond aux messages Messenger
- [ ] ✅ Les conversations sont enregistrées en BDD
- [ ] ✅ L'historique est conservé entre messages
- [ ] ✅ Les logs sont détaillés et lisibles
- [ ] ✅ Pas de messages d'erreur dans les logs
- [ ] ✅ Temps de réponse acceptable (< 5 secondes)
- [ ] ✅ Le contexte Nilsen Un-it est utilisé par l'IA
- [ ] ✅ Admin Django montre les conversations

### Test Admin Django

- [ ] Connecté à : `https://test-back.unityfianar.site/admin/`
- [ ] Section "Messenger Conversations" visible
- [ ] Section "Messenger Messages" visible
- [ ] Conversations de test affichées
- [ ] Messages de test affichés

### Test de Stress (Optionnel)

- [ ] Envoyé 5 messages consécutifs rapidement
- [ ] Tous les messages ont reçu une réponse
- [ ] Pas de duplication de message (`message_id` fonctionne)
- [ ] Pas d'erreur dans les logs

---

## 📚 Phase 7 : Documentation

### Documentation Complétée

- [ ] `MESSENGER_DEPLOYMENT_GUIDE.md` lu et compris
- [ ] `MESSENGER_QUICK_REFERENCE.md` accessible
- [ ] `core/messenger/README.md` lu
- [ ] Logs de déploiement archivés

### Équipe Informée

- [ ] Déploiement annoncé à l'équipe
- [ ] Instructions d'utilisation partagées
- [ ] Contact support défini pour bugs/questions

**Contact support :** _______________________

---

## 🐛 Problèmes Rencontrés

### Problème 1
**Description :**
```




```

**Solution :**
```




```

### Problème 2
**Description :**
```




```

**Solution :**
```




```

---

## 📝 Notes Additionnelles

```










```

---

## ✅ Validation

**Déploiement terminé avec succès :**
- [ ] OUI - Toutes les phases complétées
- [ ] NON - Voir section "Problèmes Rencontrés"

**Date de mise en production :** _______________  
**Durée totale du déploiement :** _______________ minutes  
**Signature :** _______________

---

**Prochaines étapes recommandées :**
- [ ] Monitoring des logs pendant 48h
- [ ] Feedback des premiers utilisateurs
- [ ] Ajout de fonctionnalités avancées (boutons, images, etc.)
- [ ] Documentation utilisateur final

**Date de revue post-déploiement :** _______________
