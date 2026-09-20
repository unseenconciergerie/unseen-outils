"""
Radar UNSEEN. — Calendrier des événements.

Lit les événements listés dans evenements.xlsx et envoie des rappels
Telegram à J-90, J-60, J-30 et J-7 avant chaque événement, plus un
récapitulatif groupé sur demande.

Trois façons de le lancer :
    python radar_evenements.py --test     -> affiche le résultat, n'envoie rien
    python radar_evenements.py            -> envoie les rappels du jour
    python radar_evenements.py --resume   -> envoie le récapitulatif des événements à venir

Le détail est expliqué dans le README.md.
"""

import argparse
import json
import os
import sys
from datetime import date, datetime

from openpyxl import load_workbook

import envoi_telegram

DOSSIER_SCRIPT = os.path.dirname(os.path.abspath(__file__))
FICHIER_EVENEMENTS = os.path.join(DOSSIER_SCRIPT, "evenements.xlsx")
FICHIER_MEMOIRE = os.path.join(DOSSIER_SCRIPT, "memoire_evenements.json")

JALONS = [90, 60, 30, 7]


def convertir_date(valeur):
    """Accepte une date Excel ou un texte JJ/MM/AAAA."""
    if isinstance(valeur, datetime):
        return valeur.date()
    if isinstance(valeur, date):
        return valeur
    if isinstance(valeur, str) and valeur.strip():
        try:
            return datetime.strptime(valeur.strip(), "%d/%m/%Y").date()
        except ValueError:
            return None
    return None


def lire_evenements():
    """Lit evenements.xlsx et renvoie la liste des événements actifs et valides."""
    if not os.path.exists(FICHIER_EVENEMENTS):
        print(f"❌ {FICHIER_EVENEMENTS} est introuvable.")
        sys.exit(1)

    classeur = load_workbook(FICHIER_EVENEMENTS)
    feuille = classeur.active

    evenements = []
    for numero_ligne, ligne in enumerate(feuille.iter_rows(min_row=2, values_only=True), start=2):
        if not ligne or not ligne[0]:
            continue

        nom, date_brute, ville, categorie, actif = ligne

        if str(actif).strip().lower() != "oui":
            continue

        date_evenement = convertir_date(date_brute)
        if date_evenement is None:
            print(f"⚠️  Ligne {numero_ligne} : date illisible pour « {nom} » ({date_brute!r}), ignorée.")
            continue

        evenements.append(
            {
                "nom": str(nom).strip(),
                "date": date_evenement,
                "ville": str(ville).strip() if ville else "",
                "categorie": str(categorie).strip() if categorie else "",
            }
        )

    return evenements


def charger_memoire():
    """Charge memoire_evenements.json (ce qui a déjà été envoyé aujourd'hui)."""
    if not os.path.exists(FICHIER_MEMOIRE):
        return {}
    try:
        with open(FICHIER_MEMOIRE, "r", encoding="utf-8") as fichier:
            return json.load(fichier)
    except (json.JSONDecodeError, OSError):
        print("⚠️  memoire_evenements.json illisible : on repart d'une mémoire vide.")
        return {}


def sauver_memoire(memoire):
    """Enregistre la mémoire, en oubliant ce qui date de plus d'un an."""
    limite = date.today().replace(year=date.today().year - 1).isoformat()
    memoire = {cle: jour for cle, jour in memoire.items() if jour >= limite}

    with open(FICHIER_MEMOIRE, "w", encoding="utf-8") as fichier:
        json.dump(memoire, fichier, ensure_ascii=False, indent=1)


def formater_rappel(evenement, jours_restants):
    lieu = f" ({evenement['ville']})" if evenement["ville"] else ""
    return (
        f"📅 J-{jours_restants} : {envoi_telegram.proteger(evenement['nom'])}{lieu}\n"
        f"   {evenement['date'].strftime('%d/%m/%Y')}"
    )


def lancer_rappels(evenements, mode_test):
    """Envoie les rappels pour les événements pile à J-90/60/30/7 aujourd'hui."""
    aujourdhui = date.today()
    memoire = charger_memoire()
    rappels_envoyes = 0

    for evenement in evenements:
        jours_restants = (evenement["date"] - aujourdhui).days
        if jours_restants not in JALONS:
            continue

        cle = f"{evenement['nom']}|{jours_restants}"
        texte = formater_rappel(evenement, jours_restants)

        if mode_test:
            print(f"[TEST] {texte}")
            continue

        if memoire.get(cle) == aujourdhui.isoformat():
            print(f"(déjà envoyé aujourd'hui) {evenement['nom']} J-{jours_restants}")
            continue

        if envoi_telegram.envoyer(texte):
            memoire[cle] = aujourdhui.isoformat()
            rappels_envoyes += 1
            print(f"✅ Envoyé : {evenement['nom']} J-{jours_restants}")
        else:
            print(f"❌ Échec d'envoi : {evenement['nom']} J-{jours_restants}")

    if not mode_test:
        sauver_memoire(memoire)
        if rappels_envoyes == 0:
            print("Aucun nouveau rappel à envoyer aujourd'hui.")
    elif not rappels_envoyes:
        print("[TEST] Aucun rappel ne serait envoyé aujourd'hui.")


def lancer_resume(evenements):
    """Envoie un récapitulatif de tous les événements à venir, triés par date."""
    aujourdhui = date.today()
    a_venir = sorted((e for e in evenements if e["date"] >= aujourdhui), key=lambda e: e["date"])

    if not a_venir:
        envoi_telegram.envoyer("📅 Récapitulatif UNSEEN. — aucun événement à venir dans le calendrier.")
        print("Résumé envoyé (aucun événement à venir).")
        return

    lignes = ["📅 Récapitulatif des événements à venir :"]
    for evenement in a_venir:
        lieu = f" ({evenement['ville']})" if evenement["ville"] else ""
        lignes.append(
            f"• {evenement['date'].strftime('%d/%m/%Y')} — "
            f"{envoi_telegram.proteger(evenement['nom'])}{lieu}"
        )

    envoi_telegram.envoyer("\n".join(lignes))
    print(f"✅ Résumé envoyé ({len(a_venir)} événement(s)).")


if __name__ == "__main__":
    analyseur = argparse.ArgumentParser()
    analyseur.add_argument("--test", action="store_true", help="Affiche sans rien envoyer")
    analyseur.add_argument("--resume", action="store_true", help="Envoie le récapitulatif groupé")
    arguments = analyseur.parse_args()

    evenements = lire_evenements()

    if arguments.resume:
        lancer_resume(evenements)
    else:
        lancer_rappels(evenements, arguments.test)
