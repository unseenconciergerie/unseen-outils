# Outils internes UNSEEN.

Projet : outils internes (veilles, prospection, documents) pour UNSEEN.,
conciergerie privée de luxe à Paris, fondée par Jay Pandea.

## Contexte chargé à chaque session
@contexte/entreprise.md
@ETAT-DU-PROJET.md

## Contexte à lire selon la tâche
- Prospection, messages, veilles LinkedIn, partenaires : lis d'abord
  contexte/prospection-et-canaux.md et contexte/reseau-partenaires.md.
- Documents clients, propositions, site internet, visuels : lis d'abord
  contexte/marque-et-site.md.
- Pour une tâche purement technique, ne lis pas ces fichiers inutilement.

## Mon niveau technique
Je ne suis pas développeur. Explique chaque étape simplement, en français,
et dis-moi exactement quoi taper ou sur quoi cliquer.

## Guidage pas à pas
- Quand une action doit être faite par moi hors de VS Code (Telegram, Google,
  réglages du Mac, Excel, GitHub) : donne-moi une seule étape à la fois — où
  cliquer, quoi taper, ce que je dois voir à l'écran. Attends que je réponde
  « ok », ou que je colle une capture ou une erreur, avant de passer à la
  suite.
- Quand je colle une capture ou une erreur : dis-moi d'abord ce que tu vois,
  puis la correction.

## Règles de travail
- Toujours me proposer un plan avant de coder, et attendre ma validation.
- Python le plus simple possible, commenté en français.
- Un sous-dossier par outil, chacun avec un README expliquant comment le lancer.
- Jamais de mot de passe, token ou clé API dans le code : fichier .env,
  ajouté au .gitignore.
- Me demander avant d'installer un logiciel ou une bibliothèque.
- Aucune automatisation d'actions sur LinkedIn ou Instagram (ni scraping,
  ni envoi automatique de messages) : uniquement API officielles,
  flux RSS et pages publiques.
- Les données clients sont confidentielles : jamais envoyées vers un
  service tiers sans mon accord explicite.
- Le dossier contexte/ est confidentiel : il ne doit jamais être envoyé
  sur GitHub ni sur un service en ligne. L'ajouter au .gitignore dès
  qu'un dépôt Git est créé.
- Aucun contenu destiné à un client ou au public ne détaille la structure
  de facturation interne (débours, commissions, marges) : le client voit
  un prix. Pour les factures, me demander avant de fixer la présentation.

## Règles de prospection (pour les messages rédigés)
- Français pour les contacts français ou mauriciens, anglais pour les
  sièges internationaux.
- Une seule demande par message, court et direct.
- Aucune mention de commission ou de facturation au premier contact.

## Canaux
- Notifications : bot Telegram (token et chat_id dans .env).
- CRM : fichier Excel UNSEEN_Prospection_Mail_CRM.xlsx.

## Fin de session
Quand je dis « on termine », utilise la skill /termine.
