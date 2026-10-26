---
name: verifier-mobile
description: Vérifie le site UNSEEN. comme sur un iPhone avec Safari, avant et après chaque mise en ligne. Se déclenche quand Jay dit « on publie », « vérifie le site sur téléphone », « regarde sur iPhone », ou avant tout push qui touche site-unseen/.
---

# Vérifier le site sur iPhone (Safari)

La plupart des visiteurs d'UNSEEN. sont sur **Safari, sur iPhone**. Une page qui marche
dans Firefox peut casser dans Safari (moteur WebKit). On vérifie donc dans le vrai Safari
du Mac, dans une fenêtre de la largeur d'un iPhone (390 points).

## 1. Lancer les captures Safari

Le pilote de Safari est intégré à macOS (activé une fois par Jay le 26/10/2026 avec
`safaridriver --enable`).

1. Claude démarre le pilote : `(safaridriver -p 4447 > /tmp/sd.log 2>&1 &); sleep 3`.
   Si le journal dit « Unable to start the server: Operation not permitted », un verrou est
   resté après une session mal fermée : seul un redémarrage du Mac le libère (constaté le 26/10).
2. Claude lance, depuis le dossier du projet :
   `assistant-prospection/venv/bin/python site-unseen/outils/verifier_safari.py "en ligne" <dossier du scratchpad>`
   (ou `local` pour tester avant la mise en ligne ; ajouter des noms de pages pour n'en tester que certaines).
3. Lire chaque planche (une par page), puis arrêter le pilote : `pkill -f "safaridriver -p 4447"`.

Si le pilote ne peut pas être lancé : captures Firefox à 390 px de large en dépannage,
en le disant à Jay (Firefox ne voit pas tous les bugs de Safari).

## 2. Ce qu'il faut regarder sur chaque page

- **Aucune zone vide** : un bloc qui apparaît « en douceur » peut rester invisible sur iPhone.
  Sous 900 px, `.rv` et `.reveal` doivent être visibles d'office.
- **Pas de grands trous** entre deux lignes d'une liste (piège : `flex-basis` qui s'applique
  en colonne sur téléphone).
- **Tout ensemble de plusieurs éléments défile de gauche à droite** (cartes, catégories,
  adresses, services), avec la carte suivante qui dépasse un peu, et `scroll-padding-left`
  pour s'arrêter sur la marge. Jay ne veut pas de longues listes verticales.
- **Haut de page** : texte lisible sur la photo (voile assez sombre), titres pas trop grands
  en français (les phrases françaises sont plus longues).
- **Menu trois traits** qui s'ouvre, boutons pleine largeur, bouton WhatsApp qui ne cache rien d'important.
- **Bandeau des partenaires** : défile sans s'arrêter, ne réagit pas au toucher, ni trop lent ni trop rapide.
- **Trois langues** : passer en FR et en 中文 et vérifier que rien ne déborde.
- **Une photo n'apparaît que sur une seule page** du site.

## 3. Après la mise en ligne

- Attendre que la nouvelle version soit en ligne (en général 30 s à 1 min après le push).
- Refaire les captures en mode `en ligne`.
- Dire à Jay de recharger sur son iPhone (fermer l'onglet si l'ancienne version reste affichée).
