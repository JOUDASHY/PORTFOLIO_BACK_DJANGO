# 🚀 Facebook Messenger Bot - Référence Rapide

## Déploiement Express (5 minutes)

### 1. Pousser le Code
```bash
git add .
git commit -m "Add Facebook Messenger bot"
git push
```

### 2. Sur le Serveur
```powershell
cd C:\inetpub\wwwroot\test_py
git pull
.\venv\Scripts\activate
python manage.py migrate
iisreset
```

### 3. Variables .env
Ajouter dans `C:\inetpub\wwwroot\test_py\.env` :
```env
FACEBOOK_PAGE_ACCESS_TOKEN=EAABxxxxx...
FACEBOOK_VERIFY_TOKEN=THE_BEAST_VERIFY
FACEBOOK_PAGE_ID=123456789
GROQ_API_KEY=gsk_xxxxx...
```

### 4. Test
```powershell
python test_messenger_integration.py
```

### 5. Configurer Facebook
1. https://developers.facebook.com/apps
2. Messenger > Settings > Webhooks
3. URL: `https://test-back.unityfianar.site/api/facebook/webhook/`
4. Verify Token: `THE_BEAST_VERIFY`
5. Subscribe: `messages`, `messaging_postbacks`

---

## 🔧 Commandes Utiles

### Logs
```powershell
# Voir les logs
type messenger_debug.log

# Suivre en temps réel
Get-Content messenger_debug.log -Wait -Tail 20

# Chercher des erreurs
type messenger_debug.log | findstr "ERROR"
```

### Base de Données
```sql
-- Voir les conversations
SELECT * FROM core_messengerconversation ORDER BY updated_at DESC LIMIT 10;

-- Voir les messages
SELECT * FROM core_messengermessage ORDER BY created_at DESC LIMIT 20;

-- Stats du jour
SELECT COUNT(*) FROM core_messengermessage WHERE DATE(created_at) = CURDATE();
```

### Tests
```powershell
# Test complet
python test_messenger_integration.py

# Test webhook GET
curl "https://test-back.unityfianar.site/api/facebook/webhook/?hub.mode=subscribe&hub.verify_token=THE_BEAST_VERIFY&hub.challenge=TEST"
```

---

## 📊 Endpoints

| Méthode | URL | Description |
|---------|-----|-------------|
| GET | `/api/facebook/webhook/` | Vérification Facebook |
| POST | `/api/facebook/webhook/` | Réception événements |

---

## 🐛 Dépannage Rapide

### Pas de réponse du bot ?
1. ✅ `python test_messenger_integration.py` → tous les tests passent ?
2. ✅ `type messenger_debug.log` → des POST arrivent ?
3. ✅ `.env` → tokens configurés ?
4. ✅ `python manage.py migrate` → migration OK ?

### Webhook non vérifié ?
- Vérifier `FACEBOOK_VERIFY_TOKEN` dans `.env`
- Tester : `curl "URL?hub.mode=subscribe&hub.verify_token=TOKEN&hub.challenge=TEST"`
- Devrait retourner `TEST`

### Erreur 404 sur webhook ?
- Vérifier que `core/messenger/` existe sur le serveur
- Vérifier `core/urls.py` : `path("facebook/", include("core.messenger.urls"))`
- `iisreset` après changements

---

## 📁 Fichiers Importants

| Fichier | Description |
|---------|-------------|
| `core/messenger/views.py` | Webhook GET/POST |
| `core/messenger/messenger.py` | Traitement événements |
| `core/messenger/ai_service.py` | Intégration Groq |
| `core/messenger/services.py` | Facebook Graph API |
| `core/models.py` | Models (fin du fichier) |
| `messenger_debug.log` | Logs détaillés |

---

## 🎯 Prochaines Étapes (Optionnel)

### Améliorations Possibles
- [ ] Ajouter support des images/pièces jointes
- [ ] Ajouter boutons interactifs
- [ ] Intégrer le RAG pour contexte portfolio
- [ ] Notifications proactives
- [ ] Analytics/Dashboard
- [ ] Multi-langue (FR/EN)

### Configuration Avancée
- [ ] Utiliser Redis pour le cache (au lieu de fichiers)
- [ ] Configurer signature verification (X-Hub-Signature-256)
- [ ] Rate limiting pour l'API Groq
- [ ] Backup automatique des conversations

---

**Contacts Support :**
- Documentation complète : `MESSENGER_DEPLOYMENT_GUIDE.md`
- Architecture : `core/messenger/README.md`
- Facebook Docs : https://developers.facebook.com/docs/messenger-platform

**Dernière mise à jour :** 2026-07-17
