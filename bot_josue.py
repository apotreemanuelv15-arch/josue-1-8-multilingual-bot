import os
import requests
from twilio.rest import Client

def executer_mission():
    api_key = os.environ.get("BOT_GEMINI_KEY")
    twilio_sid = os.environ.get("TWILIO_SID")
    twilio_token = os.environ.get("TWILIO_TOKEN")
    twilio_number = os.environ.get("TWILIO_NUMBER")
    target_number = os.environ.get("TARGET_NUMBER")
    
    # Utilisation du nom long officiel 2026
    modele_final = "models/gemini-1.5-flash"
    url = f"https://generativelanguage.googleapis.com/v1beta/{modele_final}:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{"text": "Génère un message puissant de motivation chrétienne (Josué 1:8) en FR, EN, PT."}]
        }]
    }

    print(f"📡 Offensive finale sur {modele_final}...")

    try:
        response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'}, timeout=30)
        
        if response.status_code == 200:
            message = response.json()['candidates'][0]['content']['parts'][0]['text']
            print("✅ L'IA A RÉPONDU ! Connexion établie.")
            
            client = Client(twilio_sid, twilio_token)
            client.messages.create(from_=twilio_number, body=message, to=target_number)
            print("🏁 MESSAGE ENVOYÉ SUR WHATSAPP !")
        else:
            print(f"❌ Erreur Google : {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur système : {str(e)}")

if __name__ == "__main__":
    executer_mission()
