import os
from google import genai
from twilio.rest import Client
import requests
import urllib.parse

# 1. Connexion en forçant la version STABLE de l'API (pas la beta)
client = genai.Client(
    api_key=os.environ["BOT_GEMINI_KEY"],
    http_options={'api_version': 'v1'} # On force le passage par la version stable
)
twilio_client = Client(os.environ["TWILIO_SID"], os.environ["TWILIO_TOKEN"])

def executer_mission():
    try:
        print("🔄 Tentative de percée via la version Stable (v1)...")
        
        prompt = "Tu es l'Aumônier du QG Josué 1:8. Génère un court message biblique en FR, PT, EN."
        
        # On utilise le nom de modèle pur, sans préfixe complexe
        response = client.models.generate_content(
            model="gemini-1.5-flash", 
            contents=prompt
        )
        message = response.text
        
        # 3. Préparation de l'image
        image_url = "https://image.pollinations.ai/prompt/biblical%20sunrise?width=1024&height=1024"

        # 4. Envoi WhatsApp
        twilio_client.messages.create(
            from_=os.environ["TWILIO_NUMBER"],
            body=message,
            media_url=[image_url],
            to=os.environ["TARGET_NUMBER"]
        )
        
        print("✅ VICTOIRE : La liaison est établie et le message est envoyé !")
        
    except Exception as e:
        print(f"❌ Erreur tactique persistante : {str(e)}")

if __name__ == "__main__":
    executer_mission()
