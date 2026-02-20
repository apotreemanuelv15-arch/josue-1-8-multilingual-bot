import os
import requests
from twilio.rest import Client

def executer_mission():
    # 1. Récupération des munitions (Secrets)
    api_key = os.environ.get("BOT_GEMINI_KEY")
    twilio_sid = os.environ.get("TWILIO_SID")
    twilio_token = os.environ.get("TWILIO_TOKEN")
    twilio_number = os.environ.get("TWILIO_NUMBER")
    target_number = os.environ.get("TARGET_NUMBER")
    
    # 2. Liste tactique des modèles (du plus récent au plus stable)
    modeles_a_tester = [
        "gemini-2.0-flash-lite-preview-02-05", # Version ultra-récente 2026
        "gemini-2.0-flash-lite",
        "gemini-2.0-flash",
        "gemini-1.5-flash"
    ]
    
    prompt = "Tu es l'Aumônier du QG Josué 1:8. Génère un message de motivation biblique puissant en 3 langues : Français (FR), Portugais (PT), et Anglais (EN). Structure : 📖 VERSET DU JOUR, 🛡️ MÉDITATION, 💡 CONSEIL TACTIQUE."
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    headers = {'Content-Type': 'application/json'}

    print("🚀 Lancement de l'opération de génération...")

    message_ia = None
    for modele in modeles_a_tester:
        print(f"📡 Tentative avec {modele}...")
        # On teste en version v1beta (plus flexible pour les nouveaux modèles)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{modele}:generateContent?key={api_key}"
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            result = response.json()
            
            if response.status_code == 200:
                message_ia = result['candidates'][0]['content']['parts'][0]['text']
                print(f"✅ Victoire ! Le modèle {modele} a répondu.")
                break
            else:
                msg_erreur = result.get('error', {}).get('message', 'Erreur inconnue')
                print(f"⚠️ Échec avec {modele} : {msg_erreur}")
        except Exception as e:
            print(f"❌ Erreur technique sur {modele} : {str(e)}")

    # 3. Phase d'expédition si le message a été généré
    if message_ia:
        try:
            print("🎨 Préparation de l'image d'illustration...")
            image_url = "https://image.pollinations.ai/prompt/warrior%20kneeling%20at%20sunrise%20biblical%20cinematic?width=1024&height=1024"
            
            print("📱 Expédition WhatsApp via Twilio...")
            client = Client(twilio_sid, twilio_token)
            client.messages.create(
                from_=twilio_number,
                body=message_ia,
                media_url=[image_url],
                to=target_number
            )
            print("🏁 MISSION ACCOMPLIE. Le message est en route !")
        except Exception as e:
            print(f"❌ Erreur lors de l'envoi Twilio : {str(e)}")
    else:
        print("🆘 ÉCHEC TOTAL : Aucun modèle n'a pu générer de texte. Vérifiez votre clé sur Google AI Studio.")

if __name__ == "__main__":
    executer_mission()
