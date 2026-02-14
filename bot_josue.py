import os
import google.generativeai as genai
from twilio.rest import Client
import requests
import urllib.parse

# Configuration des APIs
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
twilio_client = Client(os.environ["TWILIO_SID"], os.environ["TWILIO_TOKEN"])

def generer_ration_spirituelle():
    # Liste de munitions (modèles) du plus récent au plus compatible
    modeles_a_tester = [
        'gemini-1.5-flash',
        'gemini-pro',
        'models/gemini-1.5-flash',
        'models/gemini-pro'
    ]
    
    prompt = """
    Tu es l'Aumônier du QG Josué 1:8. 
    Génère un message de motivation biblique puissant en 3 langues : Français (FR), Portugais (PT), et Anglais (EN).
    Structure : 📖 VERSET DU JOUR, 🛡️ MÉDITATION, 💡 CONSEIL TACTIQUE.
    """

    for nom_modele in modeles_a_tester:
        try:
            print(f"🔄 Tentative avec le modèle : {nom_modele}...")
            model = genai.GenerativeModel(nom_modele)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"⚠️ Échec avec {nom_modele}")
            continue
    
    raise Exception("Aucun modèle Gemini n'est accessible avec cette clé API.")

def executer_mission():
    try:
        message = generer_ration_spirituelle()
        
        prompt_img = urllib.parse.quote("cinematic biblical sunrise, epic landscape, courage, high resolution")
        image_url = f"https://image.pollinations.ai/prompt/{prompt_img}?width=1024&height=1024&nologo=true"

        # Envoi Telegram
        try:
            tg_token = os.environ.get("TELEGRAM_TOKEN")
            tg_id = os.environ.get("TELEGRAM_CHAT_ID")
            if tg_token and tg_id:
                requests.post(f"https://api.telegram.org/bot{tg_token}/sendPhoto", 
                              data={'chat_id': tg_id, 'caption': message},
                              files={'photo': requests.get(image_url).content}, timeout=10)
        except:
            print("⚠️ Telegram non disponible")

        # Envoi WhatsApp
        twilio_client.messages.create(
            from_=os.environ["TWILIO_NUMBER"],
            body=message,
            media_url=[image_url],
            to=os.environ["TARGET_NUMBER"]
        )
        
        print("✅ Mission accomplie : La ration spirituelle est livrée.")
        
    except Exception as e:
        print(f"❌ Erreur tactique fatale : {str(e)}")

if __name__ == "__main__":
    executer_mission()
