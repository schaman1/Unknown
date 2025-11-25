from pyngrok import ngrok
from dotenv import load_dotenv
import os

# Charger le fichier .env
load_dotenv(dotenv_path="../secret.env")  # par défaut cherche un fichier nommé ".env" dans le même dossier

# Récupérer la variable
token = os.getenv("AUTH_KEY")

ngrok.set_auth_token(token)