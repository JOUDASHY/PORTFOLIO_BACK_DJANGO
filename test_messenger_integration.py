"""
Script de Test pour l'Intégration Facebook Messenger
Exécuter après le déploiement pour vérifier que tout fonctionne
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back_django_portfolio_me.settings')
django.setup()

from django.conf import settings
from core.models import MessengerConversation, MessengerMessage
from core.messenger.services import FacebookGraphAPI
from core.messenger.ai_service import GroqAIService

def print_section(title):
    """Affiche un titre de section"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)

def test_environment_variables():
    """Test 1: Vérifier les variables d'environnement"""
    print_section("TEST 1: Variables d'Environnement")
    
    required_vars = {
        'FACEBOOK_PAGE_ACCESS_TOKEN': settings.FACEBOOK_PAGE_ACCESS_TOKEN,
        'FACEBOOK_VERIFY_TOKEN': settings.FACEBOOK_VERIFY_TOKEN,
        'FACEBOOK_PAGE_ID': settings.FACEBOOK_PAGE_ID,
        'GROQ_API_KEY': settings.GROQ_API_KEY,
    }
    
    all_ok = True
    for var_name, var_value in required_vars.items():
        if var_value:
            # Masquer les valeurs sensibles
            display_value = f"{var_value[:10]}..." if len(var_value) > 10 else "***"
            print(f"  ✅ {var_name}: {display_value}")
        else:
            print(f"  ❌ {var_name}: NOT SET")
            all_ok = False
    
    return all_ok

def test_database_models():
    """Test 2: Vérifier que les modèles de base de données fonctionnent"""
    print_section("TEST 2: Modèles de Base de Données")
    
    try:
        # Test création d'une conversation
        print("  📝 Création d'une conversation de test...")
        conversation = MessengerConversation.objects.create(
            facebook_user_id="test_user_12345",
            page_id="test_page_67890"
        )
        print(f"  ✅ Conversation créée: ID={conversation.id}")
        
        # Test création d'un message
        print("  📝 Création d'un message de test...")
        message = MessengerMessage.objects.create(
            conversation=conversation,
            message_id="test_mid_001",
            role="user",
            content="Message de test"
        )
        print(f"  ✅ Message créé: ID={message.id}")
        
        # Test récupération
        print("  📝 Récupération des messages...")
        messages = conversation.messages.all()
        print(f"  ✅ Messages récupérés: {messages.count()}")
        
        # Nettoyage
        print("  🧹 Nettoyage...")
        conversation.delete()
        print("  ✅ Conversation supprimée")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_facebook_api():
    """Test 3: Tester l'API Facebook (sans envoyer de message réel)"""
    print_section("TEST 3: Service Facebook Graph API")
    
    try:
        print("  📝 Initialisation du service Facebook...")
        fb_service = FacebookGraphAPI()
        print("  ✅ Service initialisé")
        
        # Note: On ne teste pas l'envoi réel pour éviter de spammer
        print("  ℹ️  Service prêt (pas d'envoi de message test)")
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur: {e}")
        return False

def test_groq_service():
    """Test 4: Tester le service Groq AI"""
    print_section("TEST 4: Service Groq AI")
    
    try:
        print("  📝 Initialisation du service Groq...")
        groq_service = GroqAIService()
        print("  ✅ Service initialisé")
        
        # Test d'un appel simple
        print("  📝 Test d'une requête simple...")
        test_messages = [
            {"role": "user", "content": "Bonjour, qui es-tu ?"}
        ]
        
        response = groq_service.get_response(test_messages)
        
        if response:
            print(f"  ✅ Réponse reçue ({len(response)} caractères)")
            print(f"  💬 Aperçu: {response[:100]}...")
            return True
        else:
            print("  ❌ Pas de réponse de Groq")
            return False
        
    except Exception as e:
        print(f"  ❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_installed_apps():
    """Test 5: Vérifier que l'app est installée"""
    print_section("TEST 5: Configuration Django")
    
    if 'core.messenger' in settings.INSTALLED_APPS:
        print("  ✅ 'core.messenger' dans INSTALLED_APPS")
        return True
    else:
        print("  ❌ 'core.messenger' n'est pas dans INSTALLED_APPS")
        return False

def test_logging_config():
    """Test 6: Vérifier la configuration du logging"""
    print_section("TEST 6: Configuration du Logging")
    
    try:
        import logging
        logger = logging.getLogger('core.messenger')
        
        # Test d'un log
        logger.info("Test log from integration test script")
        print("  ✅ Logger configuré et fonctionnel")
        
        # Vérifier le fichier de log
        log_file = os.path.join(settings.BASE_DIR, 'messenger_debug.log')
        if os.path.exists(log_file):
            size = os.path.getsize(log_file)
            print(f"  ✅ Fichier de log existe: messenger_debug.log ({size} bytes)")
        else:
            print("  ⚠️  Fichier de log n'existe pas encore (normal si aucun événement)")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur: {e}")
        return False

def run_all_tests():
    """Exécute tous les tests"""
    print("\n" + "🚀" * 40)
    print("  TEST D'INTÉGRATION FACEBOOK MESSENGER BOT")
    print("🚀" * 40)
    
    results = {
        "Variables d'environnement": test_environment_variables(),
        "Modèles de base de données": test_database_models(),
        "API Facebook": test_facebook_api(),
        "Service Groq AI": test_groq_service(),
        "Apps installées": test_installed_apps(),
        "Configuration logging": test_logging_config(),
    }
    
    # Résumé
    print_section("RÉSUMÉ DES TESTS")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}  {test_name}")
    
    print(f"\n  Score: {passed}/{total} tests réussis")
    
    if passed == total:
        print("\n  🎉 TOUS LES TESTS SONT PASSÉS !")
        print("  Le bot Messenger est prêt à être utilisé.")
        return 0
    else:
        print("\n  ⚠️  CERTAINS TESTS ONT ÉCHOUÉ")
        print("  Vérifiez les erreurs ci-dessus avant de continuer.")
        return 1

if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
