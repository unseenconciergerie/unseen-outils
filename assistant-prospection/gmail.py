"""
Création de brouillons Gmail (assistant-prospection).

On se connecte à Gmail en IMAP avec un mot de passe d'application (voir
README.md pour l'obtenir), et on dépose directement le message dans le
dossier "Brouillons" de Gmail. Rien à installer : imaplib fait partie de
Python.

La signature (signature.html + logo_signature.png) est une copie exacte
de la vraie signature Gmail de Jay, récupérée une fois pour toutes. Elle
est ajoutée automatiquement à chaque brouillon, avec la bonne mise en
forme — plus besoin de cliquer sur "insérer la signature".
"""

import imaplib
import os
import sys
import time
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

DOSSIER_SCRIPT = os.path.dirname(os.path.abspath(__file__))
CHEMIN_ENV = os.path.join(DOSSIER_SCRIPT, ".env")
CHEMIN_SIGNATURE = os.path.join(DOSSIER_SCRIPT, "signature.html")
CHEMIN_LOGO = os.path.join(DOSSIER_SCRIPT, "logo_signature.png")

OBJETS_MAIL = {
    "client": "Europe by UNSEEN.",
    "partenaire": "Partenariat UNSEEN. — Paris",
    "agence": "Paris, by UNSEEN.",
}

EXPEDITEURS = {
    "EN": "contact@unseenconciergerie.com",
    "FR": "contact@unseenconciergerie.fr",
    "ZH": "contact@unseenconciergerie.com",
}

DOSSIER_BROUILLONS_GMAIL = "[Gmail]/Brouillons"


def mettre_en_forme_html(texte):
    """Transforme le texte brut du modèle en HTML avec paragraphes espacés,
    pour que Gmail affiche l'email normalement (comme un email rédigé à la
    main) plutôt que comme un bloc de texte brut.

    Les fichiers modele_*.txt contiennent des retours à la ligne internes
    juste pour rester lisibles dans un éditeur de texte : on les remplace
    par un espace pour que le paragraphe s'étale naturellement en HTML,
    au lieu de forcer une colonne étroite avec un <br> au milieu d'une
    phrase."""
    paragraphes = texte.strip().split("\n\n")
    paragraphes_html = [
        "<p>" + " ".join(ligne.strip() for ligne in paragraphe.splitlines()) + "</p>"
        for paragraphe in paragraphes
    ]

    with open(CHEMIN_SIGNATURE, "r", encoding="utf-8") as fichier:
        signature = fichier.read()

    return "<div>" + "".join(paragraphes_html) + "<br><br>" + signature + "</div>"


def lire_identifiants():
    """Charge l'adresse Gmail et le mot de passe d'application depuis .env."""
    load_dotenv(CHEMIN_ENV)
    adresse = os.getenv("GMAIL_ADRESSE", "").strip()
    mot_de_passe = os.getenv("GMAIL_MOT_DE_PASSE_APPLICATION", "").strip()

    if not adresse or not mot_de_passe:
        print("❌ GMAIL_ADRESSE ou GMAIL_MOT_DE_PASSE_APPLICATION est vide.")
        print(f"   Ouvre le fichier {CHEMIN_ENV} et complète ces deux lignes.")
        sys.exit(1)

    return adresse, mot_de_passe


def creer_brouillon(destinataire, corps_message, langue, type_contact="client"):
    """Se connecte à Gmail et dépose un brouillon dans le dossier Brouillons."""
    adresse, mot_de_passe = lire_identifiants()
    expediteur = EXPEDITEURS[langue]

    corps_html = mettre_en_forme_html(corps_message)

    message = MIMEMultipart("related")
    message["From"] = expediteur
    message["To"] = destinataire
    message["Subject"] = OBJETS_MAIL[type_contact]
    message.attach(MIMEText(corps_html, "html"))

    with open(CHEMIN_LOGO, "rb") as fichier_logo:
        logo = MIMEImage(fichier_logo.read())
    logo.add_header("Content-ID", "<logo_unseen>")
    logo.add_header("Content-Disposition", "inline", filename="logo_signature.png")
    message.attach(logo)

    try:
        connexion = imaplib.IMAP4_SSL("imap.gmail.com")
        connexion.login(adresse, mot_de_passe)
    except imaplib.IMAP4.error as erreur:
        print("❌ Connexion à Gmail refusée.")
        print(f"   Détail : {erreur}")
        print("   Vérifie l'adresse et le mot de passe d'application dans .env.")
        sys.exit(1)

    statut, reponse = connexion.append(
        DOSSIER_BROUILLONS_GMAIL,
        "\\Draft",
        imaplib.Time2Internaldate(time.time()),
        message.as_bytes(),
    )
    connexion.logout()

    if statut != "OK":
        print("❌ Gmail a refusé la création du brouillon.")
        print(f"   Détail : {reponse}")
        sys.exit(1)
