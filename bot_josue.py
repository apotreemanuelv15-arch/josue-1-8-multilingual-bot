import os
import requests
from twilio.rest import Client

def executer_mission():
    api_key = os.environ.get("BOT_GEMINI_KEY")
    twilio_sid = os.environ.get("TWILIO_SID")
    twilio_token = os.environ.get("TWILIO_TOKEN")
    twilio_number = os.environ.get("TWILIO_NUMBER")
    target_number = os.environ.get("TARGET_NUMBER")
    
    # Stratégie de repli sur le modèle PRO (souvent des quotas différents)
    modeles_a_tester = [
        "gemini-1.5-pro",
        "gemini-1.5-pro-latest",
        "gemini-pro"
    ]
    
    prompt = "Tu es l'Aumônier du QG Josué 1:8. Génère un message de motivation biblique puissant en 3 langues : Français (FR), Portugais (PT), et Anglais (EN). Structure : 📖 VERSET DU JOUR, 🛡️ MÉDITATION, 💡 CONSEIL TACTIQUE."
    
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {'Content-Type': 'application/json'}

    print("🚀 Tentative d'infiltration via les modèles PRO...")

    message_ia = None
    for modele in modeles_a_tester:
        print(f"📡 Test du modèle : {modele}...")
        # On utilise l'URL v1 (stable)
        url = f"https://generativelanguage.googleapis.com/v1/models/{modele}:generateContent?key={api_key}"
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            result = response.json()
            
            if response.status_code == 200:
                message_ia = result['candidates'][0]['content']['parts'][0]['text']
                print(f"✅ PERCÉE RÉUSSIE avec {modele} !")
                break
            else:
                msg = result.get('error', {}).get('message', 'Inconnu')
                print(f"⚠️ {modele} rejette la liaison : {msg}")
        except Exception as e:
            print(f"❌ Erreur technique : {str(e)}")

    if message_ia:
        try:
            client = Client(twilio_sid, twilio_token)
            client.messages.create(
                from_=twilio_number,
                body=message_ia,
                to=target_number
            )
            print("🏁 VICTOIRE ! Message expédié sur WhatsApp.")
        except Exception as e:
            print(f"❌ Erreur Twilio : {str(e)}")
    else:
        print("🆘 Mur de quota toujours infranchissable.")

if __name__ == "__main__":
    executer_mission()
