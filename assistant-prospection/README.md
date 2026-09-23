# Assistant de saisie prospects — UNSEEN.

Vous repérez un profil Instagram ou LinkedIn à la main, vous récupérez le
pseudo et l'email, et cet outil fait le reste :
1. Vérifie que ce prospect n'est pas déjà enregistré.
2. Ajoute une ligne dans un tableau Excel (dossier iCloud
   `UNSEEN - Prospection`).
3. Crée un brouillon Gmail personnalisé (anglais, français ou chinois),
   avec votre signature déjà intégrée, jamais envoyé automatiquement —
   vous le relisez et l'envoyez vous-même.

Trois types de contact, avec un modèle d'email différent pour chacun :
- **Client** : un prospect repéré sur Instagram/LinkedIn (créateur, voyageur).
- **Agence** : l'adresse est celle d'une agence de talents, d'un manager ou
  d'une équipe PR (`talent@`, `mgmt@`, `team@`, `bookings@`...). Le mail
  s'adresse à l'équipe et parle de « vos talents », sans supposer que la
  personne lue est le créateur lui-même.
- **Partenaire** : un tour-opérateur, une agence, un guide ou un DMC à qui
  on propose de devenir une source de signalement (avec commission),
  repéré par exemple via la veille de `radar-unseen/` (catégorie
  Tour-opérateur).

Aucune connexion ni lecture automatisée d'Instagram ou LinkedIn : c'est
vous qui repérez les profils.

## Installation (une seule fois)

1. Ouvrir le Terminal dans ce dossier (`assistant-prospection/`).
2. Activer l'environnement Python dédié :
   ```
   source venv/bin/activate
   ```
3. Les bibliothèques sont déjà installées. Si besoin de les réinstaller :
   ```
   pip install -r requirements.txt
   ```

## Configurer l'accès à Gmail (une seule fois)

L'outil se connecte à votre boîte Gmail UNSEEN. (`contact.me.unseen@gmail.com`,
celle sur laquelle sont branchés vos alias `@unseenconciergerie.fr/.com`)
avec un **mot de passe d'application** — un mot de passe spécial, différent
de votre mot de passe Google habituel, que vous pouvez révoquer à tout
moment sans toucher au reste de votre compte.

1. Va sur https://myaccount.google.com/apppasswords, connecté avec le
   compte `contact.me.unseen@gmail.com`. Si la validation en 2 étapes n'est
   pas encore activée sur ce compte, Google te demandera de l'activer
   d'abord — dis-le moi si tu bloques à cette étape.
2. Donne un nom à ce mot de passe, par exemple "Assistant prospection
   UNSEEN.", et clique sur Créer.
3. Google affiche un mot de passe de 16 caractères. Copie-le.
4. Ouvre le fichier `.env` dans ce dossier et complète les deux lignes :
   ```
   GMAIL_ADRESSE=contact.me.unseen@gmail.com
   GMAIL_MOT_DE_PASSE_APPLICATION=le-mot-de-passe-copié
   ```
5. Enregistre le fichier `.env`. Ce fichier n'est jamais envoyé sur Git
   (il est dans `.gitignore`).

## Utilisation au quotidien

1. Ouvrir le Terminal dans ce dossier.
2. Activer l'environnement (si ce n'est pas déjà fait) :
   ```
   source venv/bin/activate
   ```
3. Lancer l'outil :
   ```
   python3 ajouter_prospect.py
   ```
4. Répondre aux questions posées : type de contact (client/partenaire/agence),
   pseudo, plateforme, email, prénom, langue (EN/FR/ZH).
5. Aller dans Gmail, dossier Brouillons : le message est prêt, signature
   comprise. Le relire, vérifier l'adresse d'expéditeur, puis envoyer.

⚠️ **Langue ZH (chinois)** : le script affiche un rappel dans le
terminal, mais c'est à vous de faire relire le brouillon par un locuteur
natif avant de l'envoyer — même règle que pour le site et Xiaohongshu.

## Traiter plusieurs contacts d'un coup

Si vous avez une liste de contacts (par exemple retranscrite depuis des
captures d'écran), pas besoin de repasser par les questions une par une :

1. Ouvrez `a_traiter.xlsx` (à côté de ce README). Une ligne par contact,
   colonnes : **Type** (`client`, `partenaire` ou `agence`), **Pseudo**,
   **Plateforme**, **Email**, **Prénom** (laisser vide si inconnu, le
   mail commencera alors par « Dear Team » / « Bonjour toute l'équipe »),
   **Langue** (`EN`, `FR` ou `ZH`; `ZH` n'existe pas pour le type agence).
2. Enregistrez le fichier.
3. Lancez :
   ```
   python3 ajouter_prospect.py --fichier a_traiter.xlsx
   ```
4. Un brouillon Gmail est créé pour chaque ligne valide. Les doublons
   (déjà dans le tableau de suivi) sont ignorés automatiquement, les
   lignes avec un email ou une langue manquante aussi — le résumé à la
   fin indique combien de chaque.
5. Repassez ensuite dans Gmail pour relire chaque brouillon avant d'envoyer.

Vous pouvez me demander de remplir `a_traiter.xlsx` pour vous à partir de
captures d'écran (Instagram, LinkedIn...) : mettez-les dans un dossier et
donnez-moi le chemin, je les lis et je remplis le tableau, sans que vous
ayez à retaper quoi que ce soit.

## Modifier les modèles d'email

Les textes sont dans `modele_en.txt` / `modele_fr.txt` / `modele_zh.txt`
(prospects clients), `modele_partenariat_en.txt` /
`modele_partenariat_fr.txt` / `modele_partenariat_zh.txt` (partenaires) et
`modele_agence_en.txt` / `modele_agence_fr.txt` (agences et managers),
à côté de ce README. Modifiez-les directement avec un éditeur de texte —
le morceau `[Prénom]` sera automatiquement remplacé par le prénom du
contact (ou "Team" / "toute l'équipe" / "您" si vous n'avez pas de prénom).

Les adresses d'expéditeur (`contact@unseenconciergerie.com` en anglais et
en chinois, `contact@unseenconciergerie.fr` en français) et les objets de
mail ("Europe by UNSEEN." pour un client, "Partenariat UNSEEN. — Paris"
pour un partenaire, "Paris, by UNSEEN." pour une agence) sont réglés dans
`gmail.py`.

## La signature

`signature.html` et `logo_signature.png` sont une copie exacte de votre
signature Gmail (texte + logo), récupérée une fois pour toutes et ajoutée
automatiquement à chaque brouillon. Si vous modifiez votre signature dans
les réglages Gmail, il faudra refaire cette copie une fois (demandez-moi,
c'est rapide) pour que les brouillons restent à jour.

## Où est le tableau de suivi ?

`/Users/jaypandea/Documents/UNSEEN - Prospection/prospects.xlsx`
(dans votre dossier Documents, synchronisé automatiquement avec iCloud).

## Fichiers

- `ajouter_prospect.py` — le script à lancer.
- `a_traiter.xlsx` — pour traiter plusieurs contacts d'un coup (voir plus haut).
- `excel.py` — gestion du tableau Excel (doublons, ajout de ligne).
- `gmail.py` — connexion à Gmail et création du brouillon.
- `modele_en.txt` / `modele_fr.txt` / `modele_zh.txt` — emails pour un
  prospect client.
- `modele_partenariat_en.txt` / `modele_partenariat_fr.txt` /
  `modele_partenariat_zh.txt` — emails pour proposer un partenariat
  (tour-opérateur, agence, guide, DMC).
- `modele_agence_en.txt` / `modele_agence_fr.txt` — emails pour une agence
  de talents, un manager ou une équipe PR.
- `signature.html` / `logo_signature.png` — copie de votre signature Gmail.
- `.env` — vos identifiants Gmail (jamais sur Git).
