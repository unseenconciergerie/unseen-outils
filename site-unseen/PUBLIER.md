# Mettre le site en ligne

Cette fiche explique comment une modification du site arrive sur
unseenconciergerie.com. Elle remplace l'ancienne fiche « Infomaniak »
(octobre 2026) : le site n'est plus déposé à la main sur Infomaniak.

## Comment ça marche, en une phrase

Quand Claude envoie le dossier `site-unseen` sur GitHub (ce qu'on appelle
un « push »), GitHub met le site à jour tout seul en une à deux minutes.
Tu n'as rien à faire toi-même, ni FTP ni Web FTP.

## Ce que tu dis à Claude

- **« On publie »** : Claude envoie les changements sur GitHub, puis vérifie
  que le site en ligne a bien changé.
- Claude ne publie jamais sans ton « ok ». Tant que tu n'as rien dit, les
  pages restent seulement sur ton Mac (tu les vois en les ouvrant dans
  Firefox), et le site en ligne ne bouge pas.

## Après la mise en ligne, vérifie (ou demande à Claude de vérifier)

1. **Sur ton iPhone**, en 4G plutôt qu'en wifi : ouvre unseenconciergerie.com,
   le menu à trois traits, et une page de destination.
2. **Les trois langues** : bouton EN / FR / 中文 en haut à droite.
3. **Une adresse fausse** (par exemple `unseenconciergerie.com/xyz`) : tu dois
   voir la page d'erreur UNSEEN.
4. Si quelque chose cloche, fais une capture et montre-la à Claude. On peut
   toujours revenir à la version précédente en quelques secondes.

## Ce qui part en ligne, et ce qui reste sur ton Mac

- **En ligne** : toutes les pages (`.html`), les photos (`img/`), les couleurs
  de saison (`season.css`), les animations et les icônes.
- **Jamais en ligne** : le dossier `outils/` (les programmes qui fabriquent les
  images et les pages) et cette fiche. GitHub les retire automatiquement
  avant chaque publication.

## Changer la couleur de saison

C'est le fichier `season.css`. Demande simplement à Claude, par exemple
« passe le site en Abricot pour l'été », puis « on publie ».

## Les pages du site (octobre 2026)

| Page | Fichier |
|---|---|
| Accueil | `index.html` |
| Professionnels | `professionals.html` |
| Paris | `paris.html` |
| Riviera | `riviera.html` |
| Océan Indien | `ocean-indien.html` |
| Alpes, saison de ski | `saison-ski-2026-2027.html` |
| Grand Prix de Formule 1 | `formule-1.html` |
| Mentions légales | `legal.html` |
| Page d'erreur | `404.html` |

## Pour Claude (détail technique)

- Publication : workflow `.github/workflows/pages.yml`, déclenché par un push
  sur `main` qui touche `site-unseen/**`. Domaine : unseenconciergerie.com.
- Le fichier `.htaccess` ne sert plus (il était pour Infomaniak) ; GitHub Pages
  sert `404.html` tout seul.
- Photos : `outils/images_v14.py` fabrique les `.avif` et `.webp` depuis les
  originaux rangés dans `~/Documents/UNSEEN./`. Une photo ne sert que sur une
  seule page du site.
