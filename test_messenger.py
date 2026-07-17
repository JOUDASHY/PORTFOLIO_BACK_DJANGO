"""
Script de test pour l'intégration Facebook Messenger
Usage: python test_messenger.py
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back_django_portfolio_me.settings')
django.setup()

from core.messenger.ai_service import GroqAIService
from core.messenger.services import FacebookGraphAPI


def test_groq_api():
    """Test de l'API Groq"""
    print("\n=== Test Groq AI ===")
    try:
        service = GroqAIService()
        print("✅ Groq API Key configurée")
        
        # Test simple
        messages = [
            {"role": "user", "content": "Bonjour, qui es-tu ?"}
        ]
        response = service.chat(messages)
        print(f"✅ Réponse Groq : {response[:100]}...")
        return True
    except Exception as e:
        print(f"❌ Erreur Groq : {str(e)}")
        return False


def test_facebook_config():
    """Test de la configuration Facebook"""
    print("\n=== Test Configuration Facebook ===")
    try:
        api = FacebookGraphAPI()
        print("✅ Facebook Page Access Token configuré")
        
        verify_token = os.environ.get("FACEBOOK_VERIFY_TOKEN")
        page_id = os.environ.get("FACEBOOK_PAGE_ID")
        
        if verify_token:
            print(f"✅ Verify Token : {verify_token[:10]}...")
        else:
            print("⚠️  Verify Token non configuré")
        
        if page_id:
            print(f"✅ Page ID : {page_id}")
        else:
            print("⚠️  Page ID non configuré")
        
        return True
    except Exception as e:
        print(f"❌ Erreur Facebook : {str(e)}")
        return False


def test_database():
    """Test des modèles en base de données"""
    print("\n=== Test Base de Données ===")
    try:
        from core.messenger.models import MessengerConversation, MessengerMessage
        
        # Vérifier que les tables existent
        count_conv = MessengerConversation.objects.count()
        count_msg = MessengerMessage.objects.count()
        
        print(f"✅ Table MessengerConversation : {count_conv} conversations")
        print(f"✅ Table MessengerMessage : {count_msg} messages")
        return True
    except Exception as e:
        print(f"❌ Erreur BDD : {str(e)}")
        print("💡 Exécutez : python manage.py migrate")
        return False


def test_webhook_url():
    """Afficher l'URL du webhook"""
    print("\n=== URL du Webhook ===")
    base_url = os.environ.get("BASE_URL", "https://your-domain.com")
    webhook_url = f"{base_url}/api/facebook/webhook/"
    print(f"📍 URL à configurer dans Facebook :")
    print(f"   {webhook_url}")
    print(f"\n💡 Verify Token à utiliser : {os.environ.get('FACEBOOK_VERIFY_TOKEN', 'NON_CONFIGURÉ')}")


def main():
    """Exécute tous les tests"""
    print("=" * 60)
    print("🧪 Test de l'intégration Facebook Messenger")
    print("=" * 60)
    
    results = []
    
    # Tests
    results.append(("Groq AI", test_groq_api()))
    results.append(("Facebook Config", test_facebook_config()))
    results.append(("Base de Données", test_database()))
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ")
    print("=" * 60)
    
    for name, success in results:
        status = "✅ OK" if success else "❌ ÉCHEC"
        print(f"{status} : {name}")
    
    test_webhook_url()
    
    print("\n" + "=" * 60)
    
    all_success = all(success for _, success in results)
    if all_success:
        print("✅ Tous les tests sont passés !")
        print("\n📝 Prochaines étapes :")
        print("1. Configurez le webhook dans Facebook Developers")
        print("2. Testez en envoyant un message à votre Page Facebook")
        print("3. Vérifiez les logs Django et l'admin pour voir les conversations")
    else:
        print("⚠️  Certains tests ont échoué. Vérifiez votre configuration.")
        print("\n💡 Vérifiez :")
        print("1. Que toutes les variables d'environnement sont dans .env")
        print("2. Que vous avez exécuté : python manage.py migrate")
        print("3. Que les clés API sont valides")
    
    print("=" * 60)


if __name__ == "__main__":
    main()
