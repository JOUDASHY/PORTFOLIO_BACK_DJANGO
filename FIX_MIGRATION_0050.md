# 🔧 Fix Migration 0050 Error

## ❌ Erreur rencontrée :
```
django.db.utils.OperationalError: (1826, "Duplicate foreign key constraint name 'core_messengermessag_conversation_id_02666a88_fk_core_mess'")
```

## 🔍 Cause :
La migration `0050_messenger_models_manual` tente de créer des tables/contraintes qui existent déjà en base de données (probablement créées par la migration `0049_messenger_models`).

## ✅ Solution : Faker la migration 0050

### **Étape 1 : Vérifier l'état des migrations**
```powershell
python manage.py showmigrations core
```

Vous devriez voir quelque chose comme :
```
core
  [X] 0049_messenger_models
  [ ] 0050_messenger_models_manual  ← Non appliquée
  [ ] 0051_add_education_to_award   ← Notre nouvelle migration
```

### **Étape 2 : Faker la migration 0050**
Si les tables `MessengerConversation` et `MessengerMessage` existent déjà :

```powershell
python manage.py migrate core 0050 --fake
```

Cette commande marque la migration 0050 comme appliquée sans exécuter le SQL.

### **Étape 3 : Appliquer la migration 0051**
```powershell
python manage.py migrate core 0051
```

## 🔍 Alternative : Vérifier si les tables existent

Si vous voulez vérifier manuellement :

```powershell
python manage.py dbshell
```

Puis dans MySQL :
```sql
SHOW TABLES LIKE 'core_messenger%';
```

Si vous voyez `core_messengerconversation` et `core_messengermessage`, les tables existent déjà.

### **Sortir de dbshell :**
```sql
exit;
```

## 🚨 Si ça ne fonctionne toujours pas

### **Option A : Supprimer et recréer 0050**

1. **Faker toutes les migrations jusqu'à 0049 :**
```powershell
python manage.py migrate core 0049
```

2. **Supprimer le fichier 0050 :**
```powershell
Remove-Item "core\migrations\0050_messenger_models_manual.py"
```

3. **Appliquer 0051 directement :**
```powershell
python manage.py migrate core 0051
```

### **Option B : Éditer 0051 pour changer la dépendance**

Ouvrir `core/migrations/0051_add_education_to_award.py` et changer :

```python
dependencies = [
    ('core', '0049_messenger_models'),  # ← Changer de 0050 à 0049
]
```

Puis :
```powershell
python manage.py migrate core 0051
```

## ✅ Vérification finale

Après avoir appliqué la migration :

```powershell
python manage.py showmigrations core
```

Vous devriez voir :
```
core
  [X] 0049_messenger_models
  [X] 0050_messenger_models_manual
  [X] 0051_add_education_to_award  ← ✅ Appliquée !
```

## 🎯 Tester la relation Award-Education

```powershell
python manage.py shell
```

```python
from core.models import Education, Award

# Créer une éducation
edu = Education.objects.create(
    nom_ecole="Test School",
    nom_parcours="Test Program",
    annee_debut=2020,
    annee_fin=2024,
    lieu="Test City"
)

# Créer un diplôme lié
award = Award.objects.create(
    education=edu,
    titre="Test Diploma",
    type="diplome",
    institution="Test Institution",
    annee=2024
)

# Vérifier
print(f"Education: {edu}")
print(f"Diplomes: {edu.diplomes.all()}")
```

## 📝 Résumé des commandes

```powershell
# 1. Faker 0050
python manage.py migrate core 0050 --fake

# 2. Appliquer 0051
python manage.py migrate core 0051

# 3. Vérifier
python manage.py showmigrations core
```

✅ C'est tout ! La relation Award-Education devrait maintenant fonctionner.
