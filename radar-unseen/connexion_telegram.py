"""
Script de connexion du Radar UNSEEN. à Telegram.

Ce script :
1. Lit le token du bot dans le fichier .env.
2. Va chercher le chat_id de Jay (à partir du message "bonjour" déjà
   envoyé au bot).
3. Écrit ce chat_id dans le fichier .env.
4. Envoie un message de confirmation sur Telegram.

À lancer avec : python3 connexion_telegram.py
"""

import os
import re
import sys

import requests
from dotenv import load_dotenv

# Chemin du fichier .env, toujours à côté de ce script
DOSSIER_SCRIPT = os.path.dirname(os.path.abspath(__file__))
CHEMIN_ENV = os.path.join(DOSSIER_SCRIPT, ".env")


def lire_token():
    """Charge le token Telegram depuis le fichier .env."""
    load_dotenv(CHEMIN_ENV)
    token = os.getenv("TELEGRAM_TOKEN", "").strip()

    if not token:
        print("❌ Le token Telegram est vide.")
        print(f"   Ouvre le fichier {CHEMIN_ENV} et colle ton token")
        print("   sur la ligne TELEGRAM_TOKEN=, puis relance ce script.")
        sys.exit(1)

    return token


def recuperer_chat_id(token):
    """Trouve le chat_id à partir du dernier message envoyé au bot."""
    url = f"https://api.telegram.org/bot{token}/getUpdates"

    try:
        reponse = requests.get(url, timeout=10)
    except requests.exceptions.RequestException as erreur:
        print("❌ Impossible de contacter Telegram.")
        print(f"   Détail : {erreur}")
        sys.exit(1)

    donnees = reponse.json()

    if not donnees.get("ok"):
        print("❌ Telegram a refusé la demande. Le token est peut-être incorrect.")
        print(f"   Réponse de Telegram : {donnees}")
        sys.exit(1)

    resultats = donnees.get("result", [])

    if not resultats:
        print("❌ Aucun message reçu par le bot pour l'instant.")
        print("   Ouvre Telegram, envoie à nouveau \"bonjour\" à ton bot,")
        print("   puis relance ce script.")
        sys.exit(1)

    # On prend le chat_id du tout dernier message reçu
    dernier_message = resultats[-1]
    chat_id = dernier_message["message"]["chat"]["id"]

    return str(chat_id)


def enregistrer_chat_id(chat_id):
    """Écrit le chat_id trouvé dans le fichier .env."""
    with open(CHEMIN_ENV, "r", encoding="utf-8") as fichier:
        contenu = fichier.read()

    nouveau_contenu = re.sub(
        r"^TELEGRAM_CHAT_ID=.*$",
        f"TELEGRAM_CHAT_ID={chat_id}",
        contenu,
        flags=re.MULTILINE,
    )

    with open(CHEMIN_ENV, "w", encoding="utf-8") as fichier:
        fichier.write(nouveau_contenu)

    print(f"✅ chat_id ({chat_id}) enregistré dans {CHEMIN_ENV}")


def envoyer_message(token, chat_id, texte):
    """Envoie un message Telegram au chat_id donné."""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": texte}

    try:
        reponse = requests.post(url, data=payload, timeout=10)
    except requests.exceptions.RequestException as erreur:
        print("❌ Impossible d'envoyer le message sur Telegram.")
        print(f"   Détail : {erreur}")
        sys.exit(1)

    donnees = reponse.json()

    if not donnees.get("ok"):
        print("❌ Telegram a refusé l'envoi du message.")
        print(f"   Réponse de Telegram : {donnees}")
        sys.exit(1)

    print("✅ Message envoyé sur Telegram avec succès !")


if __name__ == "__main__":
    print("Connexion au Radar UNSEEN. en cours...")

    token = lire_token()
    chat_id = recuperer_chat_id(token)
    enregistrer_chat_id(chat_id)
    envoyer_message(token, chat_id, "Bonjour Jay, le Radar UNSEEN. est connecté.")

    print("Terminé. Regarde Telegram, tu devrais avoir reçu le message.")
