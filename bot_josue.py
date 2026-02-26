import os
import requests
from twilio.rest import Client

def executer_mission():
    api_key = os.environ.get("BOT_GEMINI_KEY")
    twilio_sid = os.environ.get("TWILIO_SID")
    twilio_token = os.environ.get("TWILIO_TOKEN")
    twilio_number = os.environ.get("TWILIO_NUMBER")
    target_number = os.environ.get("TARGET_NUMBER")
    
    # URL STABLE POUR AI STUDIO
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{"text": "Tu es l'Aumônier Josué 1:8. Génère un message de motivation biblique puissant en FR, PT, et EN."}]
        }]
    }

    print("🛰️ Connexion au canal AI Studio (Mode Stable)...")

    try:
        response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'}, timeout=30)
        
        # Si 404, on tente immédiatement la version "latest"
        if response.status_code == 404:
            print("🔄 Modèle standard non trouvé, tentative sur 'gemini-1.5-flash-latest'...")
            url_alt = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
            response = requests.post(url_alt, json=payload, headers={'Content-Type': 'application/json'}, timeout=30)

        if response.status_code == 200:
            message_ia = response.json()['candidates'][0]['content']['parts'][0]['text']
            print("✅ RÉUSSITE TOTALE ! Message généré.")
            
            client = Client(twilio_sid, twilio_token)
            client.messages.create(body=message_ia, from_=twilio_number, to=target_number)
            print(f"🏁 MISSION ACCOMPLIE : WhatsApp envoyé !")
        else:
            print(f"❌ Erreur finale ({response.status_code}) : {response.text}")
            
    except Exception as e:
        print(f"⚠️ Incident technique : {str(e)}")

if __name__ == "__main__":
    executer_mission()
