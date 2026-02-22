import os
import requests
from twilio.rest import Client

def executer_mission():
    api_key = os.environ.get("BOT_GEMINI_KEY")
    twilio_sid = os.environ.get("TWILIO_SID")
    twilio_token = os.environ.get("TWILIO_TOKEN")
    twilio_number = os.environ.get("TWILIO_NUMBER")
    target_number = os.environ.get("TARGET_NUMBER")
    
    # FORMAT ABSOLU REQUIS POUR LA v1beta SELON VOS LOGS CLOUD
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{"text": "Tu es l'Aumônier Josué 1:8. Donne un message de force en FR, EN et PT avec un verset."}]
        }]
    }
    
    headers = {'Content-Type': 'application/json'}

    print("🚀 Offensive finale : Déblocage du flux GenerativeService...")

    try:
        # Tentative principale
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        print(f"📡 Status Code : {response.status_code}")
        
        if response.status_code == 200:
            message_ia = response.json()['candidates'][0]['content']['parts'][0]['text']
            print("✨ INCROYABLE : La barrière est tombée !")
            
            client = Client(twilio_sid, twilio_token)
            client.messages.create(body=message_ia, from_=twilio_number, to=target_number)
            print("🏁 MISSION RÉUSSIE : WhatsApp envoyé !")
            
        else:
            # Si ça échoue encore, on tente le format v1 (le graphique montrait aussi des erreurs v1)
            print("⚠️ Échec v1beta, repli sur v1...")
            url_v1 = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
            response_v1 = requests.post(url_v1, json=payload, headers=headers)
            
            if response_v1.status_code == 200:
                print("✨ SAUVETAGE RÉUSSI via v1 !")
                message_ia = response_v1.json()['candidates'][0]['content']['parts'][0]['text']
                client = Client(twilio_sid, twilio_token)
                client.messages.create(body=message_ia, from_=twilio_number, to=target_number)
            else:
                print(f"❌ Mur infranchissable : {response_v1.text}")

    except Exception as e:
        print(f"❌ Erreur système : {str(e)}")

if __name__ == "__main__":
    executer_mission()
