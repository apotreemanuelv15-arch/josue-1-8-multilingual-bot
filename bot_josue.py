import os
from google import genai
from twilio.rest import Client
import requests
import urllib.parse

# 1. Connexion avec la nouvelle bibliothèque
client = genai.Client(api_key=os.environ["BOT_GEMINI_KEY"])
twilio_client = Client(os.environ["TWILIO_SID"], os.environ["TWILIO_TOKEN"])

def executer_mission():
    try:
        print("🔄 Tentative avec le modèle Vétéran (Gemini 1.0 Pro)...")
        
        prompt = """
        Tu es l'Aumônier du QG Josué 1:8. 
        Génère un message de motivation biblique en 3 langues : Français, Portugais, Anglais.
        Format : Verset, Méditation, Conseil.
        """
        
        # On force ici le modèle 1.0-pro (le plus compatible)
        response = client.models.generate_content(
            model="gemini-1.0-pro", 
            contents=prompt
        )
        message = response.text
        
        # 3. Préparation de l'image
        image_url = "https://image.pollinations.ai/prompt/biblical%20mountain%20sunrise?width=1024&height=1024"

        # 4. Envoi WhatsApp
        twilio_client.messages.create(
            from_=os.environ["TWILIO_NUMBER"],
            body=message,
            media_url=[image_url],
            to=os.environ["TARGET_NUMBER"]
        )
        
        print("✅ Mission accomplie : Le message est parti !")
        
    except Exception as e:
        print(f"❌ Erreur tactique : {str(e)}")

if __name__ == "__main__":
    executer_mission()
