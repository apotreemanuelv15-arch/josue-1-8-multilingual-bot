import os
import requests
from twilio.rest import Client

def executer_mission():
    api_key = os.environ["BOT_GEMINI_KEY"]
    twilio_sid = os.environ["TWILIO_SID"]
    twilio_token = os.environ["TWILIO_TOKEN"]
    
    # Liste des modèles détectés hier, par ordre de probabilité de succès
    modeles_a_tester = [
        "gemini-2.0-flash-lite-001",
        "gemini-2.0-flash",
        "gemini-2.0-flash-001"
    ]
    
    payload = {
        "contents": [{
            "parts": [{"text": "Tu es l'Aumônier du QG Josué 1:8. Génère un message de motivation biblique puissant en 3 langues : Français (FR), Portugais (PT), et Anglais (EN). Structure : 📖 VERSET DU JOUR, 🛡️ MÉDITATION, 💡 CONSEIL TACTIQUE."}]
        }]
    }
    headers = {'Content-Type': 'application/json'}

    print("🚀 Début de l'offensive matinale...")

    for modele in modeles_a_tester:
        print(f"📡 Tentative de liaison avec {modele}...")
        url = f"https://generativelanguage.googleapis.com/v1/models/{modele}:generateContent?key={api_key}"
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            result = response.json()
            
            if response.status_code == 200:
                message_ia = result['candidates'][0]['content']['parts'][0]['text']
                print(f"✅ Victoire tactique avec {modele} !")
                
                # Envoi WhatsApp
                client = Client(twilio_sid, twilio_token)
                client.messages.create(
                    from_=os.environ["TWILIO_NUMBER"],
                    body=message_ia,
                    to=os.environ["TARGET_NUMBER"]
                )
                print("📱 Message transmis au destinataire avec succès.")
                return # Mission terminée avec succès
            
            else:
                erreur = result.get('error', {}).get('message', 'Erreur inconnue')
                print(f"⚠️ Échec avec {modele} : {erreur}")
                
        except Exception as e:
            print(f"❌ Erreur de connexion sur {modele} : {str(e)}")

    print("🆘 Toutes les tentatives ont échoué. Le quota semble encore verrouillé.")

if __name__ == "__main__":
    executer_mission()
