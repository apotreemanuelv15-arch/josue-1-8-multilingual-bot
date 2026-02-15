import os
import google.generativeai as genai
from twilio.rest import Client
import requests
import urllib.parse

# Configuration
genai.configure(api_key=os.environ["BOT_GEMINI_KEY"])
twilio_client = Client(os.environ["TWILIO_SID"], os.environ["TWILIO_TOKEN"])

def executer_mission():
    try:
        # On force le modèle 1.5-flash qui est le plus robuste pour les clés gratuites
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = "Tu es l'Aumônier du QG Josué 1:8. Génère un court message de motivation biblique en FR, PT et EN."
        
        print("🔄 Contact avec l'intelligence du QG...")
        response = model.generate_content(prompt)
        message = response.text
        
        # Préparation de l'image
        image_url = "https://image.pollinations.ai/prompt/biblical%20sunrise%20epic?width=1024&height=1024"

        # Envoi WhatsApp
        twilio_client.messages.create(
            from_=os.environ["TWILIO_NUMBER"],
            body=message,
            media_url=[image_url],
            to=os.environ["TARGET_NUMBER"]
        )
        
        print("✅ Mission accomplie : Message envoyé !")
        
    except Exception as e:
        print(f"❌ Erreur tactique finale : {str(e)}")

if __name__ == "__main__":
    executer_mission()
