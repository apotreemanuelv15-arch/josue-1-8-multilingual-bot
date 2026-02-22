import os
import requests
from twilio.rest import Client

def executer_mission():
    api_key = os.environ.get("BOT_GEMINI_KEY")
    twilio_sid = os.environ.get("TWILIO_SID")
    twilio_token = os.environ.get("TWILIO_TOKEN")
    twilio_number = os.environ.get("TWILIO_NUMBER")
    target_number = os.environ.get("TARGET_NUMBER")
    
    # On teste les 3 formats d'URL possibles en 2026
    tests = [
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent",
        "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent",
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    ]
    
    payload = {"contents": [{"parts": [{"text": "Message court Josué 1:8"}]}]}
    
    print("🚀 Test de pénétration multi-canaux...")

    for url in tests:
        full_url = f"{url}?key={api_key}"
        print(f"📡 Essai sur : {url}")
        try:
            res = requests.post(full_url, json=payload, timeout=15)
            if res.status_code == 200:
                print("✅ PERCÉE RÉUSSIE !")
                message = res.json()['candidates'][0]['content']['parts'][0]['text']
                
                # Envoi Twilio
                client = Client(twilio_sid, twilio_token)
                client.messages.create(from_=twilio_number, body=message, to=target_number)
                print("🏁 WhatsApp expédié !")
                return
            else:
                print(f"❌ Échec ({res.status_code})")
        except:
            print("⚠️ Erreur réseau")

    print("🆘 Aucune porte ne s'est ouverte.")

if __name__ == "__main__":
    executer_mission()
