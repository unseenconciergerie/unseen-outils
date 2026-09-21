# État du projet — Outils internes UNSEEN.

Dernière mise à jour : 22 septembre 2026

Détail complet (décisions passées, réglages recommandés, feuille de route
entière) : voir `contexte/historique-projet.md`, à lire seulement si besoin.

## Outils
- **Radar UNSEEN.** (`radar-unseen/`) — veille presse, nominations et
  calendrier → Telegram. Automatisé sur GitHub Actions, rien à lancer.
- **Assistant de prospection** (`assistant-prospection/`) — prospects →
  Excel iCloud + brouillon Gmail signé. Fait et testé.
- **Site web** (`site-unseen/`) — photos AVIF/WebP, ouverture plein écran,
  animations, carte illustrée, page 404. Dépôt public poussé sur GitHub
  (`unseenconciergerie/site`), Pages activé, **et déjà vérifié : répond
  en 0,3 s** (contre 9-16 s chez Infomaniak). Adresse technique en place
  (`unseenconciergerie.github.io/site`, redirige vers le `.com`).
  **Il ne reste qu'une étape : changer le DNS chez Infomaniak.**

## Prochaine étape
Chez Infomaniak (manager.infomaniak.com → domaine
unseenconciergerie.com → Zone DNS) : changer **uniquement** les lignes
`A` de la racine et de `www` pour pointer vers GitHub Pages.
**Ne jamais toucher aux lignes MX ni TXT/SPF : ce sont les mails.**
Avant de modifier quoi que ce soit, faire confirmer par Jay une capture
de la liste complète de la zone DNS, pour repérer les bonnes lignes.
Réversible en remettant `128.65.195.180` sur les deux lignes `A`.

Ensuite : relances CRM, tableau de bord hebdo, générateur de propositions
PDF.
