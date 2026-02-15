import os
from google import genai
from twilio.rest import Client
import requests
import urllib.parse

# 1. Connexion au nouveau moteur Gemini
client = genai.Client(api_key=os.environ["BOT_GEMINI_KEY"])
twilio_client = Client(os.environ["TWILIO_SID"], os.environ["TWILIO_TOKEN"])

def executer_mission():
    try:
        print("🔄 Connexion au QG via le nouveau moteur 2026...")
        
        # 2. Génération du message
        prompt = """
        Tu es l'Aumônier du QG Josué 1:8. 
        Génère un message de motivation biblique puissant en 3 langues : Français (FR), Portugais (PT), et Anglais (EN).
        Structure : 📖 VERSET DU JOUR, 🛡️ MÉDITATION (2 phrases), 💡 CONSEIL TACTIQUE.
        """
        
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        message = response.text
        
        # 3. Préparation de l'image
        prompt_img = urllib.parse.quote("cinematic biblical sunrise, epic landscape, courage")
        image_url = f"https://image.pollinations.ai/prompt/{prompt_img}?width=1024&height=1024"

        # 4. Envoi WhatsApp via Twilio
        twilio_client.messages.create(
            from_=os.environ["TWILIO_NUMBER"],
            body=message,
            media_url=[image_url],
            to=os.environ["TARGET_NUMBER"]
        )
        
        print("✅ Mission accomplie : La ration spirituelle est livrée !")
        
    except Exception as e:
        print(f"❌ Erreur tactique : {str(e)}")

if __name__ == "__main__":
    executer_mission()
