import os
import requests
from twilio.rest import Client

def executer_mission():
    # Secrets GitHub
    api_key = os.environ.get("BOT_GEMINI_KEY")
    twilio_sid = os.environ.get("TWILIO_SID")
    twilio_token = os.environ.get("TWILIO_TOKEN")
    twilio_number = os.environ.get("TWILIO_NUMBER")
    target_number = os.environ.get("TARGET_NUMBER")
    
    # URL spécifique pour les clés AI Studio (Free Tier)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{"text": "Tu es l'Aumônier Josué 1:8. Donne un message de force court en FR, EN et PT."}]
        }]
    }

    print("🚀 Tentative via le canal AI Studio Gratuit...")

    try:
        response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'}, timeout=30)
        
        if response.status_code == 200:
            message_ia = response.json()['candidates'][0]['content']['parts'][0]['text']
            print("✨ VICTOIRE ! La barrière bancaire est contournée.")
            
            client = Client(twilio_sid, twilio_token)
            client.messages.create(body=message_ia, from_=twilio_number, to=target_number)
            print("🏁 Message envoyé sur WhatsApp !")
        else:
            print(f"❌ Erreur : {response.text}")
            
    except Exception as e:
        print(f"⚠️ Incident : {str(e)}")

if __name__ == "__main__":
    executer_mission()
