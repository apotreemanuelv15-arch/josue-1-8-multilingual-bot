import os
import requests
from twilio.rest import Client

def executer_mission():
    # 1. Récupération des secrets
    api_key = os.environ.get("BOT_GEMINI_KEY")
    twilio_sid = os.environ.get("TWILIO_SID")
    twilio_token = os.environ.get("TWILIO_TOKEN")
    twilio_number = os.environ.get("TWILIO_NUMBER")
    target_number = os.environ.get("TARGET_NUMBER")
    
    # Le modèle Flash 1.5 est le plus fiable une fois l'API activée
    modele = "gemini-1.5-flash"
    
    prompt = "Tu es l'Aumônier du QG Josué 1:8. Génère un message de motivation biblique puissant en 3 langues : Français (FR), Portugais (PT), et Anglais (EN). Structure : 📖 VERSET DU JOUR, 🛡️ MÉDITATION, 💡 CONSEIL TACTIQUE."
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{modele}:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {'Content-Type': 'application/json'}

    print(f"🚀 Lancement de la génération avec {modele}...")

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        result = response.json()
        
        if response.status_code == 200:
            message_ia = result['candidates'][0]['content']['parts'][0]['text']
            print("✅ Message généré avec succès !")
            
            # Préparation de l'image
            image_url = "https://image.pollinations.ai/prompt/warrior%20kneeling%20at%20sunrise%20biblical%20cinematic?width=1024&height=1024"
            
            # Envoi Twilio
            client = Client(twilio_sid, twilio_token)
            client.messages.create(
                from_=twilio_number,
                body=message_ia,
                media_url=[image_url],
                to=target_number
            )
            print("🏁 MISSION ACCOMPLIE. Le message et l'image sont en route !")
        else:
            erreur = result.get('error', {}).get('message', 'Erreur inconnue')
            print(f"❌ Échec Google API : {erreur}")
            
    except Exception as e:
        print(f"⚠️ Incident technique : {str(e)}")

if __name__ == "__main__":
    executer_mission()
