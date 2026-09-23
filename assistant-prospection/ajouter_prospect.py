"""
Assistant de saisie prospects UNSEEN.

Vous repérez un profil (Instagram ou LinkedIn) et récupérez vous-même le
pseudo et l'email à la main. Ce script prend le relais :
1. Il vérifie que ce prospect n'est pas déjà dans le tableau.
2. Il ajoute une ligne au tableau Excel (dossier iCloud).
3. Il crée un brouillon Gmail personnalisé, prêt à relire et envoyer.

Deux façons de s'en servir :

    python3 ajouter_prospect.py
        Un seul contact, en répondant aux questions posées dans le Terminal.

    python3 ajouter_prospect.py --fichier a_traiter.xlsx
        Plusieurs contacts d'un coup, à partir d'un tableau Excel (colonnes
        Type, Pseudo, Plateforme, Email, Prénom, Langue). Un brouillon est
        créé pour chaque ligne, sans repasser par le Terminal à chaque fois.
        Un modèle vide est fourni dans a_traiter.xlsx.
"""

import argparse
import os
import sys

from openpyxl import load_workbook

import excel
import gmail

DOSSIER_SCRIPT = os.path.dirname(os.path.abspath(__file__))
MODELES = {
    "client": {
        "EN": os.path.join(DOSSIER_SCRIPT, "modele_en.txt"),
        "FR": os.path.join(DOSSIER_SCRIPT, "modele_fr.txt"),
        "ZH": os.path.join(DOSSIER_SCRIPT, "modele_zh.txt"),
    },
    "partenaire": {
        "EN": os.path.join(DOSSIER_SCRIPT, "modele_partenariat_en.txt"),
        "FR": os.path.join(DOSSIER_SCRIPT, "modele_partenariat_fr.txt"),
        "ZH": os.path.join(DOSSIER_SCRIPT, "modele_partenariat_zh.txt"),
    },
    "agence": {
        "EN": os.path.join(DOSSIER_SCRIPT, "modele_agence_en.txt"),
        "FR": os.path.join(DOSSIER_SCRIPT, "modele_agence_fr.txt"),
    },
}

# Texte écrit dans la colonne Statut du CRM pour chaque type de contact.
STATUT_BROUILLON = {
    "client": "brouillon créé",
    "partenaire": "brouillon partenariat créé",
    "agence": "brouillon agence créé",
}

# Ce qui remplace [Prénom] quand il n'est pas connu, selon la langue.
PRENOM_PAR_DEFAUT = {"EN": "Team", "FR": "toute l'équipe", "ZH": "您"}


def demander(question, obligatoire=True):
    """Pose une question dans le Terminal et renvoie la réponse tapée."""
    while True:
        reponse = input(question).strip()
        if reponse or not obligatoire:
            return reponse
        print("   (réponse obligatoire, réessayez)")


def demander_type_contact():
    """Demande si c'est un client, un partenaire potentiel ou une agence."""
    while True:
        reponse = input("Type de contact (client/partenaire/agence) : ").strip().lower()
        if reponse in MODELES:
            return reponse
        print("   Tapez client, partenaire ou agence.")


def demander_langue(type_contact):
    """Demande EN, FR ou ZH, en insistant tant que la réponse n'est pas valide."""
    while True:
        reponse = input("Langue du message (EN/FR/ZH) : ").strip().upper()
        if reponse in MODELES[type_contact]:
            if reponse == "ZH":
                print("   ⚠️  Contenu en chinois : fais-le relire par un locuteur natif")
                print("      avant d'envoyer ce brouillon (règle du projet).")
            return reponse
        print("   Tapez EN, FR ou ZH.")


def charger_modele(type_contact, langue, prenom):
    """Lit le fichier modèle correspondant et remplace [Prénom]."""
    with open(MODELES[type_contact][langue], "r", encoding="utf-8") as fichier:
        texte = fichier.read()

    nom_a_utiliser = prenom if prenom else PRENOM_PAR_DEFAUT[langue]
    return texte.replace("[Prénom]", nom_a_utiliser)


def traiter_prospect(type_contact, pseudo, plateforme, email, prenom, langue):
    """Crée le brouillon Gmail et la ligne CRM pour un contact. Renvoie True si fait."""
    corps_message = charger_modele(type_contact, langue, prenom)
    gmail.creer_brouillon(email, corps_message, langue, type_contact)

    excel.ajouter_ligne(pseudo, plateforme, prenom, email, statut=STATUT_BROUILLON[type_contact])
    return True


def mode_un_seul():
    """Ajoute un seul contact, en posant les questions dans le Terminal."""
    print("=== Assistant de saisie prospects UNSEEN. ===\n")

    type_contact = demander_type_contact()
    pseudo = demander("Pseudo ou lien du profil : ")
    plateforme = demander("Plateforme (Instagram/LinkedIn) : ")
    email = demander("Email : ")
    prenom = demander("Prénom (laisser vide si inconnu) : ", obligatoire=False)
    langue = demander_langue(type_contact)

    if excel.trouver_doublon(pseudo, email):
        print("\n⚠️  Ce pseudo ou cet email est déjà dans le tableau.")
        continuer = demander("Ajouter quand même ? (oui/non) : ").strip().lower()
        if continuer != "oui":
            print("Annulé, rien n'a été ajouté.")
            sys.exit(0)

    print("\nConnexion à Gmail...")
    traiter_prospect(type_contact, pseudo, plateforme, email, prenom, langue)
    print("✅ Brouillon créé dans Gmail.")
    print(f"✅ Ligne ajoutée dans {excel.CHEMIN_EXCEL}")
    print("\nTerminé. Relisez le brouillon dans Gmail avant de l'envoyer.")


def mode_lot(chemin_fichier):
    """Traite plusieurs contacts d'un coup depuis un fichier Excel."""
    if not os.path.exists(chemin_fichier):
        print(f"❌ Fichier introuvable : {chemin_fichier}")
        sys.exit(1)

    classeur = load_workbook(chemin_fichier)
    feuille = classeur.active

    crees, ignores, erreurs = 0, 0, 0

    for numero_ligne, ligne in enumerate(feuille.iter_rows(min_row=2, values_only=True), start=2):
        if not ligne or not any(ligne):
            continue

        ligne = list(ligne) + [""] * (6 - len(ligne))
        type_contact, pseudo, plateforme, email, prenom, langue = ligne[:6]

        type_contact = str(type_contact or "").strip().lower()
        pseudo = str(pseudo or "").strip()
        plateforme = str(plateforme or "").strip()
        email = str(email or "").strip()
        prenom = str(prenom or "").strip()
        langue = str(langue or "").strip().upper()

        if type_contact not in MODELES:
            print(f"⚠️  Ligne {numero_ligne} : type de contact invalide ({type_contact!r}), ignorée.")
            erreurs += 1
            continue
        if not email or langue not in MODELES[type_contact]:
            print(f"⚠️  Ligne {numero_ligne} : email ou langue manquant/invalide, ignorée.")
            erreurs += 1
            continue

        if excel.trouver_doublon(pseudo, email):
            print(f"⏭️  Ligne {numero_ligne} : {email} déjà dans le tableau, ignorée.")
            ignores += 1
            continue

        traiter_prospect(type_contact, pseudo, plateforme, email, prenom, langue)
        print(f"✅ Ligne {numero_ligne} : brouillon créé pour {email} ({langue}).")
        crees += 1

    print(f"\nTerminé : {crees} brouillon(s) créé(s), {ignores} doublon(s) ignoré(s), "
          f"{erreurs} ligne(s) invalide(s).")
    print("Relisez chaque brouillon dans Gmail avant d'envoyer — en particulier les ZH,")
    print("à faire relire par un locuteur natif.")


if __name__ == "__main__":
    analyseur = argparse.ArgumentParser(description="Assistant de saisie prospects UNSEEN.")
    analyseur.add_argument("--fichier", help="Traiter plusieurs contacts d'un coup depuis ce fichier Excel")
    arguments = analyseur.parse_args()

    if arguments.fichier:
        mode_lot(arguments.fichier)
    else:
        mode_un_seul()
