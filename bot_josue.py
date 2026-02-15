import os
import google.generativeai as genai
from twilio.rest import Client
import requests
import urllib.parse

# Configuration des APIs - Utilisation du nouveau secret sécurisé
genai.configure(api_key=os.environ["BOT_GEMINI_KEY"])
twilio_client = Client(os.environ["TWILIO_SID"], os.environ["TWILIO_TOKEN"])

def generer_ration_spirituelle():
    # Liste de modèles pour garantir le succès
    modeles_a_tester = [
        'gemini-1.5-flash',
        'gemini-pro',
        'models/gemini-1.5-flash'
    ]
    
    prompt = """
    Tu es l'Aumônier du QG Josué 1:8. 
    Génère un message de motivation biblique puissant en 3 langues : Français (FR), Portugais (PT), et Anglais (EN).
    Structure pour chaque langue :
    📖 VERSET DU JOUR (Référence et texte)
    🛡️ MÉDITATION (2 phrases de leadership)
    💡 CONSEIL TACTIQUE (1 phrase d'action)
    """

    for nom_modele in modeles_a_tester:
        try:
            print(f"🔄 Tentative d'activation avec : {nom_modele}...")
            model = genai.GenerativeModel(nom_modele)
            response = model.generate_content(prompt)
            return response.text
        except Exception:
            continue
    
    raise Exception("Aucun modèle n'a répondu. Vérifiez la validité de BOT_GEMINI_KEY.")

def executer_mission():
    try:
        # 1. Génération
        message = generer_ration_spirituelle()
        
        # 2. Image
        prompt_img = urllib.parse.quote("cinematic biblical sunrise, epic landscape, courage, high resolution")
        image_url = f"https://image.pollinations.ai/prompt/{prompt_img}?width=1024&height=1024&nologo=true"

        # 3. Envoi Telegram
        try:
            tg_token = os.environ.get("TELEGRAM_TOKEN")
            tg_id = os.environ.get("TELEGRAM_CHAT_ID")
            if tg_token and tg_id:
                requests.post(f"https://api.telegram.org/bot{tg_token}/sendPhoto", 
                              data={'chat_id': tg_id, 'caption': message},
                              files={'photo': requests.get(image_url).content}, timeout=15)
        except:
            print("⚠️ Telegram en attente.")

        # 4. Envoi WhatsApp
        twilio_client.messages.create(
            from_=os.environ["TWILIO_NUMBER"],
            body=message,
            media_url=[image_url],
            to=os.environ["TARGET_NUMBER"]
        )
        
        print("✅ Mission accomplie : La ration spirituelle est livrée.")
        
    except Exception as e:
        print(f"❌ Erreur tactique : {str(e)}")

if __name__ == "__main__":
    executer_mission()
