# Mettre le site en ligne sur Infomaniak

Tout ce qu'il faut envoyer, et ce qu'il ne faut surtout pas envoyer.

## Avant de commencer

L'espace Infomaniak est limité à **10 Mo** et il est aujourd'hui plein avec
l'ancien site. **Supprime d'abord l'ancien contenu du dossier `web`**, sinon
l'envoi échouera à mi-chemin.

Le nouveau site pèse **4,06 Mo**, il restera donc environ 6 Mo libres.

## Ce qu'il faut envoyer

### À la racine du dossier `web` (11 fichiers)

```
index.html          la page principale
legal.html          les mentions légales
404.html            la page affichée quand une adresse n'existe pas
season.css          la couleur de saison
anim.css            les animations
anim.js             les animations (partie JavaScript)
favicon.svg         l'icône de l'onglet
apple-touch-icon.png  l'icône si le site est ajouté à un écran d'accueil iPhone
robots.txt          les consignes pour Google
sitemap.xml         la liste des pages, pour Google
.htaccess           les réglages du serveur
```

### Dans le sous-dossier `img`

- **tous les fichiers `.avif`** (33)
- **tous les fichiers `.webp`** (33)
- **`hero.jpg`**, et lui seul parmi les JPG

## Ce qu'il ne faut PAS envoyer

- **Les 23 autres fichiers `.jpg` du dossier `img`.** Le site ne s'en sert
  plus. Ils pèsent 4,7 Mo, soit la moitié de ton espace, pour rien.
- **Le dossier `outils`.** Ce sont les programmes qui fabriquent les images,
  ils tournent sur ton Mac et n'ont rien à faire en ligne.

## Deux pièges à connaître

### Le fichier `.htaccess` est invisible dans le Finder

Son nom commence par un point, le Mac le cache. Pour le faire apparaître :
**Cmd + Maj + point** dans la fenêtre du Finder. La même combinaison le
recache ensuite.

C'est le fichier le plus important de la liste. Sans lui, le serveur ne
reconnaît pas le format AVIF et **aucune photo du site ne s'affiche**.

### `hero.jpg` doit rester

C'est l'image d'aperçu quand quelqu'un partage le lien du site sur WhatsApp,
LinkedIn ou par message. Ces services ne savent pas lire l'AVIF.

## Après la mise en ligne

Vérifie dans cet ordre :

1. **Les photos s'affichent.** Si tout est gris ou vide, c'est le `.htaccess`
   qui n'est pas arrivé, ou qui est au mauvais endroit.
2. **Tape une adresse fausse** (par exemple `unseenconciergerie.com/xyz`) :
   tu dois voir la page noire UNSEEN., pas celle d'Infomaniak.
3. **Ouvre `unseenconciergerie.fr`** : tu dois arriver sur l'adresse en `.com`.
4. **Ouvre le site sur ton téléphone**, en 4G plutôt qu'en wifi.

Si quelque chose cloche, fais une capture et montre-la moi.

## Si les images ne s'affichent pas

C'est presque toujours le `.htaccess`. Dans l'ordre :

1. Vérifie qu'il est bien à la racine du dossier `web`, à côté d'`index.html`
2. Vérifie que son nom est exactement `.htaccess`, avec le point devant, et
   sans extension ajoutée du genre `.htaccess.txt`
3. Si le problème persiste, Infomaniak propose un réglage des types de
   fichiers dans son interface : dis-le moi, on le fera autrement

## Si le site se met à tourner en boucle

Symptôme : le navigateur affiche « trop de redirections ».

Ouvre `.htaccess`, trouve le bloc **3. L'adresse de référence du site**, et
mets un `#` devant les quatre lignes qui commencent par `Rewrite`. Renvoie le
fichier. Le site refonctionne aussitôt, et on cherchera ensuite.

Cela n'affecte jamais tes boîtes mail : le courrier et le site web empruntent
deux chemins séparés.
