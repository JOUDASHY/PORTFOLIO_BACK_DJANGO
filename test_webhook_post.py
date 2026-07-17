"""
Script pour tester le webhook POST localement
Simule un événement Facebook Messenger
"""
import requests
import json
import sys

# URL de votre webhook
WEBHOOK_URL = "https://test-back.unityfianar.site/api/facebook/webhook/"
# WEBHOOK_URL = "http://localhost:8000/api/facebook/webhook/"  # Pour test local

# Événement simulé
event_data = {
    "object": "page",
    "entry": [
        {
            "id": "PAGE_ID",
            "time": 1234567890,
            "messaging": [
                {
                    "sender": {
                        "id": "1234567890"  # ID utilisateur test
                    },
                    "recipient": {
                        "id": "0987654321"  # ID de votre page
                    },
                    "timestamp": 1234567890,
                    "message": {
                        "mid": "test_mid_123456",
                        "text": "Bonjour, ceci est un test"
                    }
                }
            ]
        }
    ]
}

def test_webhook_post():
    """Test du webhook POST"""
    print("=" * 80)
    print("🧪 TEST WEBHOOK POST")
    print("=" * 80)
    print(f"URL: {WEBHOOK_URL}")
    print(f"\nDonnées envoyées:")
    print(json.dumps(event_data, indent=2))
    print("\n" + "=" * 80)
    
    try:
        print("📤 Envoi de la requête POST...")
        response = requests.post(
            WEBHOOK_URL,
            json=event_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"\n✅ Réponse reçue!")
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"\nCorps de la réponse:")
        print(response.text)
        
        if response.status_code == 200:
            print("\n✅ SUCCESS - Le webhook a répondu 200 OK")
            print("\n💡 Vérifiez maintenant:")
            print("  1. Les logs Django (console ou messenger_debug.log)")
            print("  2. La base de données (nouvelle conversation/message)")
            print("  3. Que le bot n'a PAS envoyé de message (normal en test)")
        else:
            print(f"\n⚠️ Status code inattendu: {response.status_code}")
            
    except requests.exceptions.Timeout:
        print("\n❌ TIMEOUT - Le serveur n'a pas répondu dans les 30 secondes")
        print("Vérifiez que le serveur Django est démarré")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ CONNECTION ERROR - Impossible de se connecter au serveur")
        print("Vérifiez:")
        print(f"  1. Que l'URL est correcte: {WEBHOOK_URL}")
        print("  2. Que le serveur Django est démarré")
        print("  3. Que vous avez accès au serveur (firewall, VPN, etc.)")
        
    except Exception as e:
        print(f"\n❌ ERREUR: {type(e).__name__}")
        print(f"Message: {str(e)}")
    
    print("\n" + "=" * 80)


def test_webhook_get():
    """Test du webhook GET (vérification)"""
    print("=" * 80)
    print("🧪 TEST WEBHOOK GET (Vérification)")
    print("=" * 80)
    
    # Vous devez mettre votre vrai FACEBOOK_VERIFY_TOKEN ici
    verify_token = "THE_BEAST_VERIFY"  # Remplacez par votre token
    
    params = {
        "hub.mode": "subscribe",
        "hub.verify_token": verify_token,
        "hub.challenge": "test_challenge_123"
    }
    
    print(f"URL: {WEBHOOK_URL}")
    print(f"Paramètres: {params}")
    print("\n" + "=" * 80)
    
    try:
        print("📤 Envoi de la requête GET...")
        response = requests.get(WEBHOOK_URL, params=params, timeout=10)
        
        print(f"\n✅ Réponse reçue!")
        print(f"Status Code: {response.status_code}")
        print(f"Réponse: {response.text}")
        
        if response.status_code == 200 and response.text == "test_challenge_123":
            print("\n✅ SUCCESS - Le webhook GET fonctionne correctement!")
        else:
            print(f"\n⚠️ Problème détecté")
            if response.status_code == 403:
                print("Le verify_token ne correspond pas")
                print("Vérifiez la variable FACEBOOK_VERIFY_TOKEN dans .env")
            
    except Exception as e:
        print(f"\n❌ ERREUR: {type(e).__name__}")
        print(f"Message: {str(e)}")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "TEST WEBHOOK FACEBOOK MESSENGER" + " " * 26 + "║")
    print("╚" + "=" * 78 + "╝")
    print("\n")
    
    # Permettre de choisir le test
    if len(sys.argv) > 1:
        if sys.argv[1] == "get":
            test_webhook_get()
        elif sys.argv[1] == "post":
            test_webhook_post()
        elif sys.argv[1] == "all":
            test_webhook_get()
            print("\n\n")
            test_webhook_post()
        else:
            print(f"❌ Argument inconnu: {sys.argv[1]}")
            print("\nUtilisation:")
            print("  python test_webhook_post.py get    # Test GET uniquement")
            print("  python test_webhook_post.py post   # Test POST uniquement")
            print("  python test_webhook_post.py all    # Test GET + POST")
    else:
        # Par défaut, tester les deux
        test_webhook_get()
        print("\n\n")
        test_webhook_post()
    
    print("\n💡 Consultez MESSENGER_DEBUG_GUIDE.md pour analyser les logs\n")
