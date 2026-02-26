import os
import requests
from twilio.rest import Client

def executer_mission():
    api_key = os.environ.get("BOT_GEMINI_KEY")
    twilio_sid = os.environ.get("TWILIO_SID")
    twilio_token = os.environ.get("TWILIO_TOKEN")
    twilio_number = os.environ.get("TWILIO_NUMBER")
    target_number = os.environ.get("TARGET_NUMBER")
    
    # ON UTILISE LE MODÈLE QUE VOTRE SCAN (RUN 47) A CONFIRMÉ
    # On passe par la v1beta car c'est la plus flexible pour AI Studio
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{"text": "Message court Josué 1:8 en FR, EN, PT."}]
        }]
    }

    print("🎯 Offensive sur Gemini 2.0 Flash (Confirmé par votre scan)...")

    try:
        response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'}, timeout=30)
        
        if response.status_code == 200:
            message_ia = response.json()['candidates'][0]['content']['parts'][0]['text']
            print("✨ RÉUSSITE ! Réponse reçue de l'IA.")
            
            client = Client(twilio_sid, twilio_token)
            client.messages.create(body=message_ia, from_=twilio_number, to=target_number)
            print("🏁 TERMINÉ : Message envoyé sur WhatsApp !")
        else:
            # Si le 2.0 flash échoue, on tente le 'gemini-2.0-flash-lite' (aussi dans votre liste)
            print(f"⚠️ 2.0 Flash a échoué ({response.status_code}), repli sur 2.0 Flash Lite...")
            url_lite = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent?key={api_key}"
            response_lite = requests.post(url_lite, json=payload, headers={'Content-Type': 'application/json'})
            
            if response_lite.status_code == 200:
                message_ia = response_lite.json()['candidates'][0]['content']['parts'][0]['text']
                client = Client(twilio_sid, twilio_token)
                client.messages.create(body=message_ia, from_=twilio_number, to=target_number)
                print("🏁 TERMINÉ (via Lite) : Message envoyé !")
            else:
                print(f"❌ Erreur persistante : {response_lite.text}")
            
    except Exception as e:
        print(f"⚠️ Incident : {str(e)}")

if __name__ == "__main__":
    executer_mission()
