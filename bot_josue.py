import os
import requests
from twilio.rest import Client

def executer_mission():
    api_key = os.environ["BOT_GEMINI_KEY"]
    twilio_sid = os.environ["TWILIO_SID"]
    twilio_token = os.environ["TWILIO_TOKEN"]
    
    print("🚀 Assaut final avec le modèle Gemini 2.0 Flash...")

    # Utilisation du modèle 2.0 détecté dans votre scan
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{
            "parts": [{"text": "Tu es l'Aumônier du QG Josué 1:8. Génère un message de motivation biblique puissant en 3 langues : Français (FR), Portugais (PT), et Anglais (EN). Structure : 📖 VERSET DU JOUR, 🛡️ MÉDITATION, 💡 CONSEIL TACTIQUE."}]
        }]
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        result = response.json()
        
        if response.status_code != 200:
            raise Exception(f"Erreur Google: {result}")

        # Extraction du texte (la structure reste la même en 2.0)
        message_ia = result['candidates'][0]['content']['parts'][0]['text']
        print("✅ Message généré par la nouvelle génération d'IA (2.0).")

        # Image d'illustration
        image_url = "https://image.pollinations.ai/prompt/epic%20biblical%20sunrise%20victory?width=1024&height=1024"

        # Expédition Twilio
        client = Client(twilio_sid, twilio_token)
        client.messages.create(
            from_=os.environ["TWILIO_NUMBER"],
            body=message_ia,
            media_url=[image_url],
            to=os.environ["TARGET_NUMBER"]
        )
        print("✅ MISSION ACCOMPLIE : Votre téléphone va vibrer !")

    except Exception as e:
        print(f"❌ Erreur de dernière minute : {str(e)}")

if __name__ == "__main__":
    executer_mission()
