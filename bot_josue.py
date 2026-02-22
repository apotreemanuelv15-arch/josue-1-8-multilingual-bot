import os
import requests
from twilio.rest import Client

def executer_mission():
    api_key = os.environ.get("BOT_GEMINI_KEY")
    twilio_sid = os.environ.get("TWILIO_SID")
    twilio_token = os.environ.get("TWILIO_TOKEN")
    twilio_number = os.environ.get("TWILIO_NUMBER")
    target_number = os.environ.get("TARGET_NUMBER")
    
    # Noms de modèles ultra-précis pour 2026
    modeles_a_tester = [
        "gemini-1.5-pro-002",
        "gemini-1.5-flash-002",
        "gemini-1.5-pro",
        "gemini-2.0-flash-exp"
    ]
    
    prompt = "Tu es l'Aumônier du QG Josué 1:8. Génère un message de motivation biblique puissant en 3 langues : Français (FR), Portugais (PT), et Anglais (EN). Structure : 📖 VERSET DU JOUR, 🛡️ MÉDITATION, 💡 CONSEIL TACTIQUE."
    
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {'Content-Type': 'application/json'}

    print("🎯 Lancement de la frappe de précision (v1beta)...")

    message_ia = None
    for modele in modeles_a_tester:
        print(f"📡 Connexion au modèle : {modele}...")
        # UTILISATION DE v1beta (indispensable pour les nouveaux comptes)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{modele}:generateContent?key={api_key}"
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            result = response.json()
            
            if response.status_code == 200:
                message_ia = result['candidates'][0]['content']['parts'][0]['text']
                print(f"✨ SUCCÈS ! Liaison établie avec {modele}.")
                break
            else:
                erreur_msg = result.get('error', {}).get('message', 'Non spécifié')
                print(f"❌ Rejet de {modele} : {erreur_msg}")
        except Exception as e:
            print(f"⚠️ Incident technique sur {modele} : {str(e)}")

    if message_ia:
        try:
            client = Client(twilio_sid, twilio_token)
            client.messages.create(
                from_=twilio_number,
                body=message_ia,
                to=target_number
            )
            print("🚀 MISSION RÉUSSIE : Message envoyé au QG !")
        except Exception as e:
            print(f"❌ Erreur finale Twilio : {str(e)}")
    else:
        print("🚩 ÉCHEC : Google bloque l'accès externe. Vérifiez si l'API Gemini est activée dans Google Cloud Console.")

if __name__ == "__main__":
    executer_mission()
