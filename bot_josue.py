import os
import requests

def scan_reel():
    api_key = os.environ.get("BOT_GEMINI_KEY")
    
    # On interroge les deux versions possibles pour lister les modèles
    versions = ["v1", "v1beta"]
    
    print("🔍 SCAN DE RECONNAISSANCE DES MODÈLES...")
    
    for v in versions:
        url = f"https://generativelanguage.googleapis.com/{v}/models?key={api_key}"
        print(f"📡 Interrogation de la version {v}...")
        try:
            res = requests.get(url, timeout=15)
            if res.status_code == 200:
                modeles = res.json().get('models', [])
                print(f"✅ Version {v} a répondu ! {len(modeles)} modèles trouvés.")
                for m in modeles:
                    print(f"   -> NOM À UTILISER : {m['name']}")
            else:
                print(f"❌ Version {v} refuse : {res.status_code}")
        except Exception as e:
            print(f"⚠️ Erreur sur {v} : {str(e)}")

if __name__ == "__main__":
    scan_reel()
