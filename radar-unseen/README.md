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

### Repérer des tour-opérateurs/agences Chine-Asie (catégorie Tour-opérateur)

Six lignes sont déjà préparées dans `sources.xlsx` (`Actif = non` en
attendant), avec une colonne Note qui donne la recherche à coller dans
Google Alertes :

**1. Tour-opérateurs Chine-Asie vers Paris**
```
(tour operator OR agence de voyage OR DMC OR voyagiste) (Paris OR France) (partenariat OR "nouveau programme" OR bureau)
```

**2. Tourisme chinois France, tendance**
```
tourisme chinois (Paris OR France) (croissance OR reprise OR vols OR visa)
```

**3. Agences Moyen-Orient vers Paris**
```
(tour operator OR agence de voyage OR DMC) (Dubai OR "Abu Dhabi" OR Riyadh OR Qatar OR Golfe) (Paris OR France) (partenariat OR programme)
```

**4. Guides shopping Paris**
```
(guide OR "personal shopping" OR "shopping tour") Paris ("Galeries Lafayette" OR luxe OR "duty free" OR detaxe)
```

**5. Vols et visas Chine-Golfe vers France**
```
("vol direct" OR "direct flight" OR visa) (Chine OR China OR Golfe OR Gulf) France (Paris OR touristes OR voyageurs)
```

**6. Tour-opérateurs Inde vers Paris**
```
(tour operator OR agence de voyage OR DMC) India (Paris OR France) (partenariat OR "nouveau programme" OR bureau)
```

Même procédure que les autres alertes : crée l'alerte sur
[google.com/alerts](https://www.google.com/alerts), « Diffuser vers » →
**Flux RSS**, colle l'adresse dans la colonne « URL du flux », puis passe
`Actif` à `oui`.

**Limite à garder en tête** : cette veille repère des *entreprises*
(tour-opérateurs, agences) qui annoncent un développement sur Paris — pas
des clients individuels. Aucune veille presse ne peut détecter qu'une
famille précise arrive à Paris, ce n'est jamais public. Pour ça, voir
l'Étape 5 ci-dessous : une fois qu'un de ces tour-opérateurs devient un
partenaire (via `assistant-prospection/`), c'est lui qui te préviendra.

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

---

## Étape 5 — Carnet de groupes annoncés

### À quoi ça sert

Quand un partenaire (guide, chauffeur, DMC, hôtel) te prévient qu'un
groupe ou une famille arrive à Paris, tu envoies un message Telegram au
bot avec ce qu'on t'a dit, en texte libre — pas de formulaire à remplir.
Le script range l'info dans une base Notion, et t'envoie un rappel groupé
avant l'arrivée du groupe (J-30, J-14, J-3) pour que tu le contactes avant
qu'il soit sur place.

**Important à comprendre** : cet outil ne trouve pas de clients tout seul.
Il range et te rappelle ce qu'un partenaire t'a déjà signalé. La vraie
source, ce sont tes partenariats (voir Étape « Repérer des
tour-opérateurs » ci-dessus, et `assistant-prospection/` pour les
approcher avec une proposition de commission).

### Les commandes

Toujours depuis le dossier `radar-unseen` :

```
./venv/bin/python radar_groupes.py --recevoir --test
```
Affiche les nouveaux messages Telegram trouvés, sans rien créer dans
Notion.

```
./venv/bin/python radar_groupes.py --recevoir
```
Crée une fiche Notion « À compléter » pour chaque nouveau message
Telegram envoyé au bot depuis le dernier passage.

```
./venv/bin/python radar_groupes.py --rappels
```
Envoie **un seul message Telegram groupé** avec tous les groupes qui
tombent pile à J-30, J-14 ou J-3 aujourd'hui. À lancer une fois par jour.

```
./venv/bin/python radar_groupes.py --nouveaux
```
Récapitulatif hebdomadaire des groupes ajoutés dans les 7 derniers jours
et pas encore contactés — pour ne rien perdre entre le signalement et
l'action.

Ajoute `--test` à n'importe laquelle de ces commandes pour voir le
résultat dans le terminal sans rien envoyer ni enregistrer.

⚠️ **Ce fichier de suivi contient des données clients.** Contrairement à
la veille presse et au calendrier événements, il n'y a **pas
d'automatisation GitHub Actions** pour cet outil : tu lances ces
commandes toi-même depuis ton Mac.

### La base Notion « Groupes UNSEEN. »

Ouvre-la ici : https://app.notion.com/p/d208b64f9aac494a80a96f25f4600f4d

| Colonne | Qui la remplit | Contenu |
|---|---|---|
| Nom du groupe / client | Le script (1re ligne du message) | Libre |
| Notes | Le script | Le texte brut du message Telegram |
| Date d'arrivée | Toi | JJ/MM/AAAA — déclenche les rappels |
| Date de départ | Toi | Optionnel |
| Nationalité / zone | Toi | Libre |
| Taille du groupe | Toi | Libre |
| Signalé par | Toi | Qui t'a prévenu |
| Contact partenaire | Toi | Téléphone/email du partenaire |
| Contact direct client | Toi | Si le partenaire l'a partagé |
| Statut | Toi | À compléter → À contacter → Contacté → Rendez-vous pris / Sans suite |

Le script ne touche jamais au Statut après la création de la fiche —
c'est toi qui le mets à jour dans Notion au fur et à mesure.

**Bon réflexe** : dès qu'un partenaire te signale un groupe, même une
info incomplète (juste une date et une nationalité), envoie-la tout de
suite au bot Telegram. Tu complèteras dans Notion plus tard. Mieux vaut
un rappel imparfait qu'aucun rappel.

`memoire_groupes.json` retient le dernier message Telegram lu et les
rappels déjà envoyés aujourd'hui. Ne le modifie pas à la main.
