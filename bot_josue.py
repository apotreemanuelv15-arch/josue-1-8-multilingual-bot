import os
from google import genai
from twilio.rest import Client

# Connexion
client = genai.Client(api_key=os.environ["BOT_GEMINI_KEY"])
twilio_client = Client(os.environ["TWILIO_SID"], os.environ["TWILIO_TOKEN"])

def executer_mission():
    try:
        print("🔍 Scan des modèles disponibles pour cette clé...")
        
        # On cherche un modèle flash dans la liste officielle de VOTRE clé
        model_name = None
        for m in client.models.list():
            if 'generateContent' in m.supported_methods and 'flash' in m.name:
                model_name = m.name
                break
        
        if not model_name:
            model_name = "gemini-1.5-flash" # Repli par défaut
            
        print(f"🎯 Modèle détecté et sélectionné : {model_name}")
        
        response = client.models.generate_content(
            model=model_name,
            contents="Génère un message biblique court en FR, PT, EN pour le QG Josué 1:8."
        )
        
        # Envoi Twilio
        twilio_client.messages.create(
            from_=os.environ["TWILIO_NUMBER"],
            body=response.text,
            to=os.environ["TARGET_NUMBER"]
        )
        
        print("✅ VICTOIRE ! La liaison est enfin établie.")
        
    except Exception as e:
        print(f"❌ Rapport d'échec : {str(e)}")

if __name__ == "__main__":
    executer_mission()
