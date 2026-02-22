import os
import requests
from twilio.rest import Client

def executer_mission():
    api_key = os.environ.get("BOT_GEMINI_KEY")
    twilio_sid = os.environ.get("TWILIO_SID")
    twilio_token = os.environ.get("TWILIO_TOKEN")
    twilio_number = os.environ.get("TWILIO_NUMBER")
    target_number = os.environ.get("TARGET_NUMBER")

    print("🔍 Scan des modèles disponibles pour votre nouvelle clé...")
    
    # 1. On liste les modèles disponibles
    list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    
    try:
        res = requests.get(list_url)
        models_data = res.json()
        
        if 'models' not in models_data:
            print(f"❌ Impossible de lister les modèles : {models_data}")
            return

        # On cherche un modèle qui contient "gemini" et qui supporte "generateContent"
        modeles_trouves = [
            m['name'] for m in models_data['models'] 
            if 'generateContent' in m.get('supportedMethods', [])
        ]
        
        if not modeles_trouves:
            print("❌ Aucun modèle compatible trouvé pour cette clé.")
            return

        print(f"✅ Modèles détectés : {modeles_trouves}")
        
        # 2. On tente de générer avec le premier modèle de la liste
        choix = modeles_trouves[0]
        print(f"🚀 Tentative de génération avec le modèle détecté : {choix}")
        
        prompt = "Tu es l'Aumônier du QG Josué 1:8. Génère un message de motivation biblique puissant en 3 langues : Français (FR), Portugais (PT), et Anglais (EN)."
        gen_url = f"https://generativelanguage.googleapis.com/v1beta/{choix}:generateContent?key={api_key}"
        
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        response = requests.post(gen_url, json=payload, headers={'Content-Type': 'application/json'})
        result = response.json()

        if response.status_code == 200:
            message_ia = result['candidates'][0]['content']['parts'][0]['text']
            print(f"✨ SUCCÈS ! Message généré par {choix}.")
            
            # 3. Envoi Twilio
            client = Client(twilio_sid, twilio_token)
            client.messages.create(body=message_ia, from_=twilio_number, to=target_number)
            print("🏁 MISSION RÉUSSIE : Message envoyé !")
        else:
            print(f"❌ Échec génération avec {choix} : {result}")

    except Exception as e:
        print(f"⚠️ Erreur système : {str(e)}")

if __name__ == "__main__":
    executer_mission()
