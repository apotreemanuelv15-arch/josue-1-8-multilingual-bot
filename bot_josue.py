import os
import requests
from twilio.rest import Client

def executer_mission():
    api_key = os.environ["BOT_GEMINI_KEY"]
    twilio_sid = os.environ["TWILIO_SID"]
    twilio_token = os.environ["TWILIO_TOKEN"]
    
    print("🚀 Repli tactique sur Gemini 2.0 Flash-Lite (Plus de quota)...")

    # On utilise la version LITE qui a généralement ses propres limites séparées
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash-lite:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{
            "parts": [{"text": "Tu es l'Aumônier du QG Josué 1:8. Génère un message de motivation biblique puissant en 3 langues : Français (FR), Portugais (PT), et Anglais (EN)."}]
        }]
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        result = response.json()
        
        if response.status_code != 200:
            # Si le Lite échoue aussi, on tente une dernière fois le 1.5-flash-latest
            print("⚠️ Lite bloqué, tentative sur 1.5-flash-latest...")
            url_backup = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
            response = requests.post(url_backup, json=payload, headers=headers, timeout=30)
            result = response.json()

        if response.status_code != 200:
            raise Exception(f"Quota toujours épuisé: {result.get('error', {}).get('message')}")

        message_ia = result['candidates'][0]['content']['parts'][0]['text']
        print("✅ Message généré !")

        # Expédition Twilio
        client = Client(twilio_sid, twilio_token)
        client.messages.create(
            from_=os.environ["TWILIO_NUMBER"],
            body=message_ia,
            to=os.environ["TARGET_NUMBER"]
        )
        print("✅ Message envoyé sur WhatsApp !")

    except Exception as e:
        print(f"❌ Rapport : {str(e)}")

if __name__ == "__main__":
    executer_mission()
