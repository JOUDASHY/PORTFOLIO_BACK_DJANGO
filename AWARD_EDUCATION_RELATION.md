# 🎓 Relation Award ↔ Education : Diplômes et Certifications

## 📋 Vue d'ensemble

Le modèle `Award` a été modifié pour représenter les **diplômes et certifications** obtenus lors d'un parcours éducatif (`Education`).

## 🔗 Relation

```
Education (1) ────────< (N) Award (Diplômes/Certifications)
```

- **Type de relation** : One-to-Many (Education → Awards)
- **Cascade** : `on_delete=CASCADE` (supprimer Education → supprime ses diplômes)
- **Optionnelle** : `null=True, blank=True` (permet des certifications indépendantes)
- **Related name** : `education.diplomes.all()`

## 📊 Structure des modèles

### **Education (Parcours éducatif)**
```python
class Education(models.Model):
    image = ImageField()
    nom_ecole = CharField(max_length=255)        # Ex: "Université Paris-Saclay"
    nom_parcours = CharField(max_length=255)     # Ex: "Master Informatique"
    annee_debut = IntegerField()                 # Ex: 2020
    annee_fin = IntegerField()                   # Ex: 2022
    lieu = CharField(max_length=255)             # Ex: "Paris, France"
```

### **Award (Diplômes/Certifications)**
```python
class Award(models.Model):
    # NOUVEAU : Relation vers Education
    education = ForeignKey(
        Education,
        on_delete=CASCADE,
        related_name='diplomes',
        null=True,
        blank=True
    )
    
    titre = CharField(max_length=255)            # Ex: "Master 2 en Informatique"
    institution = CharField(max_length=255)      # Ex: "Ministère de l'Éducation"
    
    # NOUVEAU : Choices pour le type
    type = CharField(
        max_length=50,
        choices=[
            ('diplome', 'Diplôme'),
            ('certification', 'Certification'),
            ('attestation', 'Attestation'),
            ('brevet', 'Brevet'),
            ('autre', 'Autre'),
        ],
        default='diplome'
    )
    
    annee = IntegerField()                       # Ex: 2022
```

## 🎯 Cas d'usage

### **Exemple 1 : Diplômes académiques**
```json
{
  "education": {
    "nom_ecole": "ITU Madagascar",
    "nom_parcours": "Ingénieur en Génie Logiciel",
    "annee_debut": 2018,
    "annee_fin": 2023,
    "diplomes": [
      {
        "titre": "Diplôme d'Ingénieur",
        "type": "diplome",
        "institution": "Ministère de l'Éducation",
        "annee": 2023
      },
      {
        "titre": "Licence en Informatique",
        "type": "diplome",
        "institution": "ITU",
        "annee": 2021
      }
    ]
  }
}
```

### **Exemple 2 : Certifications professionnelles**
```json
{
  "education": {
    "nom_ecole": "Udemy",
    "nom_parcours": "Full Stack Developer Bootcamp",
    "annee_debut": 2022,
    "annee_fin": 2022,
    "diplomes": [
      {
        "titre": "Certificat Django & React",
        "type": "certification",
        "institution": "Udemy",
        "annee": 2022
      },
      {
        "titre": "Certificat Docker & Kubernetes",
        "type": "certification",
        "institution": "Udemy",
        "annee": 2022
      }
    ]
  }
}
```

### **Exemple 3 : Certifications indépendantes**
```json
{
  "award": {
    "education": null,
    "titre": "AWS Solutions Architect - Associate",
    "type": "certification",
    "institution": "Amazon Web Services",
    "annee": 2023
  }
}
```

## 🔧 API Endpoints

### **GET /api/educations/**
Retourne les parcours éducatifs avec leurs diplômes :
```json
[
  {
    "id": 1,
    "nom_ecole": "ITU Madagascar",
    "nom_parcours": "Ingénieur en Génie Logiciel",
    "annee_debut": 2018,
    "annee_fin": 2023,
    "lieu": "Antananarivo",
    "diplomes": [
      {
        "id": 1,
        "titre": "Diplôme d'Ingénieur",
        "type": "diplome",
        "type_display": "Diplôme",
        "institution": "Ministère",
        "annee": 2023
      }
    ]
  }
]
```

### **GET /api/awards/**
Retourne tous les diplômes/certifications :
```json
[
  {
    "id": 1,
    "education": 1,
    "education_name": "ITU Madagascar - Ingénieur en Génie Logiciel",
    "titre": "Diplôme d'Ingénieur",
    "type": "diplome",
    "type_display": "Diplôme",
    "institution": "Ministère",
    "annee": 2023
  },
  {
    "id": 2,
    "education": null,
    "education_name": null,
    "titre": "AWS Certified",
    "type": "certification",
    "type_display": "Certification",
    "institution": "Amazon",
    "annee": 2024
  }
]
```

## 📝 Modifications effectuées

### **1. Modèles (models.py)**
- ✅ Ajout de `education` ForeignKey dans `Award`
- ✅ Ajout de `TYPE_CHOICES` pour le champ `type`
- ✅ Ajout de `help_text` sur tous les champs
- ✅ Mise à jour `Meta` (verbose_name, ordering)
- ✅ Amélioration `__str__()` method

### **2. Serializers (serializers.py)**
- ✅ `AwardSerializer` : ajout de `education`, `education_name`, `type_display`
- ✅ `EducationSerializer` : ajout de `diplomes` (nested serializer)

### **3. Admin (admin.py)**
- ✅ Enregistrement de `Award` avec admin personnalisé
- ✅ Filtres par type et année
- ✅ Recherche par titre, institution, école
- ✅ Autocomplete sur le champ `education`

### **4. Migration (0051_add_education_to_award.py)**
- ✅ Ajout du champ `education` (nullable)
- ✅ Mise à jour du champ `type` avec choices
- ✅ Ajout des help_text
- ✅ Mise à jour des Meta options

## 🚀 Déploiement

### **1. Appliquer la migration**
```bash
python manage.py migrate core 0051
```

### **2. Vérifier les données existantes**
```bash
python manage.py shell
>>> from core.models import Award, Education
>>> Award.objects.filter(education__isnull=True).count()
```

### **3. Lier les awards existants (optionnel)**
Si vous avez des awards existants à lier à des educations :
```python
# Dans le shell Django
from core.models import Award, Education

# Exemple : lier tous les awards de "ITU" à l'education ITU
itu_education = Education.objects.get(nom_ecole="ITU")
Award.objects.filter(institution__icontains="ITU").update(education=itu_education)
```

## ✅ Tests

### **Test 1 : Créer une education avec diplômes**
```python
from core.models import Education, Award

# Créer une education
education = Education.objects.create(
    nom_ecole="ITU Madagascar",
    nom_parcours="Ingénieur Génie Logiciel",
    annee_debut=2018,
    annee_fin=2023,
    lieu="Antananarivo"
)

# Créer des diplômes liés
Award.objects.create(
    education=education,
    titre="Diplôme d'Ingénieur",
    type="diplome",
    institution="Ministère de l'Éducation",
    annee=2023
)

# Récupérer les diplômes d'une education
diplomes = education.diplomes.all()
print(f"Diplômes: {diplomes.count()}")
```

### **Test 2 : Award indépendant**
```python
# Créer une certification sans education
Award.objects.create(
    education=None,  # Pas de relation
    titre="AWS Solutions Architect",
    type="certification",
    institution="Amazon",
    annee=2024
)
```

## 📱 Utilisation dans le frontend

```javascript
// Récupérer une education avec ses diplômes
const response = await fetch('/api/educations/1/');
const education = await response.json();

console.log(education.nom_ecole);  // "ITU Madagascar"
console.log(education.diplomes);   // Array de diplômes

// Afficher les diplômes
education.diplomes.forEach(diplome => {
  console.log(`${diplome.titre} (${diplome.type_display}) - ${diplome.annee}`);
});
```

## 🎨 Affichage recommandé pour le CV/Portfolio

```
🎓 FORMATION

ITU Madagascar (2018-2023)
Ingénieur en Génie Logiciel
📍 Antananarivo, Madagascar

  📜 Diplômes obtenus:
  ✓ Diplôme d'Ingénieur (2023) - Ministère de l'Éducation
  ✓ Licence en Informatique (2021) - ITU
  ✓ Certification Scrum Master (2022) - Scrum.org

───────────────────────────────────────

🎓 CERTIFICATIONS INDÉPENDANTES

  📜 Certifications obtenues:
  ✓ AWS Solutions Architect - Associate (2024) - Amazon Web Services
  ✓ Google Cloud Professional (2024) - Google
```

## 🐛 Dépannage

### **Problème : Migration ne s'applique pas**
```bash
python manage.py showmigrations core
# Vérifier que 0051 n'est pas déjà appliquée

python manage.py migrate core 0051 --fake
# Si la base est déjà à jour mais Django ne le sait pas
```

### **Problème : awards existants sans education**
C'est normal ! La relation est optionnelle. Les awards existants restent valides avec `education=null`.

## 📚 Ressources

- Documentation Django ForeignKey: https://docs.djangoproject.com/en/4.2/ref/models/fields/#foreignkey
- Documentation Django Choices: https://docs.djangoproject.com/en/4.2/ref/models/fields/#choices
- REST Framework Nested Serializers: https://www.django-rest-framework.org/api-guide/relations/#nested-relationships
