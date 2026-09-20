# Assistant de saisie prospects — UNSEEN.

Vous repérez un profil Instagram ou LinkedIn à la main, vous récupérez le
pseudo et l'email, et cet outil fait le reste :
1. Vérifie que ce prospect n'est pas déjà enregistré.
2. Ajoute une ligne dans un tableau Excel (dossier iCloud
   `UNSEEN - Prospection`).
3. Crée un brouillon Gmail personnalisé (anglais ou français), avec votre
   signature déjà intégrée, jamais envoyé automatiquement — vous le relisez
   et l'envoyez vous-même.

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
4. Répondre aux questions posées (pseudo, plateforme, email, prénom,
   langue EN/FR).
5. Aller dans Gmail, dossier Brouillons : le message est prêt, signature
   comprise. Le relire, vérifier l'adresse d'expéditeur, puis envoyer.

## Modifier les modèles d'email

Les textes des emails sont dans `modele_en.txt` et `modele_fr.txt`, à côté
de ce README. Modifiez-les directement avec un éditeur de texte — le
morceau `[Prénom]` sera automatiquement remplacé par le prénom du prospect
(ou "there" / "vous" si vous n'avez pas de prénom).

L'objet du mail ("Europe by UNSEEN.") et les adresses d'expéditeur
(`contact@unseenconciergerie.com` en anglais,
`contact@unseenconciergerie.fr` en français) sont réglés dans `gmail.py`.

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
- `excel.py` — gestion du tableau Excel (doublons, ajout de ligne).
- `gmail.py` — connexion à Gmail et création du brouillon.
- `modele_en.txt` / `modele_fr.txt` — textes des emails, modifiables.
- `signature.html` / `logo_signature.png` — copie de votre signature Gmail.
- `.env` — vos identifiants Gmail (jamais sur Git).
