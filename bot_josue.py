import os
import google.generativeai as genai
from twilio.rest import Client
import requests
import urllib.parse

# Config APIs
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
twilio_client = Client(os.environ["TWILIO_SID"], os.environ["TWILIO_TOKEN"])

def generer_ration_spirituelle():
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = """
    Tu es l'Aumônier du QG Josué 1:8. 
    Génère un message de motivation biblique puissant en 3 langues : Français (FR), Portugais (PT), et Anglais (EN).
    
    Structure pour chaque langue :
    📖 VERSET DU JOUR (Référence et texte)
    🛡️ MÉDITATION (2 phrases de leadership)
    💡 CONSEIL TACTIQUE (1 phrase d'action)
    """
    response = model.generate_content(prompt)
    return response.text

def executer_mission():
    try:
        message = generer_ration_spirituelle()
        
        # Image universelle
        prompt_img = urllib.parse.quote("cinematic biblical sunrise, epic landscape, courage, high resolution")
        image_url = f"https://image.pollinations.ai/prompt/{prompt_img}?width=1024&height=1024&nologo=true"

        # 1. Envoi Telegram
        tg_token = os.environ["TELEGRAM_TOKEN"]
        tg_id = os.environ["TELEGRAM_CHAT_ID"]
        requests.post(f"https://api.telegram.org/bot{tg_token}/sendPhoto", 
                      data={'chat_id': tg_id, 'caption': message},
                      files={'photo': requests.get(image_url).content})

        # 2. Envoi WhatsApp
        twilio_client.messages.create(
            from_=os.environ["TWILIO_NUMBER"],
            body=message,
            media_url=[image_url],
            to=os.environ["TARGET_NUMBER"]
        )
        
        print("✅ Mission accomplie : La ration spirituelle est livrée au Commandant.")
    except Exception as e:
        print(f"❌ Erreur tactique : {e}")

if __name__ == "__main__":
    executer_mission()
