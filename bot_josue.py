import os
import requests
from twilio.rest import Client

def executer_mission():
    api_key = os.environ.get("BOT_GEMINI_KEY")
    twilio_sid = os.environ.get("TWILIO_SID")
    twilio_token = os.environ.get("TWILIO_TOKEN")
    twilio_number = os.environ.get("TWILIO_NUMBER")
    target_number = os.environ.get("TARGET_NUMBER")
    
    # On utilise le nom simple et la version v1 (stable)
    modele = "gemini-1.5-flash"
    url = f"https://generativelanguage.googleapis.com/v1/models/{modele}:generateContent?key={api_key}"
    
    prompt = "Tu es l'Aumônier du QG Josué 1:8. Génère un message de motivation biblique puissant en 3 langues : Français (FR), Portugais (PT), et Anglais (EN). Structure : 📖 VERSET DU JOUR, 🛡️ MÉDITATION, 💡 CONSEIL TACTIQUE."
    
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    print(f"🎯 Tentative de frappe directe via v1 avec {modele}...")

    try:
        response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'}, timeout=30)
        result = response.json()
        
        if response.status_code == 200:
            message_ia = result['candidates'][0]['content']['parts'][0]['text']
            print("✅ Victoire ! Message généré.")
            
            client = Client(twilio_sid, twilio_token)
            client.messages.create(from_=twilio_number, body=message_ia, to=target_number)
            print("🏁 Envoyé sur WhatsApp !")
        else:
            # Si v1 échoue encore, on tente un dernier recours immédiat avec v1beta et un nom différent
            print("⚠️ v1 a échoué, tentative de repli immédiat...")
            url_alt = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
            response = requests.post(url_alt, json=payload, headers={'Content-Type': 'application/json'}, timeout=30)
            
            if response.status_code == 200:
                print("✅ Sauvetage réussi avec gemini-pro !")
                message_ia = response.json()['candidates'][0]['content']['parts'][0]['text']
                client = Client(twilio_sid, twilio_token)
                client.messages.create(from_=twilio_number, body=message_ia, to=target_number)
            else:
                print(f"❌ Échec critique : {response.text}")
                
    except Exception as e:
        print(f"❌ Erreur : {str(e)}")

if __name__ == "__main__":
    executer_mission()
