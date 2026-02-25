import requests
from twilio.rest import Client

def executer_mission():
    api_key = os.environ.get("BOT_GEMINI_KEY")
    twilio_sid = os.environ.get("TWILIO_SID")
    twilio_token = os.environ.get("TWILIO_TOKEN")
    twilio_number = os.environ.get("TWILIO_NUMBER")
    target_number = os.environ.get("TARGET_NUMBER")
    
    # Utilisation du nom exact détecté par le scan
    modele = "gemini-2.5-flash"
    url = f"https://generativelanguage.googleapis.com/v1/models/{modele}:generateContent?key={api_key}"
    
    prompt = "Tu es l'Aumônier Josué 1:8. Génère un message de motivation biblique en FR, EN, et PT. Structure : 📖 VERSET, 🛡️ MÉDITATION, 💡 CONSEIL."
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {'Content-Type': 'application/json'}

    print(f"🚀 Lancement de la mission avec la génération 2.5 : {modele}...")

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            message_ia = response.json()['candidates'][0]['content']['parts'][0]['text']
            print("✨ SUCCÈS TOTAL : Liaison 2.5 établie.")
            
            client = Client(twilio_sid, twilio_token)
            client.messages.create(body=message_ia, from_=twilio_number, to=target_number)
            print("🏁 MESSAGE ENVOYÉ SUR WHATSAPP !")
        else:
            print(f"❌ Échec de la mission : {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur critique : {str(e)}")

if __name__ == "__main__":
    executer_mission()
