"""
Assistant de saisie prospects UNSEEN.

Vous repérez un profil (Instagram ou LinkedIn) et récupérez vous-même le
pseudo et l'email à la main. Ce script prend le relais :
1. Il vérifie que ce prospect n'est pas déjà dans le tableau.
2. Il ajoute une ligne au tableau Excel (dossier iCloud).
3. Il crée un brouillon Gmail personnalisé, prêt à relire et envoyer.

À lancer avec : python3 ajouter_prospect.py
"""

import os
import sys

import excel
import gmail

DOSSIER_SCRIPT = os.path.dirname(os.path.abspath(__file__))
MODELES = {
    "EN": os.path.join(DOSSIER_SCRIPT, "modele_en.txt"),
    "FR": os.path.join(DOSSIER_SCRIPT, "modele_fr.txt"),
}


def demander(question, obligatoire=True):
    """Pose une question dans le Terminal et renvoie la réponse tapée."""
    while True:
        reponse = input(question).strip()
        if reponse or not obligatoire:
            return reponse
        print("   (réponse obligatoire, réessayez)")


def demander_langue():
    """Demande EN ou FR, en insistant tant que la réponse n'est pas valide."""
    while True:
        reponse = input("Langue du message (EN/FR) : ").strip().upper()
        if reponse in MODELES:
            return reponse
        print("   Tapez EN ou FR.")


def charger_modele(langue, prenom):
    """Lit le fichier modèle correspondant et remplace [Prénom]."""
    with open(MODELES[langue], "r", encoding="utf-8") as fichier:
        texte = fichier.read()

    nom_a_utiliser = prenom if prenom else "there" if langue == "EN" else "vous"
    return texte.replace("[Prénom]", nom_a_utiliser)


if __name__ == "__main__":
    print("=== Assistant de saisie prospects UNSEEN. ===\n")

    pseudo = demander("Pseudo ou lien du profil : ")
    plateforme = demander("Plateforme (Instagram/LinkedIn) : ")
    email = demander("Email : ")
    prenom = demander("Prénom (laisser vide si inconnu) : ", obligatoire=False)
    langue = demander_langue()

    if excel.trouver_doublon(pseudo, email):
        print("\n⚠️  Ce pseudo ou cet email est déjà dans le tableau.")
        continuer = demander("Ajouter quand même ? (oui/non) : ").strip().lower()
        if continuer != "oui":
            print("Annulé, rien n'a été ajouté.")
            sys.exit(0)

    print("\nConnexion à Gmail...")
    corps_message = charger_modele(langue, prenom)
    gmail.creer_brouillon(email, corps_message, langue)
    print("✅ Brouillon créé dans Gmail.")

    excel.ajouter_ligne(pseudo, plateforme, prenom, email, statut="brouillon créé")
    print(f"✅ Ligne ajoutée dans {excel.CHEMIN_EXCEL}")

    print("\nTerminé. Relisez le brouillon dans Gmail avant de l'envoyer.")
