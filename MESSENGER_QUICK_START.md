# 🚀 Guide Rapide - Facebook Messenger Bot

## Configuration en 5 minutes

### 1. Variables d'environnement

Ajoutez dans `.env` :

```env
# Groq AI (déjà configuré normalement)
GROQ_API_KEY=gsk_votre_cle_groq

# Facebook Messenger (à ajouter)
FACEBOOK_PAGE_ACCESS_TOKEN=EAABxxxxxxxxxxxxxxxx
FACEBOOK_VERIFY_TOKEN=MON_TOKEN_SECURISE_123
FACEBOOK_PAGE_ID=123456789012345
```

### 2. Migrations

```bash
python manage.py migrate
```

### 3. Configuration Facebook

#### A. Créer l'app Facebook
1. [developers.facebook.com](https://developers.facebook.com) → **Créer une app**
2. Type : **Entreprise**
3. Ajoutez le produit **Messenger**

#### B. Obtenir le Page Access Token
1. Messenger → **Settings** → **Access Tokens**
2. Sélectionnez votre Page
3. **Generate Token** → Copiez dans `.env`

#### C. Configurer le Webhook
1. Messenger → **Settings** → **Webhooks**
2. **Add Callback URL** :
   - URL : `https://votre-domaine.com/api/facebook/webhook/`
   - Verify Token : Même valeur que dans `.env`
3. **Subscribe** aux événements :
   - ✅ messages
   - ✅ messaging_postbacks

### 4. Test

```bash
# Tester la configuration
python test_messenger.py

# Démarrer le serveur
python manage.py runserver
```

Envoyez un message à votre Page Facebook → Le bot devrait répondre ! 🎉

---

## Commandes utiles

```bash
# Voir les conversations dans l'admin
python manage.py createsuperuser  # Si pas encore fait
# Puis allez sur http://localhost:8000/admin/

# Tester Groq seul
python -c "from core.messenger.ai_service import GroqAIService; s = GroqAIService(); print(s.chat([{'role':'user','content':'Hello'}]))"

# Vérifier les modèles
python manage.py showmigrations core
```

---

## Personnalisation rapide

### Changer le comportement du bot

Éditez `core/messenger/ai_service.py` :

```python
def get_system_prompt(self) -> str:
    return """Tu es l'assistant de Nilsen, développeur Full Stack.
    
    Tu peux parler de :
    - Ses compétences (Django, React, etc.)
    - Ses projets
    - Comment le contacter
    
    Sois professionnel et concis."""
```

### Ajouter le contexte du portfolio

```python
def get_system_prompt(self) -> str:
    from core.models import Profile, Projet
    
    profile = Profile.objects.first()
    projets = Projet.objects.filter(is_featured=True)[:3]
    
    context = f"""Tu es l'assistant de {profile.user.get_full_name()}.
    
    À propos : {profile.about}
    
    Projets vedettes :
    {chr(10).join([f"- {p.nom}: {p.description}" for p in projets])}
    
    Réponds aux questions sur ces projets."""
    
    return context
```

---

## Dépannage

### ❌ "GROQ_API_KEY not set"
→ Vérifiez `.env` et redémarrez le serveur

### ❌ "Webhook verification failed"
→ Vérifiez que `FACEBOOK_VERIFY_TOKEN` correspond exactement

### ❌ Le bot ne répond pas
→ Vérifiez les logs Django : `python manage.py runserver`

### ❌ Messages dupliqués
→ C'est normal, la déduplication est déjà en place

---

## Pour aller plus loin

Consultez `MESSENGER_INTEGRATION.md` pour :
- Configuration avancée
- Sécurité renforcée
- Ajout de quick replies
- Webhook signature verification
- Support des images/fichiers
