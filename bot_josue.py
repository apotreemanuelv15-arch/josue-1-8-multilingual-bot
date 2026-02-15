import os
import requests
from twilio.rest import Client

def executer_mission():
    # Récupération des munitions
    api_key = os.environ["BOT_GEMINI_KEY"]
    twilio_sid = os.environ["TWILIO_SID"]
    twilio_token = os.environ["TWILIO_TOKEN"]
    
    print("🚀 Connexion directe établie. Génération de la ration spirituelle...")

    # 1. Appel direct à l'API Google (Méthode la plus stable)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{
            "parts": [{"text": "Tu es l'Aumônier du QG Josué 1:8. Génère un message de motivation biblique puissant en 3 langues : Français (FR), Portugais (PT), et Anglais (EN). Structure : 📖 VERSET DU JOUR, 🛡️ MÉDITATION, 💡 CONSEIL TACTIQUE."}]
        }]
    }

    try:
        # Timeout de 30s pour éviter les blocages infinis
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        result = response.json()
        
        if response.status_code != 200:
            raise Exception(f"Erreur Google: {result}")

        message_ia = result['candidates'][0]['content']['parts'][0]['text']
        print("✅ Message généré par l'IA.")

        # 2. Préparation de l'image d'illustration
        image_url = "https://image.pollinations.ai/prompt/biblical%20sunrise%20warrior%20cinematic?width=1024&height=1024"

        # 3. Expédition via Twilio
        client = Client(twilio_sid, twilio_token)
        client.messages.create(
            from_=os.environ["TWILIO_NUMBER"],
            body=message_ia,
            media_url=[image_url],
            to=os.environ["TARGET_NUMBER"]
        )
        print("✅ Mission accomplie : La ration est sur WhatsApp !")

    except Exception as e:
        print(f"❌ Échec de la mission : {str(e)}")

if __name__ == "__main__":
    executer_mission()
