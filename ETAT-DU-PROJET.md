# État du projet — Outils internes UNSEEN.

Dernière mise à jour : 21 septembre 2026 (soir)

Détail complet (décisions passées, réglages recommandés, feuille de route
entière) : voir `contexte/historique-projet.md`, à lire seulement si besoin.

## Outils
- **Radar UNSEEN.** (`radar-unseen/`) — veille presse, nominations et
  calendrier → Telegram. Automatisé sur GitHub Actions, rien à lancer.
- **Assistant de prospection** (`assistant-prospection/`) — prospects →
  Excel iCloud + brouillon Gmail signé. Fait et testé.
- **Site web** (`site-unseen/`) — **en ligne sur unseenconciergerie.com**.
  Photos AVIF/WebP, ouverture plein écran, animations, carte illustrée,
  page 404. 4,06 Mo sur 10. Outils dans `site-unseen/outils/`, marche à
  suivre dans `site-unseen/PUBLIER.md`.
  **Bloquant : l'hébergement Starter répond en 9 à 16 s et échoue une
  fois sur deux.** Le site est bon, le serveur ne le livre pas.

## Prochaine étape
Déplacer le site sur **GitHub Pages** (gratuit). Le dépôt local est prêt
et commité dans `~/Documents/UNSEEN-site-public` (81 fichiers). Reste à :
créer le dépôt public `unseenconciergerie/site` sur github.com (vide,
sans README), pousser, activer Pages, puis chez Infomaniak ne changer que
les lignes `A` de `unseenconciergerie.com` et de `www`.
**Ne jamais toucher aux lignes MX ni SPF : ce sont les mails.**

Ensuite : relances CRM, tableau de bord hebdo, générateur de propositions
PDF.
