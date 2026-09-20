"""
Radar UNSEEN. — Veille presse et nominations.

Lit les flux RSS listés dans sources.xlsx, trie les articles avec les
règles de mots-cles.xlsx, et envoie sur Telegram ce qui mérite ton
attention.

Trois façons de le lancer :
    python veille_presse.py --test     -> affiche le résultat, n'envoie rien
    python veille_presse.py            -> envoie les alertes rouges tout de suite
    python veille_presse.py --resume   -> envoie le résumé groupé du reste

Le détail est expliqué dans le README.md.
"""

import argparse
import calendar
import html
import json
import os
import re
import sys
import unicodedata
from datetime import datetime, timedelta, timezone
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

import feedparser
import requests
from openpyxl import load_workbook

import envoi_telegram

DOSSIER_SCRIPT = os.path.dirname(os.path.abspath(__file__))
FICHIER_SOURCES = os.path.join(DOSSIER_SCRIPT, "sources.xlsx")
FICHIER_MOTS_CLES = os.path.join(DOSSIER_SCRIPT, "mots-cles.xlsx")
FICHIER_MEMOIRE = os.path.join(DOSSIER_SCRIPT, "memoire.json")

NAVIGATEUR = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125 Safari/537.36",
    "Accept": "application/rss+xml, application/xml, text/xml, */*",
}

# Les cinq catégories, avec leur écriture officielle (accents compris).
CATEGORIES = {
    "nomination": "Nomination",
    "ouverture": "Ouverture",
    "evenement": "Événement",
    "tendance clientele": "Tendance clientèle",
    "concurrent": "Concurrent",
}

# Quand plusieurs thèmes correspondent, on garde le plus parlant.
ORDRE_CATEGORIES = ["Ouverture", "Événement", "Concurrent", "Tendance clientèle"]

MOIS_FR = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
           "août", "septembre", "octobre", "novembre", "décembre"]

# Paramètres de suivi qu'on retire des adresses avant de comparer deux articles.
PARAMETRES_PARASITES = {"fbclid", "gclid", "mc_cid", "mc_eid", "rct", "sa",
                        "usg", "ved", "ct", "cd", "source", "ref", "referrer"}


# ----------------------------------------------------------------------
# Petits outils de texte
# ----------------------------------------------------------------------

def normaliser(texte):
    """
    Met un texte à plat pour pouvoir le comparer :
    minuscules, sans accents, apostrophes uniformisées, espaces simples.
    « Directeur d'Hôtel » et « directeur d'hotel » deviennent identiques.
    """
    if texte is None:
        return ""
    texte = str(texte).replace("’", "'").replace("ʼ", "'")
    texte = unicodedata.normalize("NFD", texte)
    texte = "".join(c for c in texte if unicodedata.category(c) != "Mn")
    texte = texte.lower()
    return re.sub(r"\s+", " ", texte).strip()


def construire_regex(liste_mots):
    """
    Fabrique un chercheur de mots-clés.

    On cherche des mots entiers : « inde » ne se déclenchera donc pas
    sur « indépendant » ou « industrie ».
    """
    mots = [normaliser(m) for m in liste_mots if normaliser(m)]
    if not mots:
        return None
    # Les expressions les plus longues d'abord, pour attraper
    # « directeur general » plutôt que « directeur » tout seul.
    mots.sort(key=len, reverse=True)
    motif = "|".join(re.escape(m) for m in mots)
    return re.compile(r"\b(" + motif + r")\b")


def nettoyer_titre(titre):
    """Retire les balises de mise en gras que Google Alertes ajoute aux titres."""
    titre = re.sub(r"<[^>]+>", "", str(titre or ""))
    titre = html.unescape(titre).replace("\xa0", " ")
    return re.sub(r"\s+", " ", titre).strip()


def retirer_nom_du_journal(titre):
    """
    Google Alertes colle le nom du journal à la fin du titre :
    « Mauro Colagreco au Raffles London - Paris Select Book ».

    Sans ce nettoyage, le « Paris » du nom du journal ferait croire
    que l'article concerne Paris. On coupe donc ce suffixe.
    """
    morceaux = titre.rsplit(" - ", 1)
    if len(morceaux) == 2 and 0 < len(morceaux[1]) <= 40:
        return morceaux[0].strip()
    return titre


def nettoyer_lien(url):
    """
    Ramène une adresse à sa forme canonique.

    Deux choses importantes :
    - Google Alertes enveloppe les liens dans une redirection
      google.com/url?...&url=LA_VRAIE_ADRESSE : on extrait la vraie adresse,
      sinon le même article arriverait deux fois.
    - On retire les paramètres de suivi publicitaire (utm_source, etc.)
      qui changent à chaque envoi.
    """
    url = str(url or "").strip()
    if not url:
        return ""

    if "google.com/url" in url or "google.com/alerts" in url:
        parametres = dict(parse_qsl(urlparse(url).query))
        if parametres.get("url"):
            url = parametres["url"]

    morceaux = urlparse(url)
    parametres_gardes = [
        (cle, valeur) for cle, valeur in parse_qsl(morceaux.query)
        if not cle.lower().startswith("utm_") and cle.lower() not in PARAMETRES_PARASITES
    ]

    return urlunparse((
        morceaux.scheme or "https",
        morceaux.netloc.lower(),
        morceaux.path.rstrip("/"),
        "",
        urlencode(parametres_gardes),
        "",
    ))


def date_en_francais(moment):
    """Transforme une date en « 20 septembre »."""
    return f"{moment.day} {MOIS_FR[moment.month - 1]}"


# ----------------------------------------------------------------------
# Lecture des fichiers Excel
# ----------------------------------------------------------------------

def lire_feuille(chemin, nom_feuille):
    """Lit un onglet Excel et renvoie la liste des lignes (sans l'en-tête)."""
    if not os.path.exists(chemin):
        print(f"❌ Fichier introuvable : {chemin}")
        sys.exit(1)

    classeur = load_workbook(chemin, data_only=True)
    if nom_feuille not in classeur.sheetnames:
        print(f"❌ L'onglet « {nom_feuille} » est absent de {os.path.basename(chemin)}.")
        sys.exit(1)

    feuille = classeur[nom_feuille]
    lignes = []
    for ligne in feuille.iter_rows(min_row=2, values_only=True):
        if ligne and any(cellule not in (None, "") for cellule in ligne):
            lignes.append(["" if c is None else c for c in ligne])
    return lignes


def lire_sources():
    """Renvoie la liste des sources actives de sources.xlsx."""
    sources = []
    for ligne in lire_feuille(FICHIER_SOURCES, "Sources"):
        ligne = list(ligne) + [""] * (6 - len(ligne))
        nom, url, type_source, actif, categorie_imposee, _note = ligne[:6]

        if normaliser(actif) != "oui":
            continue
        if not str(url).strip():
            print(f"⚠️  Source « {nom} » marquée active mais sans adresse de flux : ignorée.")
            continue

        sources.append({
            "nom": str(nom).strip(),
            "url": str(url).strip(),
            "type": str(type_source).strip(),
            "categorie_imposee": CATEGORIES.get(normaliser(categorie_imposee), ""),
            "est_alerte_google": "google.com/alerts" in str(url).lower(),
        })
    return sources


def lire_mots_cles():
    """Charge tous les onglets de mots-cles.xlsx et prépare les chercheurs."""
    postes = [l[0] for l in lire_feuille(FICHIER_MOTS_CLES, "Postes") if l[0]]
    verbes = [l[0] for l in lire_feuille(FICHIER_MOTS_CLES, "Verbes de nomination") if l[0]]

    zones = []
    for ligne in lire_feuille(FICHIER_MOTS_CLES, "Zones"):
        ligne = list(ligne) + [""] * (3 - len(ligne))
        nom, variantes, prioritaire = ligne[:3]
        mots = [m.strip() for m in str(variantes).split(",") if m.strip()]
        if not mots:
            mots = [str(nom)]
        zones.append({
            "nom": str(nom).strip(),
            "regex": construire_regex(mots),
            "prioritaire": normaliser(prioritaire) == "oui",
        })

    themes = []
    for ligne in lire_feuille(FICHIER_MOTS_CLES, "Themes"):
        ligne = list(ligne) + [""] * (2 - len(ligne))
        mot, categorie = ligne[:2]
        if not str(mot).strip():
            continue
        themes.append({
            "regex": construire_regex([mot]),
            "categorie": CATEGORIES.get(normaliser(categorie), ""),
        })

    exclusions = [l[0] for l in lire_feuille(FICHIER_MOTS_CLES, "Exclusions") if l[0]]

    actions = {}
    for ligne in lire_feuille(FICHIER_MOTS_CLES, "Actions"):
        ligne = list(ligne) + [""] * (2 - len(ligne))
        categorie, action = ligne[:2]
        canonique = CATEGORIES.get(normaliser(categorie))
        if canonique:
            actions[canonique] = str(action).strip()

    return {
        "postes": construire_regex(postes),
        "verbes": construire_regex(verbes),
        "zones": zones,
        "themes": themes,
        "exclusions": construire_regex(exclusions),
        "actions": actions,
    }


def lire_reglages():
    """Charge l'onglet Réglages, avec des valeurs de secours si besoin."""
    valeurs = {
        "age_max_jours": 10,
        "max_rouges_par_passage": 5,
        "max_articles_resume": 12,
        "message_si_rien": "oui",
    }
    for ligne in lire_feuille(FICHIER_MOTS_CLES, "Reglages"):
        ligne = list(ligne) + [""] * (2 - len(ligne))
        cle, valeur = normaliser(ligne[0]), ligne[1]
        if cle in valeurs:
            valeurs[cle] = valeur

    for cle in ("age_max_jours", "max_rouges_par_passage", "max_articles_resume"):
        try:
            valeurs[cle] = int(valeurs[cle])
        except (TypeError, ValueError):
            print(f"⚠️  Réglage « {cle} » illisible, valeur par défaut utilisée.")
            valeurs[cle] = {"age_max_jours": 10, "max_rouges_par_passage": 5,
                            "max_articles_resume": 12}[cle]

    valeurs["message_si_rien"] = normaliser(valeurs["message_si_rien"]) == "oui"
    return valeurs


# ----------------------------------------------------------------------
# Mémoire (articles déjà traités)
# ----------------------------------------------------------------------

def charger_memoire():
    if not os.path.exists(FICHIER_MEMOIRE):
        return {"initialise": False, "vus": {}, "en_attente": []}
    try:
        with open(FICHIER_MEMOIRE, "r", encoding="utf-8") as fichier:
            memoire = json.load(fichier)
    except (json.JSONDecodeError, OSError):
        print("⚠️  memoire.json illisible : on repart d'une mémoire vide.")
        return {"initialise": False, "vus": {}, "en_attente": []}

    memoire.setdefault("initialise", False)
    memoire.setdefault("vus", {})
    memoire.setdefault("en_attente", [])
    return memoire


def sauver_memoire(memoire):
    """Enregistre la mémoire, en oubliant les articles de plus de 90 jours."""
    limite = (datetime.now(timezone.utc) - timedelta(days=90)).strftime("%Y-%m-%d")
    memoire["vus"] = {url: jour for url, jour in memoire["vus"].items() if jour >= limite}

    with open(FICHIER_MEMOIRE, "w", encoding="utf-8") as fichier:
        json.dump(memoire, fichier, ensure_ascii=False, indent=1)


# ----------------------------------------------------------------------
# Lecture des flux
# ----------------------------------------------------------------------

def recuperer_flux(source):
    """Télécharge un flux RSS et renvoie ses articles. Ne plante jamais."""
    try:
        reponse = requests.get(source["url"], headers=NAVIGATEUR, timeout=25)
    except requests.exceptions.RequestException as erreur:
        return None, f"connexion impossible ({type(erreur).__name__})"

    if reponse.status_code != 200:
        return None, f"le site répond {reponse.status_code}"

    flux = feedparser.parse(reponse.content)
    if not flux.entries:
        # Une Google Alerte sans résultat récent est un flux valide mais vide :
        # ce n'est pas une panne.
        if flux.feed.get("title"):
            return [], None
        return None, "flux illisible"

    return flux.entries, None


def date_article(entree):
    """Récupère la date de publication d'un article, ou None."""
    for champ in ("published_parsed", "updated_parsed"):
        valeur = entree.get(champ)
        if valeur:
            try:
                return datetime.fromtimestamp(calendar.timegm(valeur), tz=timezone.utc)
            except (ValueError, OverflowError):
                continue
    return None


# ----------------------------------------------------------------------
# Le tri : c'est ici que se décide ce qui t'est envoyé
# ----------------------------------------------------------------------

def trouver_signaux(texte, mots):
    """Relève tous les mots-clés présents dans un texte déjà normalisé."""
    zone_trouvee = ""
    zone_prioritaire = False
    for zone in mots["zones"]:
        if zone["regex"] and zone["regex"].search(texte):
            # Une zone prioritaire l'emporte toujours sur une zone secondaire.
            if zone["prioritaire"] and not zone_prioritaire:
                zone_trouvee, zone_prioritaire = zone["nom"], True
            elif not zone_trouvee:
                zone_trouvee = zone["nom"]

    categories_themes = []
    for theme in mots["themes"]:
        if theme["regex"] and theme["regex"].search(texte):
            if theme["categorie"]:
                categories_themes.append(theme["categorie"])
            else:
                categories_themes.append("")

    return {
        "poste": bool(mots["postes"] and mots["postes"].search(texte)),
        "verbe": bool(mots["verbes"] and mots["verbes"].search(texte)),
        "zone": zone_trouvee,
        "zone_prioritaire": zone_prioritaire,
        "themes": categories_themes,
    }


def deduire_categorie(signaux):
    """Devine la catégorie à partir des signaux relevés, ou renvoie ''."""
    if signaux["verbe"] and signaux["poste"]:
        return "Nomination"
    for candidate in ORDRE_CATEGORIES:
        if candidate in signaux["themes"]:
            return candidate
    return ""


def analyser(titre, resume, mots, categorie_imposee):
    """
    Décide si un article t'intéresse.

    Renvoie un dictionnaire (catégorie, priorité, zone, action)
    ou None si l'article doit être jeté.

    Principe : le résumé sert à repérer un article intéressant, mais une
    alerte rouge exige que la preuve soit dans le TITRE. Les résumés sont
    trop souvent trompeurs — un article sur Rio peut citer Paris en passant.
    """
    texte_complet = normaliser(titre + " . " + resume)
    texte_titre = normaliser(titre)

    # 1. Les exclusions passent avant tout le reste.
    if mots["exclusions"] and mots["exclusions"].search(texte_complet):
        return None

    signaux = trouver_signaux(texte_complet, mots)
    signaux_titre = trouver_signaux(texte_titre, mots)

    # 2. Quelle catégorie ? Une source peut imposer la sienne
    #    (cas des Google Alertes, qui ont déjà fait le tri en amont).
    categorie = deduire_categorie(signaux)
    categorie_deduite = bool(categorie)
    if not categorie:
        categorie = categorie_imposee

    # 3. Rien de reconnu : on jette. C'est le filtre principal contre le bruit.
    if not categorie:
        return None
    if not (signaux["poste"] or signaux["verbe"] or signaux["themes"] or categorie_imposee):
        return None

    # 4. Quelle priorité ?
    #    Rouge = nomination ou ouverture réellement détectée (pas seulement
    #    imposée par la source), confirmée par le titre, en zone prioritaire.
    confirme_par_le_titre = deduire_categorie(signaux_titre) == categorie
    merite_le_rouge = (
        categorie in ("Nomination", "Ouverture")
        and categorie_deduite
        and confirme_par_le_titre
        and signaux_titre["zone_prioritaire"]
    )

    # La géographie est le vrai filtre : une nomination dans une ville où tes
    # clients ne vont jamais ne mérite pas de remonter au même niveau qu'une
    # nomination parisienne.
    #
    # Une ville citée dans le titre est un signal fiable. Une ville citée
    # seulement dans le résumé l'est beaucoup moins, sauf pour les nominations
    # et les ouvertures : là, le titre nomme souvent l'établissement sans
    # préciser la ville (« Le Bristol nomme un nouveau directeur général »),
    # et ce sont les articles qu'on veut surtout ne pas rater.
    categorie_forte = categorie in ("Nomination", "Ouverture") and categorie_deduite

    if merite_le_rouge:
        priorite = "🔴"
    elif signaux_titre["zone"] or (signaux["zone"] and categorie_forte):
        priorite = "🟠"
    else:
        priorite = "⚪"

    return {
        "categorie": categorie,
        "priorite": priorite,
        "zone": signaux_titre["zone"] or signaux["zone"],
        "action": mots["actions"].get(categorie, ""),
    }


def collecter(sources, mots, reglages, memoire, mode_test):
    """Parcourt toutes les sources et renvoie les articles retenus."""
    plus_vieux_accepte = datetime.now(timezone.utc) - timedelta(days=reglages["age_max_jours"])
    retenus = []
    total_lus = 0

    for source in sources:
        entrees, erreur = recuperer_flux(source)
        if erreur:
            print(f"   ⚠️  {source['nom']} : {erreur}")
            continue

        gardes_ici = 0
        for entree in entrees:
            total_lus += 1

            lien = nettoyer_lien(entree.get("link", ""))
            if not lien:
                continue
            if not mode_test and lien in memoire["vus"]:
                continue

            publie_le = date_article(entree)
            if publie_le and publie_le < plus_vieux_accepte:
                continue

            titre = nettoyer_titre(entree.get("title", ""))
            if not titre:
                continue

            if source["est_alerte_google"]:
                # Deux pièges propres aux Google Alertes : le nom du journal
                # est collé au titre, et le résumé n'est qu'un assemblage de
                # fragments pris un peu partout dans la page. On ne se fie
                # donc qu'au titre, une fois le nom du journal retiré.
                titre = retirer_nom_du_journal(titre)
                resume = ""
            else:
                resume = nettoyer_titre(entree.get("summary", ""))[:1200]

            verdict = analyser(titre, resume, mots, source["categorie_imposee"])
            if not verdict:
                continue

            retenus.append({
                "titre": titre,
                "lien": lien,
                "source": source["nom"],
                "date": (publie_le or datetime.now(timezone.utc)).isoformat(),
                **verdict,
            })
            gardes_ici += 1

        print(f"   ✓ {source['nom']} : {len(entrees)} articles lus, {gardes_ici} retenus")

    # Les plus urgents et les plus récents en premier.
    rang = {"🔴": 0, "🟠": 1, "⚪": 2}
    retenus.sort(key=lambda a: (rang[a["priorite"]], a["date"]), reverse=False)
    retenus.sort(key=lambda a: rang[a["priorite"]])

    print(f"\n   Total : {total_lus} articles lus, {len(retenus)} retenus.")
    return retenus


# ----------------------------------------------------------------------
# Mise en forme des messages Telegram
# ----------------------------------------------------------------------

def message_urgent(article):
    """Le message d'une alerte rouge, envoyée seule."""
    moment = datetime.fromisoformat(article["date"])
    entete = f"{article['priorite']} {article['categorie'].upper()}"
    if article["zone"]:
        entete += f" · {article['zone']}"

    lignes = [
        entete,
        envoi_telegram.lien_cliquable(article["lien"], article["titre"]),
        f"{envoi_telegram.proteger(article['source'])} · {date_en_francais(moment)}",
    ]
    if article["action"]:
        lignes.append("")
        lignes.append(f"→ À faire : {envoi_telegram.proteger(article['action'])}")

    return "\n".join(lignes)


def message_resume(articles, reglages):
    """Le résumé groupé, envoyé une fois par jour."""
    aujourdhui = date_en_francais(datetime.now())
    lignes = [f"📋 <b>Radar UNSEEN.</b> — résumé du {aujourdhui}", ""]

    detailles = articles[:reglages["max_articles_resume"]]
    restants = len(articles) - len(detailles)

    groupes = [
        ("🔴", "Urgent"),
        ("🟠", "Pertinent"),
        ("⚪", "À surveiller"),
    ]

    for symbole, intitule in groupes:
        du_groupe = [a for a in detailles if a["priorite"] == symbole]
        if not du_groupe:
            continue

        lignes.append(f"{symbole} <b>{intitule}</b> ({len(du_groupe)})")
        lignes.append("")

        for article in du_groupe:
            moment = datetime.fromisoformat(article["date"])
            lignes.append(envoi_telegram.lien_cliquable(article["lien"], article["titre"]))

            contexte = f"{article['source']} · {date_en_francais(moment)} · {article['categorie']}"
            if article["zone"]:
                contexte += f" · {article['zone']}"
            lignes.append(envoi_telegram.proteger(contexte))

            if symbole != "⚪" and article["action"]:
                lignes.append(f"→ {envoi_telegram.proteger(article['action'])}")
            lignes.append("")

    if restants > 0:
        lignes.append(f"<i>+ {restants} autre(s) article(s) de moindre importance, non détaillés.</i>")

    return "\n".join(lignes).rstrip()


def apercu_terminal(articles):
    """Affiche les articles retenus dans le terminal, sans rien envoyer."""
    if not articles:
        print("\n   Aucun article ne correspond à tes critères pour le moment.")
        return

    print("\n" + "=" * 70)
    for article in articles:
        moment = datetime.fromisoformat(article["date"])
        zone = f" · {article['zone']}" if article["zone"] else ""
        print(f"\n{article['priorite']} {article['categorie'].upper()}{zone}")
        print(f"   {article['titre']}")
        print(f"   {article['source']} · {date_en_francais(moment)}")
        if article["action"]:
            print(f"   → {article['action']}")
        print(f"   {article['lien']}")
    print("\n" + "=" * 70)


# ----------------------------------------------------------------------
# Les trois modes de lancement
# ----------------------------------------------------------------------

def marquer_vu(memoire, article):
    memoire["vus"][article["lien"]] = datetime.now(timezone.utc).strftime("%Y-%m-%d")


def lancer_resume(memoire, reglages):
    """Envoie le résumé groupé et vide la file d'attente."""
    en_attente = memoire.get("en_attente", [])

    if not en_attente:
        print("Rien en attente.")
        if reglages["message_si_rien"]:
            envoi_telegram.envoyer("📋 <b>Radar UNSEEN.</b> — rien à signaler aujourd'hui.")
            print("Message de confirmation envoyé.")
        return

    rang = {"🔴": 0, "🟠": 1, "⚪": 2}
    en_attente.sort(key=lambda a: rang.get(a["priorite"], 3))

    print(f"Envoi du résumé : {len(en_attente)} article(s) en attente.")
    if envoi_telegram.envoyer(message_resume(en_attente, reglages)):
        memoire["en_attente"] = []
        sauver_memoire(memoire)
        print("✅ Résumé envoyé.")
    else:
        print("❌ Envoi échoué : les articles restent en attente pour le prochain essai.")


def lancer_collecte(memoire, sources, mots, reglages, mode_test):
    print(f"Lecture de {len(sources)} source(s)...\n")
    articles = collecter(sources, mots, reglages, memoire, mode_test)

    # --- Mode test : on montre et on s'arrête.
    if mode_test:
        print("\n(Mode test : rien n'a été envoyé et rien n'a été enregistré.)")
        apercu_terminal(articles)
        return

    # --- Tout premier lancement : on remplit la mémoire sans rien envoyer.
    if not memoire["initialise"]:
        print("\n" + "=" * 70)
        print("PREMIER LANCEMENT")
        print("Les flux contiennent parfois 100 articles d'un coup.")
        print("Pour ne pas te noyer, rien n'est envoyé cette fois-ci.")
        print("Voici ce qui t'aurait été envoyé, pour que tu puisses")
        print("ajuster mots-cles.xlsx avant de démarrer pour de bon :")
        apercu_terminal(articles)

        for article in articles:
            marquer_vu(memoire, article)
        memoire["initialise"] = True
        sauver_memoire(memoire)

        print(f"\n✅ Mémoire initialisée ({len(articles)} articles enregistrés).")
        print("   La veille démarre vraiment au prochain lancement.")
        return

    # --- Fonctionnement normal.
    rouges = [a for a in articles if a["priorite"] == "🔴"]
    autres = [a for a in articles if a["priorite"] != "🔴"]

    a_envoyer = rouges[:reglages["max_rouges_par_passage"]]
    en_trop = rouges[reglages["max_rouges_par_passage"]:]

    envoyes = 0
    for article in a_envoyer:
        if envoi_telegram.envoyer(message_urgent(article)):
            marquer_vu(memoire, article)
            envoyes += 1
        else:
            print(f"⚠️  Échec de l'envoi pour « {article['titre'][:50]} » : sera réessayé.")

    # Le reste part en file d'attente pour le résumé.
    for article in en_trop + autres:
        memoire["en_attente"].append(article)
        marquer_vu(memoire, article)

    sauver_memoire(memoire)

    print(f"\n✅ {envoyes} alerte(s) rouge(s) envoyée(s) tout de suite.")
    print(f"   {len(en_trop) + len(autres)} article(s) mis en attente du résumé.")
    if en_trop:
        print(f"   (dont {len(en_trop)} alertes rouges au-delà de la limite par passage)")


def principal():
    analyseur = argparse.ArgumentParser(
        description="Radar UNSEEN. — veille presse et nominations")
    analyseur.add_argument("--test", action="store_true",
                           help="affiche le résultat dans le terminal sans rien envoyer")
    analyseur.add_argument("--resume", action="store_true",
                           help="envoie le résumé groupé des articles en attente")
    arguments = analyseur.parse_args()

    reglages = lire_reglages()
    memoire = charger_memoire()

    if arguments.resume:
        lancer_resume(memoire, reglages)
        return

    sources = lire_sources()
    if not sources:
        print("❌ Aucune source active dans sources.xlsx.")
        sys.exit(1)

    mots = lire_mots_cles()
    lancer_collecte(memoire, sources, mots, reglages, arguments.test)


if __name__ == "__main__":
    principal()
