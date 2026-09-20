# Radar UNSEEN.

Veille presse, nominations et calendrier des événements, envoyés sur
Telegram.

---

## Installation (à faire une seule fois)

Déjà fait sur ce Mac. Pour mémoire, ou pour réinstaller ailleurs :

```
cd radar-unseen
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
./venv/bin/python connexion_telegram.py
```

Le token du bot se colle dans le fichier `.env`, jamais dans le code.
`.env` n'est jamais envoyé sur GitHub.

---

## Étape 1 — Connexion Telegram ✅

`connexion_telegram.py` récupère ton `chat_id` et envoie un message de test.
À relancer seulement si tu changes de bot.

---

## Étape 2 — Veille presse et nominations ✅

### Les trois commandes

Toujours depuis le dossier `radar-unseen` :

```
./venv/bin/python veille_presse.py --test
```
**Le mode réglage.** Lit toutes les sources, affiche le résultat dans le
terminal et **n'envoie rien, n'enregistre rien**. C'est la commande à
utiliser après chaque modification de tes mots-clés, autant de fois que tu
veux, sans risque.

```
./venv/bin/python veille_presse.py
```
**Le vrai passage.** Envoie immédiatement les alertes 🔴 et met le reste
en attente. À lancer plusieurs fois par jour.

```
./venv/bin/python veille_presse.py --resume
```
**Le résumé.** Envoie en un seul message tout ce qui était en attente.
À lancer une fois par jour, le matin.

Plus tard (étape 4), GitHub Actions lancera ces commandes tout seul.

---

### Les deux fichiers Excel : c'est là que tu règles tout

Tu ne touches jamais au code. Tout se règle dans ces deux fichiers.
Après chaque modification : enregistre, ferme le fichier, puis relance
`veille_presse.py --test` pour voir l'effet.

#### `sources.xlsx`

La liste des flux lus. **12 flux RSS** vérifiés + **7 de tes Google Alertes**.

La colonne **Actif** (`oui` / `non`) est ton interrupteur : une source
devient trop bavarde, tu mets `non`, c'est réglé.

La colonne **Catégorie imposée** sert à tes Google Alertes qui ont déjà
fait le tri en amont : tout ce qui vient de l'alerte « Ouvertures » est
classé Ouverture sans autre examen. Laisse vide pour les sources
généralistes.

#### `mots-cles.xlsx`

| Onglet | Ce qu'il contient |
|---|---|
| Postes | Les 75 intitulés de poste à repérer, en français et en anglais |
| Verbes de nomination | « nommé », « rejoint », « appointed », « joins as »… |
| Zones | Les villes suivies. Colonne **Prioritaire** : `oui` = peut déclencher une alerte rouge |
| Themes | Les sujets suivis hors nominations |
| Exclusions | Les mots qui font jeter un article (offre d'emploi, webinaire, code promo…) |
| Actions | Le texte de l'action suggérée, par catégorie |
| Reglages | Les quelques chiffres qui règlent le volume |

Les accents et les majuscules n'ont aucune importance. Le script cherche
des **mots entiers** : « inde » ne se déclenche pas sur « industrie ».

---

### Comment un article est trié

**1. Est-il jeté d'office ?** Si le texte contient un mot de l'onglet
Exclusions, c'est fini.

**2. Quelle catégorie ?** Nomination (un verbe **et** un poste),
Ouverture, Événement, Tendance clientèle, ou Concurrent.
**Un article qui ne correspond à aucune catégorie est simplement ignoré** —
c'est le filtre principal, et la raison pour laquelle 600 articles lus
n'en donnent qu'une poignée.

**3. Quelle priorité ?** La ville est le critère central :

| | Condition |
|---|---|
| 🔴 | Nomination ou ouverture réelle, **confirmée dans le titre**, dans une zone prioritaire |
| 🟠 | Une ville suivie est reconnue |
| ⚪ | Le sujet est pertinent mais aucune ville n'est reconnue |

Pourquoi « confirmée dans le titre » : un article sur un hôtel à Rio peut
citer Paris au détour d'une phrase. Se fier au seul résumé produisait huit
fausses alertes rouges sur douze lors des tests. Pour les nominations et
les ouvertures uniquement, une ville citée dans le résumé suffit à passer
en 🟠 — parce que le titre dit souvent « Le Bristol nomme son nouveau
directeur général » sans préciser la ville.

**4. Qu'est-ce qui part, et quand ?**
Les 🔴 partent tout de suite, 5 au maximum par passage.
Les 🟠 et ⚪ attendent le résumé quotidien.
Un article n'est **jamais** envoyé deux fois.

---

### Le tout premier lancement

Certains flux contiennent 100 articles d'un coup. Pour éviter de te noyer,
**le premier `veille_presse.py` n'envoie rien** : il enregistre l'existant
et t'affiche dans le terminal ce qu'il aurait envoyé, pour que tu puisses
ajuster tes mots-clés. La veille démarre vraiment au lancement suivant.

---

### Les fichiers que le script gère seul

`memoire.json` retient les articles déjà envoyés et ceux en attente du
résumé. **Ne le modifie pas à la main.** Pour tout recommencer à zéro,
supprime-le : le prochain lancement repartira comme un premier lancement.

---

### Si quelque chose ne va pas

**Trop de notifications** → dans `mots-cles.xlsx`, retire des mots de
l'onglet Themes, ou ajoute des mots dans Exclusions. Ou passe une source
à `Actif = non` dans `sources.xlsx`.

**Pas assez** → ajoute des postes ou des thèmes, ou passe une ville à
`Prioritaire = oui` dans l'onglet Zones.

**« flux illisible »** sur une source → le site a changé d'adresse de flux.
Mets-la à `Actif = non` et signale-le moi.

**Une Google Alerte affiche « 0 articles lus »** → c'est normal, elle n'a
simplement rien trouvé de récent.

---

### Les 11 sources sans flux RSS

Ces sites n'exposent pas de flux exploitable. Il faut créer **3 Google
Alertes** groupées, puis coller leur lien RSS dans les 3 dernières lignes
de `sources.xlsx` (déjà préparées, `Actif = non` en attendant) :

**1. Presse hôtellerie FR**
```
site:journaldespalaces.com OR site:lhotellerie-restauration.fr OR site:tendancehotellerie.fr OR site:lechotouristique.com OR site:deplacementspros.com
```

**2. Luxe et voyage international**
```
site:fashionnetwork.com OR site:ttgasia.com OR site:elitetraveler.com
```

**3. Aviation, yachting et Maurice**
```
site:ainonline.com OR site:boatinternational.com OR site:lexpress.mu
```

Dans Google Alertes : « Diffuser vers » → **Flux RSS**, puis copier
l'adresse du flux.

---

## Étape 3 — Radar des événements ✅

### Les trois commandes

Toujours depuis le dossier `radar-unseen` :

```
./venv/bin/python radar_evenements.py --test
```
**Le mode réglage.** Affiche dans le terminal les rappels qui seraient
envoyés aujourd'hui, sans rien envoyer. À utiliser après chaque
modification d'`evenements.xlsx`.

```
./venv/bin/python radar_evenements.py
```
**Le vrai passage.** Envoie une alerte Telegram pour chaque événement qui
tombe pile à J-90, J-60, J-30 ou J-7 aujourd'hui. À lancer une fois par
jour.

```
./venv/bin/python radar_evenements.py --resume
```
**Le récapitulatif.** Envoie en un seul message la liste de tous les
événements actifs à venir, triés par date. À lancer le lundi matin.

Plus tard (étape 4), GitHub Actions lancera ces commandes tout seul.

### `evenements.xlsx` : c'est là que tu ajoutes tes événements

| Colonne | Contenu |
|---|---|
| Nom | Le nom de l'événement |
| Date | Le premier jour de l'événement (JJ/MM/AAAA, ou une vraie date Excel) |
| Ville | Optionnel |
| Catégorie | Optionnel (F1, Mode, Ski…), pas encore utilisé par le script mais utile pour t'y retrouver |
| Actif | `oui` / `non` — un événement passé ou annulé, tu le passes à `non` |

Un événement qui dure plusieurs jours (Fashion Week…) : mets la date du
premier jour, c'est sur elle que les rappels J-90/60/30/7 se calculent.

`memoire_evenements.json` retient ce qui a déjà été envoyé aujourd'hui,
pour ne jamais doubler un rappel si tu relances le script deux fois le
même jour. Ne le modifie pas à la main.

## Étape 4 — Automatisation GitHub Actions

À venir. **Point d'attention** : `sources.xlsx` contient les adresses de
tes flux Google Alertes, qui donnent accès à tes alertes sans mot de passe.
Le dépôt GitHub doit impérativement rester privé.
