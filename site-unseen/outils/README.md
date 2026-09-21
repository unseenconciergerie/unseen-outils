# Outils du site UNSEEN.

Deux petits programmes pour préparer les images du site. Tu n'as normalement
besoin de les relancer que si tu changes une photo.

## Ce qu'ils font

### 1. `images.py` — fabrique les images du site

Il part des photos d'origine en haute définition
(`Bureau/UNSEEN./photo unsplash`), les recadre au format exact où le site les
affiche, et enregistre chacune dans deux formats modernes :

- **AVIF** : le format que liront presque tous tes visiteurs. Deux à trois
  fois plus léger qu'un JPG à qualité identique.
- **WebP** : le filet de sécurité pour les navigateurs d'avant 2023.

Les JPG d'origine restent dans `img/`, mais le site ne s'en sert plus.

**Pour le lancer :**

```
python3 site-unseen/outils/images.py
```

Compte deux à trois minutes. Il affiche à la fin le poids gagné.

### 2. `brancher_images.py` — connecte le site aux nouvelles images

Il modifie `index.html` pour que chaque image soit servie en AVIF, avec le
WebP en secours. À ne lancer qu'une seule fois : s'il voit que c'est déjà
fait, il ne touche à rien.

```
python3 site-unseen/outils/brancher_images.py
```

## Changer une photo

1. Mets la nouvelle photo dans `Bureau/UNSEEN./photo unsplash`
2. Ouvre `images.py` et repère la ligne de l'image à changer dans le
   `CATALOGUE` (par exemple `"s-table"` pour la carte « Tables »)
3. Remplace le nom de fichier après `source=` par celui de ta nouvelle photo
4. Relance `python3 site-unseen/outils/images.py`

Si le recadrage automatique coupe mal, ajoute `centrage=(0.5, 0.3)` sur la
même ligne. Le premier chiffre déplace le cadrage de gauche (0) à droite (1),
le second de haut (0) en bas (1). Par défaut les deux valent 0.5, le centre.

## Important au moment de mettre en ligne

L'hébergement Infomaniak est limité à 10 Mo. **N'envoie pas les fichiers
`.jpg` du dossier `img/`**, le site ne les utilise plus et ils prendraient la
moitié de la place. Une seule exception : garde `hero.jpg`, qui sert d'image
d'aperçu quand quelqu'un partage le lien du site sur WhatsApp, LinkedIn ou
Facebook (ces services ne savent pas lire l'AVIF).

À envoyer dans `img/` : tous les `.avif`, tous les `.webp`, et `hero.jpg`.

## Si Pillow n'est pas installé

```
python3 -m pip install Pillow
```

Pillow est la bibliothèque qui sait lire et écrire les images. La version 12
ou plus récente est nécessaire pour l'AVIF.
