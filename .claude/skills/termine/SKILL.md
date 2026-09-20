---
name: termine
description: Routine de fin de session. Se déclenche quand Jay dit « on termine » — met à jour ETAT-DU-PROJET.md (version courte) et contexte/historique-projet.md (détail) et change la date de mise à jour.
---

# Fin de session

`ETAT-DU-PROJET.md` est chargé à chaque début de session : il doit rester
court (une vingtaine de lignes maximum). Le détail va dans
`contexte/historique-projet.md`, qui n'est lu qu'à la demande.

Quand Jay dit « on termine » :

1. Dans `ETAT-DU-PROJET.md`, mets à jour seulement :
   - le statut en une ligne par outil (section « Outils »),
   - la prochaine étape.
   Pas de liste de décisions ni de détails ici — si le fichier dépasse
   une vingtaine de lignes, coupe et déplace vers historique-projet.md.

2. Dans `contexte/historique-projet.md`, ajoute :
   - ce qui a été fait pendant la session (détail),
   - les décisions prises et leur raison,
   - ce qui reste en cours côté Jay.

3. Change la date de mise à jour en haut d'`ETAT-DU-PROJET.md`.

4. Ne modifie jamais un fichier du dossier `contexte/` sans proposer le
   changement à Jay d'abord.
