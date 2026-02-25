import os
import requests
from twilio.rest import Client

def executer_mission():
    api_key = os.environ.get("BOT_GEMINI_KEY")
    twilio_sid = os.environ.get("TWILIO_SID")
    twilio_token = os.environ.get("TWILIO_TOKEN")
    twilio_number = os.environ.get("TWILIO_NUMBER")
    target_number = os.environ.get("TARGET_NUMBER")
    
    # On tente le modèle 2.0 Flash qui était dans votre liste
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{"parts": [{"text": "Donne un verset de Josué 1:8 et une courte méditation en FR, EN, PT."}]}]
    }

    print("🛰️ Envoi de la requête à Google...")

    try:
        response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
        print(f"📡 Status de la réponse : {response.status_code}")
        
        data = response.json()
        
        if response.status_code == 200:
            message_ia = data['candidates'][0]['content']['parts'][0]['text']
            print("✅ Message généré ! Tentative d'envoi WhatsApp...")
            
            client = Client(twilio_sid, twilio_token)
            client.messages.create(body=message_ia, from_=twilio_number, to=target_number)
            print("🏁 TERMINÉ : Regardez votre téléphone !")
        else:
            print(f"❌ Échec Google : {data}")
            
    except Exception as e:
        print(f"⚠️ Erreur système détaillée : {str(e)}")

if __name__ == "__main__":
    executer_mission()
