"""
Radar UNSEEN. — Carnet de groupes annoncés.

Quand un partenaire (guide, chauffeur, DMC, hôtel, tour-opérateur) te
prévient qu'un groupe ou une famille arrive à Paris, tu envoies simplement
un message Telegram au bot avec ce qu'on t'a dit, en texte libre. Ce script
range l'info dans une base Notion, et te rappelle chaque groupe avant son
arrivée pour que tu le contactes en amont.

Trois façons de le lancer :
    python radar_groupes.py --recevoir   -> range dans Notion les messages
                                             Telegram reçus depuis la dernière fois
    python radar_groupes.py --rappels    -> envoie le rappel groupé du jour
                                             (J-30, J-14, J-3)
    python radar_groupes.py --nouveaux   -> rappelle les groupes ajoutés cette
                                             semaine et pas encore contactés

Ajoute --test à n'importe lequel pour voir le résultat dans le terminal
sans rien envoyer ni rien enregistrer.

Le détail est expliqué dans le README.md.
"""

import argparse
import json
import os
import sys
from datetime import date, datetime, timedelta

import requests
from dotenv import load_dotenv

import envoi_telegram

DOSSIER_SCRIPT = os.path.dirname(os.path.abspath(__file__))
CHEMIN_ENV = os.path.join(DOSSIER_SCRIPT, ".env")
FICHIER_MEMOIRE = os.path.join(DOSSIER_SCRIPT, "memoire_groupes.json")

JALONS = [30, 14, 3]
NOTION_VERSION = "2022-06-28"


# ----------------------------------------------------------------------
# Identifiants et connexion
# ----------------------------------------------------------------------

def lire_identifiants():
    """Récupère les identifiants Telegram et Notion depuis le fichier .env."""
    load_dotenv(CHEMIN_ENV)
    telegram_token = os.getenv("TELEGRAM_TOKEN", "").strip()
    telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID", "").strip()
    notion_token = os.getenv("NOTION_TOKEN", "").strip()
    notion_database_id = os.getenv("NOTION_DATABASE_ID", "").strip()

    manquants = [
        nom for nom, valeur in (
            ("TELEGRAM_TOKEN", telegram_token),
            ("TELEGRAM_CHAT_ID", telegram_chat_id),
            ("NOTION_TOKEN", notion_token),
            ("NOTION_DATABASE_ID", notion_database_id),
        ) if not valeur
    ]
    if manquants:
        print(f"❌ Il manque dans .env : {', '.join(manquants)}")
        sys.exit(1)

    return telegram_token, telegram_chat_id, notion_token, notion_database_id


def entetes_notion(notion_token):
    return {
        "Authorization": f"Bearer {notion_token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }


# ----------------------------------------------------------------------
# Mémoire (dernier message Telegram lu, rappels déjà envoyés)
# ----------------------------------------------------------------------

def charger_memoire():
    if not os.path.exists(FICHIER_MEMOIRE):
        return {"dernier_update_id": 0, "rappels_envoyes": {}}
    try:
        with open(FICHIER_MEMOIRE, "r", encoding="utf-8") as fichier:
            memoire = json.load(fichier)
    except (json.JSONDecodeError, OSError):
        print("⚠️  memoire_groupes.json illisible : on repart d'une mémoire vide.")
        return {"dernier_update_id": 0, "rappels_envoyes": {}}

    memoire.setdefault("dernier_update_id", 0)
    memoire.setdefault("rappels_envoyes", {})
    return memoire


def sauver_memoire(memoire):
    """Enregistre la mémoire, en oubliant les rappels de plus d'un an."""
    limite = date.today().replace(year=date.today().year - 1).isoformat()
    memoire["rappels_envoyes"] = {
        cle: jour for cle, jour in memoire["rappels_envoyes"].items() if jour >= limite
    }
    with open(FICHIER_MEMOIRE, "w", encoding="utf-8") as fichier:
        json.dump(memoire, fichier, ensure_ascii=False, indent=1)


# ----------------------------------------------------------------------
# Réception : lire les messages Telegram et créer une fiche Notion
# ----------------------------------------------------------------------

def recuperer_nouveaux_messages(telegram_token, telegram_chat_id, dernier_update_id):
    """Récupère les messages Telegram envoyés par Jay depuis le dernier passage."""
    reponse = requests.get(
        f"https://api.telegram.org/bot{telegram_token}/getUpdates",
        params={"offset": dernier_update_id + 1, "timeout": 0},
        timeout=20,
    )
    donnees = reponse.json()
    if not donnees.get("ok"):
        print(f"❌ Telegram a refusé la lecture des messages : {donnees.get('description')}")
        sys.exit(1)

    messages = []
    plus_grand_id = dernier_update_id
    for mise_a_jour in donnees.get("result", []):
        plus_grand_id = max(plus_grand_id, mise_a_jour["update_id"])
        message = mise_a_jour.get("message")
        if not message:
            continue
        # On ignore les messages qui ne viennent pas du chat de Jay
        # (par exemple si le bot est ajouté ailleurs par erreur).
        if str(message.get("chat", {}).get("id", "")) != str(telegram_chat_id):
            continue
        texte = (message.get("text") or "").strip()
        # On ignore les commandes du bot (/start, etc.), pas des signalements.
        if texte and not texte.startswith("/"):
            messages.append(texte)

    return messages, plus_grand_id


def creer_fiche_notion(notion_token, notion_database_id, texte):
    """Crée une fiche 'À compléter' dans la base Notion à partir d'un texte libre."""
    premiere_ligne = texte.strip().splitlines()[0][:80] if texte.strip() else "Groupe signalé"

    payload = {
        "parent": {"database_id": notion_database_id},
        "properties": {
            "Nom du groupe / client": {
                "title": [{"text": {"content": premiere_ligne}}]
            },
            "Notes": {
                "rich_text": [{"text": {"content": texte[:2000]}}]
            },
            "Statut": {"select": {"name": "À compléter"}},
        },
    }
    reponse = requests.post(
        "https://api.notion.com/v1/pages",
        headers=entetes_notion(notion_token),
        json=payload,
        timeout=20,
    )
    return reponse.status_code == 200


def lancer_reception(mode_test):
    telegram_token, telegram_chat_id, notion_token, notion_database_id = lire_identifiants()
    memoire = charger_memoire()

    messages, plus_grand_id = recuperer_nouveaux_messages(
        telegram_token, telegram_chat_id, memoire["dernier_update_id"]
    )

    if not messages:
        print("Aucun nouveau message à ranger.")
        return

    if mode_test:
        print(f"[TEST] {len(messages)} message(s) seraient rangés dans Notion :")
        for texte in messages:
            print(f"  • {texte[:100]}")
        return

    crees = 0
    for texte in messages:
        if creer_fiche_notion(notion_token, notion_database_id, texte):
            crees += 1
            print(f"✅ Fiche créée : {texte[:60]}")
        else:
            print(f"❌ Échec de création pour : {texte[:60]}")

    memoire["dernier_update_id"] = plus_grand_id
    sauver_memoire(memoire)
    print(f"\n{crees}/{len(messages)} fiche(s) créée(s) dans Notion.")


# ----------------------------------------------------------------------
# Lecture des groupes dans Notion
# ----------------------------------------------------------------------

def texte_riche(propriete):
    return "".join(morceau["plain_text"] for morceau in propriete.get("rich_text", []))


def texte_titre(propriete):
    return "".join(morceau["plain_text"] for morceau in propriete.get("title", []))


def recuperer_groupes(notion_token, notion_database_id):
    """Renvoie tous les groupes de la base Notion, avec leurs champs utiles."""
    groupes = []
    curseur = None

    while True:
        corps = {"page_size": 100}
        if curseur:
            corps["start_cursor"] = curseur

        reponse = requests.post(
            f"https://api.notion.com/v1/databases/{notion_database_id}/query",
            headers=entetes_notion(notion_token),
            json=corps,
            timeout=20,
        )
        donnees = reponse.json()
        if reponse.status_code != 200:
            print(f"❌ Erreur Notion : {donnees.get('message', reponse.status_code)}")
            sys.exit(1)

        for page in donnees.get("results", []):
            proprietes = page["properties"]
            statut_brut = proprietes["Statut"]["select"]
            statut = statut_brut["name"] if statut_brut else "À compléter"

            date_arrivee_brute = proprietes["Date d'arrivée"]["date"]
            date_arrivee = None
            if date_arrivee_brute and date_arrivee_brute.get("start"):
                date_arrivee = datetime.strptime(
                    date_arrivee_brute["start"][:10], "%Y-%m-%d"
                ).date()

            groupes.append({
                "id": page["id"],
                "nom": texte_titre(proprietes["Nom du groupe / client"]) or "Groupe sans nom",
                "date_arrivee": date_arrivee,
                "nationalite": texte_riche(proprietes["Nationalité / zone"]),
                "taille": texte_riche(proprietes["Taille du groupe"]),
                "signale_par": texte_riche(proprietes["Signalé par"]),
                "contact": texte_riche(proprietes["Contact partenaire"]),
                "statut": statut,
                "cree_le": page["created_time"],
            })

        curseur = donnees.get("next_cursor")
        if not donnees.get("has_more"):
            break

    return groupes


# ----------------------------------------------------------------------
# Rappels groupés
# ----------------------------------------------------------------------

def formater_ligne(groupe, jours_restants):
    lieu = f" ({groupe['nationalite']})" if groupe["nationalite"] else ""
    taille = f" · {groupe['taille']}" if groupe["taille"] else ""
    lignes = [f"🧳 J-{jours_restants} : {envoi_telegram.proteger(groupe['nom'])}{lieu}{taille}"]
    lignes.append(f"   Arrivée le {groupe['date_arrivee'].strftime('%d/%m/%Y')}")
    if groupe["signale_par"] or groupe["contact"]:
        signale = envoi_telegram.proteger(groupe["signale_par"])
        contact = envoi_telegram.proteger(groupe["contact"])
        detail = " · ".join(part for part in (signale, contact) if part)
        lignes.append(f"   Signalé par : {detail}")
    return "\n".join(lignes)


def lancer_rappels(mode_test):
    _, _, notion_token, notion_database_id = lire_identifiants()
    groupes = recuperer_groupes(notion_token, notion_database_id)
    aujourdhui = date.today()
    memoire = charger_memoire()

    a_signaler = []
    cles_du_jour = []
    for groupe in groupes:
        if not groupe["date_arrivee"] or groupe["statut"] == "Sans suite":
            continue
        jours_restants = (groupe["date_arrivee"] - aujourdhui).days
        if jours_restants not in JALONS:
            continue

        cle = f"{groupe['id']}|{jours_restants}"
        if memoire["rappels_envoyes"].get(cle) == aujourdhui.isoformat():
            continue

        a_signaler.append(formater_ligne(groupe, jours_restants))
        cles_du_jour.append(cle)

    if not a_signaler:
        print("Aucun rappel à envoyer aujourd'hui.")
        return

    texte = "🧳 <b>Radar UNSEEN. — groupes à recontacter</b>\n\n" + "\n\n".join(a_signaler)

    if mode_test:
        print(f"[TEST]\n{texte}")
        return

    if envoi_telegram.envoyer(texte):
        for cle in cles_du_jour:
            memoire["rappels_envoyes"][cle] = aujourdhui.isoformat()
        sauver_memoire(memoire)
        print(f"✅ Rappel envoyé ({len(a_signaler)} groupe(s)).")
    else:
        print("❌ Échec d'envoi du rappel.")


# ----------------------------------------------------------------------
# Récapitulatif hebdomadaire des nouveaux signalements
# ----------------------------------------------------------------------

def lancer_nouveaux(mode_test):
    _, _, notion_token, notion_database_id = lire_identifiants()
    groupes = recuperer_groupes(notion_token, notion_database_id)

    limite = datetime.now().astimezone() - timedelta(days=7)
    recents = [
        g for g in groupes
        if g["statut"] in ("À compléter", "À contacter")
        and datetime.fromisoformat(g["cree_le"].replace("Z", "+00:00")) >= limite
    ]

    if not recents:
        print("Aucun nouveau signalement cette semaine.")
        if not mode_test:
            envoi_telegram.envoyer(
                "🧳 <b>Radar UNSEEN.</b> — aucun nouveau groupe signalé cette semaine."
            )
        return

    lignes = [f"🧳 <b>Radar UNSEEN.</b> — {len(recents)} nouveau(x) signalement(s) cette semaine :", ""]
    for groupe in recents:
        date_txt = groupe["date_arrivee"].strftime("%d/%m/%Y") if groupe["date_arrivee"] else "date à préciser"
        lignes.append(f"• {envoi_telegram.proteger(groupe['nom'])} — {date_txt} — {groupe['statut']}")

    texte = "\n".join(lignes)

    if mode_test:
        print(f"[TEST]\n{texte}")
        return

    if envoi_telegram.envoyer(texte):
        print(f"✅ Récapitulatif envoyé ({len(recents)} groupe(s)).")
    else:
        print("❌ Échec d'envoi du récapitulatif.")


# ----------------------------------------------------------------------
if __name__ == "__main__":
    analyseur = argparse.ArgumentParser(
        description="Radar UNSEEN. — carnet de groupes annoncés")
    groupe_mode = analyseur.add_mutually_exclusive_group(required=True)
    groupe_mode.add_argument("--recevoir", action="store_true",
                              help="range dans Notion les messages Telegram reçus")
    groupe_mode.add_argument("--rappels", action="store_true",
                              help="envoie le rappel groupé du jour (J-30/J-14/J-3)")
    groupe_mode.add_argument("--nouveaux", action="store_true",
                              help="récapitulatif hebdomadaire des groupes ajoutés récemment")
    analyseur.add_argument("--test", action="store_true",
                            help="affiche le résultat sans rien envoyer ni enregistrer")
    arguments = analyseur.parse_args()

    if arguments.recevoir:
        lancer_reception(arguments.test)
    elif arguments.rappels:
        lancer_rappels(arguments.test)
    elif arguments.nouveaux:
        lancer_nouveaux(arguments.test)
