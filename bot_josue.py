import os
import requests
from twilio.rest import Client

def executer_mission():
    api_key = os.environ.get("BOT_GEMINI_KEY")
    twilio_sid = os.environ.get("TWILIO_SID")
    twilio_token = os.environ.get("TWILIO_TOKEN")
    twilio_number = os.environ.get("TWILIO_NUMBER")
    target_number = os.environ.get("TARGET_NUMBER")
    
    # UTILISATION DU MODÈLE DÉTECTÉ DANS VOTRE SCAN
    modele_detecte = "models/gemini-2.0-flash"
    url = f"https://generativelanguage.googleapis.com/v1/ {modele_detecte}:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{"text": "Tu es l'Aumônier Josué 1:8. Génère un message de motivation biblique puissant en 3 langues : Français (FR), Portugais (PT), et Anglais (EN). Structure : 📖 VERSET, 🛡️ MÉDITATION, 💡 CONSEIL."}]
        }]
    }

    print(f"🚀 ATTAQUE FINALE avec le modèle : {modele_detecte}...")

    try:
        response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'}, timeout=30)
        
        if response.status_code == 200:
            message_ia = response.json()['candidates'][0]['content']['parts'][0]['text']
            print("✨ VICTOIRE ! L'IA a répondu avec succès.")
            
            # Envoi Twilio
            client = Client(twilio_sid, twilio_token)
            client.messages.create(body=message_ia, from_=twilio_number, to=target_number)
            print(f"🏁 MISSION ACCOMPLIE : Message envoyé au {target_number} !")
        else:
            print(f"❌ Erreur Google ({response.status_code}) : {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur système : {str(e)}")

if __name__ == "__main__":
    executer_mission()
