"""
Envoi de messages Telegram — fonctions partagées par tous les outils du Radar UNSEEN.

Ce fichier ne se lance pas tout seul : il est utilisé par veille_presse.py
(et plus tard par le radar des événements).
"""

import html
import os
import sys
import time

import requests
from dotenv import load_dotenv

DOSSIER_SCRIPT = os.path.dirname(os.path.abspath(__file__))
CHEMIN_ENV = os.path.join(DOSSIER_SCRIPT, ".env")

# Telegram refuse les messages de plus de 4096 caractères.
# On garde une marge de sécurité.
TAILLE_MAX_MESSAGE = 3800


def lire_identifiants():
    """Récupère le token et le chat_id depuis le fichier .env."""
    load_dotenv(CHEMIN_ENV)
    token = os.getenv("TELEGRAM_TOKEN", "").strip()
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "").strip()

    if not token or not chat_id:
        print("❌ TELEGRAM_TOKEN ou TELEGRAM_CHAT_ID est vide dans le fichier .env.")
        print("   Lance d'abord : python connexion_telegram.py")
        sys.exit(1)

    return token, chat_id


def proteger(texte):
    """
    Rend un texte sans danger pour Telegram.

    Telegram interprète les signes < > & comme de la mise en forme.
    Un titre d'article qui contient « Dior & Co » casserait l'envoi,
    donc on remplace ces signes par leur version protégée.
    """
    return html.escape(str(texte), quote=False)


def lien_cliquable(url, texte_affiche):
    """Fabrique un titre cliquable qui ouvre l'article."""
    return f'<a href="{html.escape(str(url), quote=True)}">{proteger(texte_affiche)}</a>'


def decouper(texte):
    """
    Coupe un message trop long en plusieurs morceaux.

    On coupe toujours entre deux lignes, jamais au milieu d'une phrase.
    """
    lignes = texte.split("\n")
    morceaux = []
    courant = ""

    for ligne in lignes:
        if len(courant) + len(ligne) + 1 > TAILLE_MAX_MESSAGE and courant:
            morceaux.append(courant.rstrip())
            courant = ""
        courant += ligne + "\n"

    if courant.strip():
        morceaux.append(courant.rstrip())

    return morceaux


def envoyer(texte):
    """
    Envoie un message sur Telegram.

    Réessaie jusqu'à 3 fois : l'API Telegram met parfois quelques secondes
    à répondre depuis une connexion domestique.
    Renvoie True si tout est parti, False sinon.
    """
    token, chat_id = lire_identifiants()
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    tout_ok = True

    for morceau in decouper(texte):
        payload = {
            "chat_id": chat_id,
            "text": morceau,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        }

        envoye = False
        for tentative in range(1, 4):
            try:
                reponse = requests.post(url, data=payload, timeout=20)
                donnees = reponse.json()
                if donnees.get("ok"):
                    envoye = True
                    break
                print(f"⚠️  Telegram a refusé le message : {donnees.get('description')}")
                break
            except requests.exceptions.RequestException as erreur:
                print(f"⚠️  Tentative {tentative}/3 échouée ({type(erreur).__name__}).")
                if tentative < 3:
                    time.sleep(3)

        if not envoye:
            tout_ok = False
        else:
            # Petite pause entre deux messages : Telegram limite le débit.
            time.sleep(1)

    return tout_ok
