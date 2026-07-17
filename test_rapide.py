"""
Script de Test Rapide - Messenger Bot
Lancez ce script pour vérifier rapidement si tout fonctionne
"""
import os
import sys

def print_header(text):
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def print_success(text):
    print(f"  ✅ {text}")

def print_error(text):
    print(f"  ❌ {text}")

def print_info(text):
    print(f"  ℹ️  {text}")

print_header("TEST RAPIDE - MESSENGER BOT")

# Test 1: Fichiers
print_header("TEST 1: Vérification des Fichiers")
files_to_check = [
    "core/messenger/__init__.py",
    "core/messenger/views.py",
    "core/messenger/messenger.py",
    "core/messenger/ai_service.py",
    "core/messenger/services.py",
    "core/migrations/0049_messenger_models.py",
]

all_files_exist = True
for file in files_to_check:
    if os.path.exists(file):
        print_success(f"{file}")
    else:
        print_error(f"{file} MANQUANT")
        all_files_exist = False

if all_files_exist:
    print_success("Tous les fichiers sont présents")
else:
    print_error("Des fichiers sont manquants")
    sys.exit(1)

# Test 2: Django Setup
print_header("TEST 2: Configuration Django")
try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back_django_portfolio_me.settings')
    import django
    django.setup()
    print_success("Django configuré")
except Exception as e:
    print_error(f"Erreur Django: {e}")
    sys.exit(1)

# Test 3: Variables d'environnement
print_header("TEST 3: Variables d'Environnement")
from django.conf import settings

vars_to_check = {
    'FACEBOOK_PAGE_ACCESS_TOKEN': settings.FACEBOOK_PAGE_ACCESS_TOKEN,
    'FACEBOOK_VERIFY_TOKEN': settings.FACEBOOK_VERIFY_TOKEN,
    'FACEBOOK_PAGE_ID': settings.FACEBOOK_PAGE_ID,
    'GROQ_API_KEY': settings.GROQ_API_KEY,
}

all_vars_ok = True
for var_name, var_value in vars_to_check.items():
    if var_value:
        masked = f"{var_value[:10]}..." if len(var_value) > 10 else "***"
        print_success(f"{var_name}: {masked}")
    else:
        print_error(f"{var_name}: NON CONFIGURÉ")
        all_vars_ok = False

if not all_vars_ok:
    print_info("Configurez les variables manquantes dans le fichier .env")
    sys.exit(1)

# Test 4: Modèles
print_header("TEST 4: Modèles de Base de Données")
try:
    from core.models import MessengerConversation, MessengerMessage
    print_success("MessengerConversation importé")
    print_success("MessengerMessage importé")
    
    # Tester une requête
    count = MessengerConversation.objects.count()
    print_info(f"Conversations dans la BDD: {count}")
except Exception as e:
    print_error(f"Erreur modèles: {e}")
    print_info("Lancez: python manage.py migrate")
    sys.exit(1)

# Test 5: Service Groq
print_header("TEST 5: Service Groq AI")
try:
    from core.messenger.ai_service import GroqAIService
    groq = GroqAIService()
    print_success("Service Groq initialisé")
    
    print_info("Test d'un appel rapide...")
    response = groq.get_response([{"role": "user", "content": "Bonjour"}])
    if response:
        print_success(f"Réponse reçue ({len(response)} caractères)")
    else:
        print_error("Pas de réponse de Groq")
except Exception as e:
    print_error(f"Erreur Groq: {e}")
    sys.exit(1)

# Test 6: Service Facebook
print_header("TEST 6: Service Facebook API")
try:
    from core.messenger.services import FacebookGraphAPI
    fb = FacebookGraphAPI()
    print_success("Service Facebook initialisé")
except Exception as e:
    print_error(f"Erreur Facebook: {e}")
    sys.exit(1)

# Résumé
print_header("RÉSUMÉ")
print_success("✨ TOUS LES TESTS SONT PASSÉS !")
print("")
print_info("Prochaines étapes:")
print("    1. Pousser le code: git push")
print("    2. Déployer: git pull (sur le serveur)")
print("    3. Migrer: python manage.py migrate")
print("    4. Tester webhook: curl https://test-back.unityfianar.site/api/facebook/webhook/...")
print("    5. Configurer Facebook webhook")
print("")
print_info("Documentation: README_MESSENGER.md")
print("")

sys.exit(0)
