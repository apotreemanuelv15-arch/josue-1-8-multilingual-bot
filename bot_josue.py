import os
import requests

def executer_mission():
    api_key = os.environ["BOT_GEMINI_KEY"]
    
    # On teste la version v1 (stable) qui semble être la seule qui réponde chez vous
    url = f"https://generativelanguage.googleapis.com/v1/models?key={api_key}"
    
    print("📡 Interrogatoire des serveurs Google (Version Stable v1)...")

    try:
        response = requests.get(url, timeout=30)
        result = response.json()
        
        if response.status_code != 200:
            print(f"❌ Erreur Serveur: {result}")
            return

        print("--- LISTE DES MODÈLES AUTORISÉS POUR VOTRE CLÉ ---")
        models = result.get('models', [])
        for m in models:
            # On affiche le nom exact et les capacités
            name = m.get('name')
            methods = m.get('supportedMethods', [])
            print(f"▶️ Modèle: {name} | Capacités: {methods}")
        print("-------------------------------------------------")
        
        if not models:
            print("⚠️ Aucun modèle n'est rattaché à cette clé. La clé est peut-être restreinte.")

    except Exception as e:
        print(f"❌ Erreur de connexion : {str(e)}")

if __name__ == "__main__":
    executer_mission()
