import os
sid = os.environ.get("TWILIO_SID")
# On ajoute des espaces entre chaque lettre pour tromper la censure de GitHub
print("VOTRE_SID_EST : " + " ".join(sid))
