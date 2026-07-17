# 🚀 FACEBOOK MESSENGER BOT - COMMENCEZ ICI

## 👋 Bienvenue !

Votre bot Facebook Messenger avec Groq AI a été **entièrement implémenté**.

---

## ⚡ Démarrage en 3 étapes

### 1️⃣ Configuration (5 min)

Créez un fichier `.env` à la racine avec :

```env
GROQ_API_KEY=gsk_votre_cle
FACEBOOK_PAGE_ACCESS_TOKEN=EAABxxx
FACEBOOK_VERIFY_TOKEN=MON_TOKEN
FACEBOOK_PAGE_ID=123456789
```

### 2️⃣ Installation (2 min)

```bash
python manage.py migrate
python test_messenger.py
```

### 3️⃣ Configuration Facebook (10 min)

1. Créez une app sur [developers.facebook.com](https://developers.facebook.com)
2. Obtenez votre **Page Access Token**
3. Configurez le webhook : `https://votre-domaine.com/api/facebook/webhook/`

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| **`MESSENGER_QUICK_START.md`** | ⚡ Guide rapide 5 min |
| **`RESUME_INTEGRATION_FR.md`** | 🇫🇷 Résumé complet en français |
| **`MESSENGER_INDEX.md`** | 📚 Index de toute la doc |
| **`MESSENGER_INTEGRATION.md`** | 📖 Guide technique complet |
| **`MESSENGER_COMMANDS.md`** | 🔧 Toutes les commandes |

---

## ✅ Checklist

- [ ] Variables d'environnement dans `.env`
- [ ] Migration : `python manage.py migrate`
- [ ] Test : `python test_messenger.py`
- [ ] App Facebook créée
- [ ] Webhook configuré
- [ ] Test en production (envoyer message à la Page)

---

## 🆘 Aide rapide

**Problème ?**
1. Exécutez : `python test_messenger.py`
2. Consultez : `RESUME_INTEGRATION_FR.md` (section "Résolution")
3. Regardez les logs Django

**Personnaliser ?**
1. Éditez : `core/messenger/ai_service.py`
2. Méthode : `get_system_prompt()`
3. Redémarrez le serveur

---

## 📂 Fichiers créés

```
core/messenger/          → Module complet (9 fichiers)
├── models.py           → Base de données
├── services.py         → Facebook API
├── ai_service.py       → Groq AI
├── messenger.py        → Logique métier
└── ...

Documentation/          → 10 fichiers MD
├── MESSENGER_QUICK_START.md
├── MESSENGER_INTEGRATION.md
├── RESUME_INTEGRATION_FR.md
└── ...

test_messenger.py       → Script de test
```

---

## 🎯 Prochaines étapes

1. ✅ **Lisez** : `MESSENGER_QUICK_START.md`
2. ✅ **Configurez** : Variables + Facebook
3. ✅ **Testez** : Envoyez un message à votre Page
4. ✅ **Personnalisez** : Modifiez le prompt IA

---

## 💡 Navigation rapide

- 🚀 **Débutant** → `MESSENGER_QUICK_START.md`
- 🇫🇷 **Français** → `RESUME_INTEGRATION_FR.md`
- 📚 **Tous les docs** → `MESSENGER_INDEX.md`
- 🔧 **Commandes** → `MESSENGER_COMMANDS.md`
- 📖 **Technique** → `MESSENGER_INTEGRATION.md`

---

## ✨ C'est parti !

Votre bot est prêt. Il suffit de configurer les tokens Facebook ! 🤖

**Commencez par** : `MESSENGER_QUICK_START.md`

---

**Bon courage ! 🚀**
