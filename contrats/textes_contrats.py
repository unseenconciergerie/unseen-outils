"""
Textes des contrats UNSEEN. (anglais et français).

Chaque contrat est une liste de "blocs". Un bloc = (type, contenu) :
- "titre" / "sous"  : titre du document et sous-titre
- "h"               : titre d'article
- "p"               : paragraphe (les **mots** entre doubles étoiles sont en gras)
- "li"              : élément de liste à puce
- "tableau"         : liste de lignes [libellé, valeur]
- "signatures"      : bloc de signature à deux colonnes
- "saut"            : saut de page
- "note"            : petit texte en italique

Les informations propres à chaque client (nom, adresse, dates...) arrivent
dans le dictionnaire `i`. Tout ce qui est encore inconnu est écrit entre
[[doubles crochets]] : le générateur le surligne en jaune pour qu'on voie
tout de suite ce qu'il reste à compléter avant la signature.

Règles respectées dans ces textes (voir l'historique du projet) :
- jamais le nom du partenaire qui obtient les rendez-vous (l'accord de
  confidentialité signé avec lui rend l'identité des partenaires confidentielle) ;
- jamais de sac garanti ;
- aucun détail de la facturation interne (le client voit un prix) ;
- pas de tiret long dans la prose.
"""

UNSEEN_EN = (
    "**UNSEEN.**, trading name of Mr Jay Pandea, sole trader (entrepreneur individuel) "
    "under the French micro-enterprise regime, SIREN 999 356 587, SIRET 999 356 587 00017, "
    "registered office at 8 rue du Docteur Gravery, 77100 Meaux, France, "
    "contact@unseenconciergerie.com, represented by Jay Pandea, Founder (\"**UNSEEN.**\")"
)
UNSEEN_FR = (
    "**UNSEEN.**, nom commercial de M. Jay Pandea, entrepreneur individuel relevant du "
    "régime de la micro-entreprise, SIREN 999 356 587, SIRET 999 356 587 00017, dont le "
    "siège est situé 8 rue du Docteur Gravery, 77100 Meaux, France, "
    "contact@unseenconciergerie.com, représenté par Jay Pandea, fondateur (« **UNSEEN.** »)"
)


# ---------------------------------------------------------------------------
# 1. ACCORD DE PARTENARIAT ET D'APPORT D'AFFAIRES (Mayank)
# ---------------------------------------------------------------------------

def partenariat_en(i):
    """Version anglaise de l'accord de partenariat (version de lecture)."""
    return [
        ("titre", "PARTNERSHIP AND REFERRAL AGREEMENT"),
        ("sous", "English version, provided for convenience. The French version below prevails."),
        ("h", "Between"),
        ("p", UNSEEN_EN + ","),
        ("p", "and"),
        ("p", f"**{i['nom_usage']}**, {i['profession']}, "
              f"residing at {i['adresse']}, {i['email']} (the \"**Partner**\")."),
        ("p", "Together the \"Parties\"."),

        ("h", "Background"),
        ("p", "UNSEEN. is a private concierge service based in Paris. The Partner is a content "
              "creator in the luxury field (Instagram @shopaholique6, TikTok @mayankbhatter) and "
              "may recommend UNSEEN. to the Partner's audience and contacts. This Agreement sets out a simple "
              "referral arrangement. It replaces all prior discussions and drafts between the "
              "Parties on this subject."),

        ("h", "Article 1. Purpose"),
        ("p", "This Agreement defines the referral code, the benefit offered to the clients the "
              "Partner refers, the Partner's commission and the obligations of each Party. The "
              "services the Partner books for the Partner's own use are governed by their own booking agreements."),

        ("h", "Article 2. Referral code and Referred Clients"),
        ("p", "2.1. UNSEEN. assigns the Partner a unique referral code within seven (7) days of "
              "signature."),
        ("p", "2.2. A \"**Referred Client**\" is a person who (a) contacts UNSEEN. for the first time "
              "using the code, or whom the Partner introduced to UNSEEN. in writing before that first "
              "contact, (b) had no prior business relationship with UNSEEN., and (c) signs and pays "
              "at least one request after the signature of this Agreement."),
        ("p", "2.3. UNSEEN.'s written records are the reference. The Partner may at any time ask "
              "UNSEEN. to confirm whether a person the Partner introduced is a Referred Client."),

        ("h", "Article 3. Benefit offered to Referred Clients"),
        ("p", "3.1. Each Referred Client receives **50% off UNSEEN.'s Service Fee on their first two "
              "(2) requests** (\"Service Fee\" is defined in Article 4.1)."),
        ("p", "3.2. The benefit applies once per Referred Client, to the Service Fee only, never to "
              "supplier costs. It cannot be combined with any other offer and is not a permanent "
              "discount."),
        ("p", "3.3. UNSEEN. does not raise its fees to offset the benefit. The Partner presents the "
              "benefit only as described in this Article and never against an inflated reference "
              "price."),

        ("h", "Article 4. Commission"),
        ("p", "4.1. \"**Service Fee**\" means the fee UNSEEN. charges for its own work on a request, "
              "shown as such on its quote or invoice, excluding any supplier cost and any amount "
              "passed on to a third party."),
        ("p", "4.2. For each Referred Client, the Partner receives a commission of **ten percent "
              "(10%) of the Service Fee actually invoiced and received by UNSEEN.**, after any "
              "discount, on the requests accepted during the six (6) months following that client's "
              "first signed request."),
        ("p", "4.3. The commission is never calculated on the total invoiced, on supplier costs, on "
              "goods purchased by the client or on amounts passed through. Example: on a request "
              "with a Service Fee of EUR 700, the commission is EUR 70, whatever the total invoiced. "
              "Where the 50% benefit applies, the Service Fee is EUR 350 and the commission EUR 35."),
        ("p", "4.4. Some services are sold at a fixed, all-inclusive price, with no separate "
              "Service Fee (for example a private maison appointment). For those, UNSEEN. states in "
              "its quote whether and how Articles 3 and 4 apply. Failing such a statement, they do "
              "not apply."),
        ("p", "4.5. No commission and no benefit apply to requests made by or for the Partner, or "
              "for persons travelling with the Partner or booked at the Partner's request, unless UNSEEN. agrees "
              "otherwise in writing."),
        ("p", "4.6. Requests accepted before the signature of this Agreement give rise to no "
              "commission. Benefits already granted to persons introduced earlier remain in place."),
        ("p", "4.7. Commissions are paid quarterly, within thirty (30) days of the end of each "
              "calendar quarter, by SEPA bank transfer in euros to a euro-zone IBAN the Partner "
              "indicates in writing. A single transfer covers all the Partner's commissions for the "
              "quarter. If the total due for a quarter is below EUR 100, no transfer is made and the "
              "amount is carried forward to the next quarter; carried-over amounts are paid with the "
              "next transfer and, in any case, within thirty (30) days of the end of this Agreement. "
              "Any other currency or payment route requested by the Partner is at the Partner's "
              "cost. Each payment comes with a statement showing, for each request, the client "
              "reference, the date, the type of service, the Service Fee received and the commission. "
              "A client's name appears only with that client's consent."),
        ("p", "4.8. If a request is cancelled or refunded, the corresponding commission is deducted "
              "from the next statement."),
        ("p", "4.9. The Partner alone is responsible for declaring and paying any tax or social "
              "contribution due on the commissions, and issues an invoice where the law applicable "
              "to the Partner requires one."),

        ("h", "Article 5. The Partner's communications"),
        ("p", "5.1. The Partner describes UNSEEN.'s services accurately and never states or suggests "
              "that UNSEEN. guarantees a commercial outcome, and in particular the allocation of any "
              "product, including quota handbags."),
        ("p", "5.2. Any promotional content clearly discloses the commercial relationship with "
              "UNSEEN., as required by the laws applicable to the Partner and to the Partner's audience."),
        ("p", "5.3. The Partner has no authority to bind UNSEEN., quote a price or promise "
              "availability on its behalf."),
        ("p", "5.4. The Partner keeps full editorial freedom over, and ownership of, the content the "
              "Partner creates about the Partner's own experience, and does not name or identify UNSEEN.'s suppliers or "
              "partners. UNSEEN. may share that content only with the Partner's prior approval and "
              "within the limits of its own commitments to its suppliers."),

        ("h", "Article 6. Independence and non-exclusivity"),
        ("p", "Each Party acts as an independent professional. This Agreement creates no employment, "
              "agency, partnership or exclusivity. The Partner remains free to work with other "
              "brands, provided this does not harm UNSEEN.'s image or interests."),

        ("h", "Article 7. Confidentiality"),
        ("p", "7.1. Each Party keeps confidential the non-public information received from the other, "
              "in particular prices and terms, the identity of clients, suppliers and partners, and "
              "working methods, during this Agreement and for three (3) years after it ends."),
        ("p", "7.2. This does not apply to information that is public through no fault of the "
              "receiving Party, was already known to it, was lawfully received from a third party, "
              "or must be disclosed by law."),

        ("h", "Article 8. Personal data"),
        ("p", "The Partner passes on a person's contact details only with that person's consent. "
              "UNSEEN. processes the data it collects as controller, under the GDPR, and shares no "
              "client data with the Partner beyond Article 4.7. Requests: privacy@unseenconciergerie.com."),

        ("h", "Article 9. Brand"),
        ("p", "The UNSEEN. name, logo and visual identity remain UNSEEN.'s exclusive property. The "
              "Partner may mention the partnership with UNSEEN. and use its name accurately, without "
              "altering it."),

        ("h", "Article 10. Founding status"),
        ("p", "If UNSEEN. relaunches an annual membership, the Partner keeps founding-client status "
              "and is offered its terms first. This creates no obligation for UNSEEN. to launch it."),

        ("h", "Article 11. Term and termination"),
        ("p", "11.1. This Agreement takes effect on signature by both Parties, for twelve (12) months, "
              "renewed automatically for successive twelve-month periods."),
        ("p", "11.2. Either Party may end it at any time by written notice, with thirty (30) days' "
              "notice. In case of a serious breach not remedied within fifteen (15) days of a written "
              "notice, the other Party may end it immediately."),
        ("p", "11.3. Commissions on requests performed and paid before the end date remain due. "
              "Articles 7 and 8 survive."),

        ("h", "Article 12. General provisions"),
        ("p", "12.1. UNSEEN.'s invoices bear the mention: VAT not applicable, article L.223-3 CIBS."),
        ("p", "12.2. This Agreement is governed by French law. Failing an amicable settlement within "
              "thirty (30) days of written notice of a dispute, the competent French courts have "
              "jurisdiction, without prejudice to any protective rules applicable to the Partner."),
        ("p", "12.3. This Agreement is made in English and in French. In case of discrepancy, the "
              "French version prevails."),
        ("p", "12.4. Any amendment requires a written agreement signed by both Parties. If a clause "
              "is held invalid, the others remain in force. Notices are given by email: UNSEEN., "
              f"contact@unseenconciergerie.com; the Partner, {i['email']}."),
        ("p", "12.5. The Parties agree to sign electronically and recognise the validity and "
              "evidential value of the electronic signature (Regulation (EU) No 910/2014 and "
              "articles 1366 and 1367 of the French Civil Code)."),
    ]


def partenariat_fr(i):
    """Version française de l'accord de partenariat (version qui prévaut)."""
    return [
        ("titre", "ACCORD DE PARTENARIAT ET D'APPORT D'AFFAIRES"),
        ("sous", "Version française. Elle prévaut en cas de divergence avec la version anglaise."),
        ("h", "Entre"),
        ("p", UNSEEN_FR + ","),
        ("p", "et"),
        ("p", f"**{i['nom_usage']}**, {i.get('profession_fr', i['profession'])}, "
              f"demeurant {i['adresse']}, {i['email']} (le « **Partenaire** »)."),
        ("p", "Ensemble les « Parties »."),

        ("h", "Préambule"),
        ("p", "UNSEEN. est une conciergerie privée basée à Paris. Le Partenaire est créateur de "
              "contenu dans l'univers du luxe (Instagram @shopaholique6, TikTok @mayankbhatter) et "
              "peut recommander UNSEEN. à son audience et à ses relations. Le présent accord fixe un "
              "dispositif d'apport d'affaires simple. Il remplace toutes les discussions et tous les "
              "projets antérieurs entre les Parties sur ce sujet."),

        ("h", "Article 1. Objet"),
        ("p", "Le présent accord définit le code de parrainage, l'avantage accordé aux clients "
              "apportés par le Partenaire, la commission du Partenaire et les obligations de chaque "
              "Partie. Les prestations que le Partenaire réserve pour lui-même relèvent de leurs "
              "propres contrats de réservation."),

        ("h", "Article 2. Code de parrainage et Clients Apportés"),
        ("p", "2.1. UNSEEN. attribue au Partenaire un code de parrainage unique dans les sept (7) "
              "jours suivant la signature."),
        ("p", "2.2. Est un « **Client Apporté** » la personne qui (a) contacte UNSEEN. pour la "
              "première fois au moyen du code, ou que le Partenaire a présentée par écrit à UNSEEN. "
              "avant ce premier contact, (b) n'entretenait aucune relation d'affaires antérieure avec "
              "UNSEEN., et (c) signe et règle au moins une demande après la signature du présent accord."),
        ("p", "2.3. Les enregistrements écrits d'UNSEEN. font foi. Le Partenaire peut à tout moment "
              "demander à UNSEEN. de confirmer si une personne qu'il a présentée est un Client Apporté."),

        ("h", "Article 3. Avantage accordé aux Clients Apportés"),
        ("p", "3.1. Chaque Client Apporté bénéficie de **50 % de réduction sur les Honoraires "
              "d'UNSEEN. pour ses deux (2) premières demandes** (les « Honoraires » sont définis "
              "à l'article 4.1)."),
        ("p", "3.2. L'avantage s'applique une seule fois par Client Apporté, sur les Honoraires "
              "uniquement, jamais sur les coûts des prestataires. Il n'est cumulable avec aucune "
              "autre offre et ne constitue pas une remise permanente."),
        ("p", "3.3. UNSEEN. n'augmente pas ses honoraires pour compenser l'avantage. Le Partenaire "
              "présente l'avantage uniquement dans les termes du présent article, et jamais par "
              "rapport à un prix de référence majoré."),

        ("h", "Article 4. Commission"),
        ("p", "4.1. On entend par « **Honoraires** » la rémunération qu'UNSEEN. facture pour son "
              "propre travail sur une demande, identifiée comme telle sur son devis ou sa facture, à "
              "l'exclusion de tout coût de prestataire et de toute somme reversée à un tiers."),
        ("p", "4.2. Pour chaque Client Apporté, le Partenaire perçoit une commission de **dix pour "
              "cent (10 %) des Honoraires effectivement facturés et encaissés par UNSEEN.**, après "
              "toute réduction, sur les demandes acceptées pendant les six (6) mois suivant la "
              "première demande signée de ce client."),
        ("p", "4.3. La commission n'est jamais calculée sur le montant total facturé, sur les coûts "
              "des prestataires, sur les achats du client ni sur les sommes reversées. Exemple : sur "
              "une demande comportant 700 euros d'Honoraires, la commission est de 70 euros, quel "
              "que soit le total facturé. Lorsque l'avantage de 50 % s'applique, les Honoraires sont "
              "de 350 euros et la commission de 35 euros."),
        ("p", "4.4. Certaines prestations sont vendues à un prix forfaitaire tout compris, sans "
              "Honoraires distincts (par exemple un rendez-vous privé en maison). Pour celles-ci, "
              "UNSEEN. précise dans son devis si et comment les articles 3 et 4 s'appliquent. À "
              "défaut de cette précision, ils ne s'appliquent pas."),
        ("p", "4.5. Aucune commission ni aucun avantage ne s'applique aux demandes faites par le "
              "Partenaire ou pour lui, ni à celles des personnes qui voyagent avec lui ou qui sont "
              "réservées à sa demande, sauf accord écrit d'UNSEEN."),
        ("p", "4.6. Les demandes acceptées avant la signature du présent accord n'ouvrent droit à "
              "aucune commission. Les avantages déjà accordés aux personnes présentées auparavant "
              "sont maintenus."),
        ("p", "4.7. Les commissions sont versées chaque trimestre, dans les trente (30) jours suivant "
              "la fin de chaque trimestre civil, par virement SEPA en euros sur un IBAN de la zone euro "
              "indiqué par écrit par le Partenaire. Un seul virement couvre toutes les commissions du "
              "trimestre. Lorsque le total dû pour un trimestre est inférieur à 100 euros, aucun "
              "virement n'est effectué et le montant est reporté au trimestre suivant ; les sommes "
              "reportées sont versées avec le virement suivant et, en tout état de cause, dans les "
              "trente (30) jours suivant la fin du présent accord. Toute autre devise ou tout autre "
              "mode de paiement demandé par le Partenaire est à ses frais. Chaque versement est "
              "accompagné d'un relevé indiquant, pour chaque "
              "demande, la référence du client, la date, le type de prestation, les Honoraires "
              "encaissés et la commission. Le nom d'un client n'y figure qu'avec son accord."),
        ("p", "4.8. En cas d'annulation ou de remboursement d'une demande, la commission "
              "correspondante est déduite du relevé suivant."),
        ("p", "4.9. Le Partenaire est seul responsable de la déclaration et du paiement des impôts "
              "et contributions dus sur ses commissions, et émet une facture lorsque la loi qui lui "
              "est applicable l'exige."),

        ("h", "Article 5. Communication du Partenaire"),
        ("p", "5.1. Le Partenaire présente les services d'UNSEEN. avec exactitude. Il n'affirme ni "
              "ne laisse entendre qu'UNSEEN. garantit un résultat commercial, et notamment "
              "l'attribution d'un produit, y compris d'un sac soumis à quota."),
        ("p", "5.2. Tout contenu promotionnel mentionne clairement la relation commerciale avec "
              "UNSEEN., conformément aux lois applicables au Partenaire et à son audience."),
        ("p", "5.3. Le Partenaire n'a aucun pouvoir d'engager UNSEEN., d'annoncer un prix ou de "
              "promettre une disponibilité en son nom."),
        ("p", "5.4. Le Partenaire conserve une entière liberté éditoriale et la propriété du contenu "
              "qu'il crée sur sa propre expérience. Il ne nomme ni n'identifie les prestataires ou "
              "partenaires d'UNSEEN. UNSEEN. ne peut partager ce contenu qu'avec l'accord préalable "
              "du Partenaire et dans les limites de ses propres engagements envers ses prestataires."),

        ("h", "Article 6. Indépendance et absence d'exclusivité"),
        ("p", "Chaque Partie agit en professionnel indépendant. Le présent accord ne crée ni contrat "
              "de travail, ni mandat, ni société, ni exclusivité. Le Partenaire reste libre de "
              "collaborer avec d'autres marques, sous réserve de ne pas nuire à l'image ou aux "
              "intérêts d'UNSEEN."),

        ("h", "Article 7. Confidentialité"),
        ("p", "7.1. Chaque Partie garde confidentielles les informations non publiques reçues de "
              "l'autre, notamment les prix et conditions, l'identité des clients, prestataires et "
              "partenaires, et les méthodes de travail, pendant la durée du présent accord et trois "
              "(3) ans après son terme."),
        ("p", "7.2. Cette obligation ne s'applique pas aux informations devenues publiques sans "
              "faute de la Partie qui les a reçues, déjà connues d'elle, reçues légitimement d'un "
              "tiers ou dont la loi impose la communication."),

        ("h", "Article 8. Données personnelles"),
        ("p", "Le Partenaire ne transmet les coordonnées d'une personne qu'avec l'accord de celle-ci. "
              "UNSEEN. traite les données qu'il collecte en qualité de responsable de traitement, "
              "conformément au RGPD, et ne communique au Partenaire aucune donnée client au-delà de "
              "l'article 4.7. Demandes : privacy@unseenconciergerie.com."),

        ("h", "Article 9. Marque"),
        ("p", "Le nom, le logo et l'identité visuelle UNSEEN. restent la propriété exclusive "
              "d'UNSEEN. Le Partenaire peut mentionner son partenariat avec UNSEEN. et utiliser son "
              "nom avec exactitude, sans l'altérer."),

        ("h", "Article 10. Statut de client fondateur"),
        ("p", "Si UNSEEN. relance une adhésion annuelle, le Partenaire conserve son statut de client "
              "fondateur et se voit proposer ses conditions en priorité. Cette clause n'oblige pas "
              "UNSEEN. à la lancer."),

        ("h", "Article 11. Durée et résiliation"),
        ("p", "11.1. Le présent accord prend effet à sa signature par les deux Parties, pour douze "
              "(12) mois, renouvelés tacitement par périodes successives de douze mois."),
        ("p", "11.2. Chaque Partie peut y mettre fin à tout moment par écrit, moyennant un préavis "
              "de trente (30) jours. En cas de manquement grave non réparé dans les quinze (15) jours "
              "d'une mise en demeure écrite, l'autre Partie peut y mettre fin immédiatement."),
        ("p", "11.3. Les commissions sur les demandes exécutées et encaissées avant la date de fin "
              "restent dues. Les articles 7 et 8 survivent à la fin de l'accord."),

        ("h", "Article 12. Dispositions générales"),
        ("p", "12.1. Les factures d'UNSEEN. portent la mention : TVA non applicable, article L.223-3 "
              "du CIBS."),
        ("p", "12.2. Le présent accord est régi par le droit français. À défaut de règlement amiable "
              "dans les trente (30) jours suivant la notification écrite d'un différend, les "
              "juridictions françaises compétentes sont seules saisies, sans préjudice des règles "
              "protectrices applicables au Partenaire."),
        ("p", "12.3. Le présent accord est établi en anglais et en français. En cas de divergence, "
              "la version française prévaut."),
        ("p", "12.4. Toute modification fait l'objet d'un avenant écrit signé par les deux Parties. "
              "La nullité d'une clause n'affecte pas les autres. Les notifications se font par "
              "courriel : UNSEEN., contact@unseenconciergerie.com ; le Partenaire, "
              f"{i['email']}."),
        ("p", "12.5. Les Parties conviennent de signer par voie électronique et reconnaissent la "
              "validité et la force probante de la signature électronique (règlement (UE) "
              "n° 910/2014 et articles 1366 et 1367 du code civil)."),
    ]


# ---------------------------------------------------------------------------
# 2. CONTRAT DE RÉSERVATION : RENDEZ-VOUS PRIVÉ HERMÈS PARIS
# ---------------------------------------------------------------------------

def reservation_en(i):
    """Version anglaise du contrat de réservation (version de lecture)."""
    return [
        ("titre", "BOOKING AGREEMENT"),
        ("sous", "Private appointment, Hermès Paris. English version, provided for convenience. "
                 "The French version below prevails."),
        ("h", "Between"),
        ("p", UNSEEN_EN + ","),
        ("p", "and"),
        ("p", f"**{i['client_nom']}**, residing at {i['client_adresse']}, {i['client_email']} "
              "(the \"**Client**\")."),
        ("p", f"Payment is made by: {i['payeur_en']} (the \"**Payer**\")."),

        ("h", "Booking summary"),
        ("tableau", [
            ["Service", "One private appointment with a sales advisor at one of the three Hermès "
                        "boutiques in Paris"],
            ["Target dates", f"{i['dates_en']}, the day being chosen by UNSEEN. as set out in "
                             "Article 1.2"],
            ["Preferred time", f"{i['heure_en']} (requested, not guaranteed)"],
            ["Total price", f"EUR {i['prix']}, all inclusive, nothing payable on site"],
            ["Deposit", f"EUR {i['acompte']}, to be received by {i['date_acompte_en']}, refundable "
                        "in full if no appointment is obtained"],
            ["Balance", f"EUR {i['solde']}, due on the store's written confirmation, the day "
                        "before the appointment"],
        ]),

        ("h", "Article 1. The service"),
        ("p", "1.1. UNSEEN. obtains for the Client one private appointment with a sales advisor at "
              "one of the three Hermès boutiques in Paris. The boutique is assigned: UNSEEN. cannot "
              "promise a specific boutique."),
        ("p", f"1.2. The appointment is sought on {i['dates_en']}. UNSEEN. chooses the day on the "
              "advice of its partner as to the best chances, and informs the Client in writing. "
              f"A time around {i['heure_en']} is requested, without guarantee."),
        ("p", "1.3. The appointment is booked in the Client's name, the day before the visit. The "
              "\"**Written Confirmation**\" is the store's written confirmation of the date, time "
              "and boutique, a copy of which UNSEEN. sends to the Client."),
        ("p", "1.4. UNSEEN. works through an independent partner, bound to it by a signed agreement "
              "covering confidentiality and non-circumvention, which UNSEEN. does not name. That "
              "partner is contractually bound to obtain appointments by lawful means, without any "
              "payment or advantage to an employee of the maison. UNSEEN. does not know, and makes "
              "no statement about, who handles the booking on the maison's side or whether the "
              "advisor knows how the appointment was obtained."),

        ("h", "Article 2. What the service does not include"),
        ("p", "2.1. The service is the appointment only. **No purchase, allocation or product is "
              "guaranteed**, including Birkin, Kelly or any quota handbag. Any offer is decided "
              "solely by the advisor and the maison on the day. If a piece is not in store, the "
              "advisor may arrange for it to reach the Client later, at the advisor's sole "
              "discretion."),
        ("p", "2.2. Any purchase is made by the Client personally, in the Client's own name, directly from "
              "the maison. UNSEEN. does not purchase on the Client's behalf under this Agreement. "
              "The Client pays nothing on site for the appointment itself."),

        ("h", "Article 3. Price and payment"),
        ("p", f"3.1. The price is **EUR {i['prix']}, all inclusive**, with no fee on top. VAT not "
              "applicable, article L.223-3 CIBS."),
        ("p", f"3.2. A deposit of **EUR {i['acompte']}** must be received by UNSEEN. by "
              f"**{i['date_acompte_en']}**, together with the Client's passport details (full name, number and expiry date) "
              "and, where possible, a copy of the passport. UNSEEN. "
              "places the booking once both are received. The deposit is due before the Written "
              "Confirmation because UNSEEN.'s partner requires payment before booking."),
        ("p", f"3.3. The balance of **EUR {i['solde']}** is due on the Written Confirmation, the day "
              "before the appointment, and must be received before the appointment. No payment is "
              "ever requested after the visit."),
        ("p", "3.4. Payments are made by bank transfer in euros to the account below. Amounts must "
              "reach UNSEEN. in full: transfer and currency conversion costs are borne by the Payer "
              "(with Wise, choose \"recipient gets exactly\" the amount in EUR). UNSEEN. never "
              "changes its bank details by email alone; before a first transfer, the Payer may "
              "confirm them by telephone with UNSEEN."),
        ("tableau", [
            ["Account holder", i["titulaire"]],
            ["IBAN", i["iban"]],
            ["BIC", i["bic"]],
            ["Bank", i["banque"]],
            ["Reference", i["reference"]],
        ]),
        ("p", "3.5. UNSEEN. issues an invoice for each payment. Where the Payer is not the Client, "
              "the Client remains the beneficiary of the service and any refund is made to the Payer."),

        ("h", "Article 4. Refunds and cancellation"),
        ("li", "**No appointment obtained**: the deposit is refunded in full within five (5) working "
               "days and nothing else is due."),
        ("li", "**Appointment confirmed, then cancelled or not honoured by the maison**: every amount "
               "paid is refunded in full."),
        ("li", "**Appointment held, and no piece offered or bought**: no refund, as the service is the "
               "appointment, never a purchase."),
        ("li", "**Client cancels, or does not attend, after UNSEEN. has placed the booking**: the "
               "amounts paid are not refunded and the balance remains due once the Written "
               "Confirmation has been issued, the appointment being personal and booked in the "
               "Client's name."),

        ("h", "Article 5. Right of withdrawal"),
        ("p", "Where the Client contracts as a consumer, the Client has in principle fourteen (14) days to "
              "withdraw from a distance contract. As the appointment falls within that period, the "
              "Client **expressly asks UNSEEN. to begin performance immediately**. The Client acknowledges "
              "that, in case of withdrawal after performance has begun, an amount proportionate "
              "to the service provided until the withdrawal is owed, and that **the right of "
              "withdrawal is lost once the service has been fully performed** (articles L.221-25 and "
              "L.221-28 of the French Consumer Code)."),

        ("h", "Article 6. Identity documents and personal data"),
        ("p", "The Client consents to UNSEEN. receiving the Client's passport details and, where provided, a "
              "copy of the passport, and passing them only to "
              "the partner who places the booking, for that sole purpose. UNSEEN. and its partner "
              "delete them within thirty (30) days after the service. UNSEEN. processes personal data "
              "as controller under the GDPR. Requests: privacy@unseenconciergerie.com."),

        ("h", "Article 7. Discretion"),
        ("p", "UNSEEN. keeps the Client's identity and request confidential. The Client does not "
              "seek to identify or approach UNSEEN.'s partner in order to obtain the same service "
              "directly, for twelve (12) months, as provided in UNSEEN.'s terms."),

        ("h", "Article 8. Liability"),
        ("p", "UNSEEN. is bound by a reinforced obligation of means. It guarantees the performance "
              "of the service described, not its commercial outcome. To the extent permitted by "
              "law, its liability is limited to direct and foreseeable loss and capped at the "
              "amounts received under this Agreement."),

        ("h", "Article 9. General provisions"),
        ("p", "9.1. UNSEEN.'s terms (unseenconciergerie.com/legal) apply. In case of conflict, this "
              "Agreement prevails. It replaces the earlier exchanges on this appointment."),
        ("p", "9.2. Complaints: contact@unseenconciergerie.com, answered within fifteen (15) days. "
              "A consumer may refer an unresolved complaint free of charge to a consumer mediator, "
              "whose details are: CM2C, 49 rue de Ponthieu, 75008 Paris, tel. +33 1 89 47 00 14, "
              "cm2c.net/declarer-un-litige.php, litiges@cm2c.net."),
        ("p", "9.3. This Agreement is governed by French law. Failing an amicable settlement within "
              "thirty (30) days of written notice of a dispute, the competent French courts have "
              "jurisdiction, without prejudice to the protective rules applicable to consumers. It "
              "is made in English and in French; the French version prevails."),
        ("p", "9.4. The Parties agree to sign electronically and recognise the validity and "
              "evidential value of the electronic signature (Regulation (EU) No 910/2014 and "
              "articles 1366 and 1367 of the French Civil Code)."),
    ]


def reservation_fr(i):
    """Version française du contrat de réservation (version qui prévaut)."""
    return [
        ("titre", "CONTRAT DE RÉSERVATION"),
        ("sous", "Rendez-vous privé, Hermès Paris. Version française. Elle prévaut en cas de "
                 "divergence avec la version anglaise."),
        ("h", "Entre"),
        ("p", UNSEEN_FR + ","),
        ("p", "et"),
        ("p", f"**{i['client_nom']}**, demeurant {i['client_adresse']}, {i['client_email']} "
              "(le « **Client** »)."),
        ("p", f"Le paiement est effectué par : {i['payeur_fr']} (le « **Payeur** »)."),

        ("h", "Récapitulatif de la réservation"),
        ("tableau", [
            ["Prestation", "Un rendez-vous privé avec un conseiller de vente dans l'une des trois "
                           "boutiques Hermès de Paris"],
            ["Dates visées", f"{i['dates_fr']}, le jour étant choisi par UNSEEN. selon "
                             "l'article 1.2"],
            ["Horaire souhaité", f"{i['heure_fr']} (demandé, non garanti)"],
            ["Prix total", f"{i['prix'].replace(',', ' ')} euros, tout compris, rien à payer sur place"],
            ["Acompte", f"{i['acompte']} euros, à recevoir au plus tard le {i['date_acompte_fr']}, "
                        "remboursé intégralement si aucun rendez-vous n'est obtenu"],
            ["Solde", f"{i['solde'].replace(',', ' ')} euros, dû à la confirmation écrite de la boutique, la veille "
                      "du rendez-vous"],
        ]),

        ("h", "Article 1. La prestation"),
        ("p", "1.1. UNSEEN. obtient pour le Client un rendez-vous privé avec un conseiller de vente "
              "dans l'une des trois boutiques Hermès de Paris. La boutique est attribuée : UNSEEN. "
              "ne peut pas promettre une boutique déterminée."),
        ("p", f"1.2. Le rendez-vous est recherché le {i['dates_fr']}. UNSEEN. choisit le jour sur "
              "l'avis de son partenaire quant aux meilleures chances, et en informe le Client par "
              f"écrit. Un horaire vers {i['heure_fr']} est demandé, sans garantie."),
        ("p", "1.3. Le rendez-vous est réservé au nom du Client, la veille de la visite. La "
              "« **Confirmation Écrite** » est la confirmation écrite de la boutique indiquant la "
              "date, l'heure et la boutique, dont UNSEEN. transmet une copie au Client."),
        ("p", "1.4. UNSEEN. fait appel à un partenaire indépendant, lié à lui par un accord signé de "
              "confidentialité et de non-contournement, qu'UNSEEN. ne nomme pas. Ce partenaire est "
              "contractuellement tenu d'obtenir les rendez-vous par des moyens licites, sans aucun "
              "versement ni avantage à un salarié de la maison. UNSEEN. ignore, et n'affirme rien "
              "sur, la personne qui traite la réservation du côté de la maison ou sur le fait que le "
              "conseiller sache comment le rendez-vous a été obtenu."),

        ("h", "Article 2. Ce que la prestation ne comprend pas"),
        ("p", "2.1. La prestation porte uniquement sur le rendez-vous. **Aucun achat, aucune "
              "attribution ni aucun produit n'est garanti**, y compris un Birkin, un Kelly ou tout "
              "sac soumis à quota. Toute proposition relève de la seule décision du conseiller et "
              "de la maison le jour même. Si une pièce n'est pas en boutique, le conseiller peut "
              "faire en sorte qu'elle parvienne plus tard au Client, à sa seule discrétion."),
        ("p", "2.2. Tout achat est effectué par le Client lui-même, en son nom, directement auprès "
              "de la maison. UNSEEN. n'achète pas pour le compte du Client au titre du présent "
              "contrat. Le Client ne paie rien sur place pour le rendez-vous lui-même."),

        ("h", "Article 3. Prix et paiement"),
        ("p", f"3.1. Le prix est de **{i['prix'].replace(',', ' ')} euros, tout compris**, sans honoraires en sus. "
              "TVA non applicable, article L.223-3 du CIBS."),
        ("p", f"3.2. Un acompte de **{i['acompte']} euros** doit être reçu par UNSEEN. au plus tard "
              f"le **{i['date_acompte_fr']}**, accompagné des informations de passeport du Client (nom complet, numéro et date "
              "d'expiration) et, si possible, d'une copie du passeport. UNSEEN. "
              "place la réservation dès réception des deux. L'acompte est dû avant la Confirmation "
              "Écrite car le partenaire d'UNSEEN. exige d'être réglé avant de réserver."),
        ("p", f"3.3. Le solde de **{i['solde'].replace(',', ' ')} euros** est dû à la Confirmation Écrite, la veille du "
              "rendez-vous, et doit être reçu avant le rendez-vous. Aucun paiement n'est jamais "
              "demandé après la visite."),
        ("p", "3.4. Les paiements se font par virement en euros sur le compte ci-dessous. Les "
              "montants doivent parvenir intégralement à UNSEEN. : les frais de virement et de "
              "conversion sont à la charge du Payeur (avec Wise, choisir que le destinataire "
              "reçoive exactement le montant en euros). UNSEEN. ne modifie jamais ses coordonnées "
              "bancaires par simple courriel ; avant un premier virement, le Payeur peut les "
              "confirmer par téléphone auprès d'UNSEEN."),
        ("tableau", [
            ["Titulaire", i["titulaire"]],
            ["IBAN", i["iban"]],
            ["BIC", i["bic"]],
            ["Banque", i["banque"]],
            ["Référence", i["reference"]],
        ]),
        ("p", "3.5. UNSEEN. émet une facture pour chaque paiement. Lorsque le Payeur n'est pas le "
              "Client, le Client reste le bénéficiaire de la prestation et tout remboursement est "
              "fait au Payeur."),

        ("h", "Article 4. Remboursements et annulation"),
        ("li", "**Aucun rendez-vous obtenu** : l'acompte est remboursé intégralement sous cinq (5) "
               "jours ouvrés et rien d'autre n'est dû."),
        ("li", "**Rendez-vous confirmé, puis annulé ou non honoré par la maison** : toutes les "
               "sommes versées sont remboursées intégralement."),
        ("li", "**Rendez-vous tenu, sans pièce proposée ni achetée** : aucun remboursement, la "
               "prestation étant le rendez-vous, jamais un achat."),
        ("li", "**Le Client annule, ou ne se présente pas, après qu'UNSEEN. a placé la "
               "réservation** : les sommes versées ne sont pas remboursées et le solde reste dû dès "
               "lors que la Confirmation Écrite a été émise, le rendez-vous étant personnel et "
               "réservé au nom du Client."),

        ("h", "Article 5. Droit de rétractation"),
        ("p", "Lorsque le Client contracte en tant que consommateur, il dispose en principe de "
              "quatorze (14) jours pour se rétracter d'un contrat conclu à distance. Le rendez-vous "
              "intervenant dans ce délai, le Client **demande expressément à UNSEEN. de commencer "
              "l'exécution immédiatement**. Il reconnaît que, s'il se rétracte après le début de "
              "l'exécution, il doit un montant proportionnel au service fourni jusqu'à sa "
              "rétractation, et qu'**il perd son droit de rétractation une fois la prestation "
              "pleinement exécutée** (articles L.221-25 et L.221-28 du code de la consommation)."),

        ("h", "Article 6. Pièces d'identité et données personnelles"),
        ("p", "Le Client accepte qu'UNSEEN. reçoive les informations de son passeport et, s'il la fournit, "
              "une copie de celui-ci, et les transmette "
              "uniquement au partenaire qui place la réservation, à cette seule fin. UNSEEN. et son "
              "partenaire les suppriment dans les trente (30) jours suivant la prestation. UNSEEN. "
              "traite les données personnelles en qualité de responsable de traitement, "
              "conformément au RGPD. Demandes : privacy@unseenconciergerie.com."),

        ("h", "Article 7. Discrétion"),
        ("p", "UNSEEN. garde confidentiels l'identité et la demande du Client. Le Client ne cherche "
              "pas à identifier ni à approcher le partenaire d'UNSEEN. pour obtenir directement la "
              "même prestation, pendant douze (12) mois, comme le prévoient les conditions "
              "d'UNSEEN."),

        ("h", "Article 8. Responsabilité"),
        ("p", "UNSEEN. est tenu d'une obligation de moyens renforcée. Il garantit l'exécution de la "
              "prestation décrite, non son résultat commercial. Dans la mesure permise par la loi, "
              "sa responsabilité est limitée aux préjudices directs et prévisibles et plafonnée aux "
              "sommes reçues au titre du présent contrat."),

        ("h", "Article 9. Dispositions générales"),
        ("p", "9.1. Les conditions d'UNSEEN. (unseenconciergerie.com/legal) s'appliquent. En cas "
              "de contradiction, le présent contrat prévaut. Il remplace les échanges antérieurs "
              "relatifs à ce rendez-vous."),
        ("p", "9.2. Réclamations : contact@unseenconciergerie.com, réponse sous quinze (15) jours. "
              "Le consommateur peut soumettre gratuitement une réclamation non résolue à un "
              "médiateur de la consommation : CM2C, 49 rue de Ponthieu, 75008 Paris, tél. 01 89 47 00 14, "
              "cm2c.net/declarer-un-litige.php, litiges@cm2c.net."),
        ("p", "9.3. Le présent contrat est régi par le droit français. À défaut de règlement amiable "
              "dans les trente (30) jours suivant la notification écrite d'un différend, les "
              "juridictions françaises compétentes sont seules saisies, sans préjudice des règles "
              "protectrices applicables au consommateur. Il est établi en anglais et en français ; "
              "la version française prévaut."),
        ("p", "9.4. Les Parties conviennent de signer par voie électronique et reconnaissent la "
              "validité et la force probante de la signature électronique (règlement (UE) "
              "n° 910/2014 et articles 1366 et 1367 du code civil)."),
    ]


def signatures(nom_droite_en, nom_droite_fr, nom_signataire=""):
    """Bloc de signature commun aux deux versions (une seule signature vaut pour les deux)."""
    return [
        ("h", "Signatures"),
        ("p", "Signed electronically. One signature covers both the English and the French "
              "versions. / Signé par voie électronique. Une seule signature vaut pour les versions "
              "anglaise et française."),
        ("signatures", ("For UNSEEN. / Pour UNSEEN.", "Jay Pandea, Founder / fondateur",
                        f"{nom_droite_en} / {nom_droite_fr}", nom_signataire)),
    ]


# ---------------------------------------------------------------------------
# 3. DOSSIER D'ACCORDS : plusieurs accords, une seule signature
# ---------------------------------------------------------------------------

def paquet_couverture(p, r):
    """Page de garde du dossier : explique que deux accords distincts sont
    regroupés pour n'avoir qu'une seule signature."""
    nom = p["nom_usage"]
    prix_fr = r["prix"].replace(",", " ")
    return [
        ("titre", "AGREEMENT PACK / DOSSIER D'ACCORDS"),
        ("sous", f"UNSEEN. and {nom}. Two agreements, one signature. / "
                 f"UNSEEN. et {nom}. Deux accords, une seule signature."),
        ("h", "English"),
        ("p", f"This document groups two agreements between UNSEEN. and {nom} so that a single "
              "signature covers both. Each one remains a separate agreement, with its own terms."),
        ("li", "**Part A. Partnership and Referral Agreement**: referral code, benefit for the "
               "clients the Partner refers, and the Partner's commission on UNSEEN.'s service fees."),
        ("li", f"**Part B. Booking Agreement, Hermès appointment**: the Partner's own private "
               f"appointment, at a total price of EUR {r['prix']} all inclusive, with a "
               f"EUR {r['acompte']} deposit refundable in full if no appointment is obtained."),
        ("p", "As set out in Article 4.5 of Part A, the Partner earns no referral commission and "
              "receives no referral benefit on his own bookings, which are governed by Part B only."),
        ("p", "Each part is written in English, then in French. The French version prevails. "
              "One signature on the last page covers both parts and both languages."),
        ("h", "Français"),
        ("p", f"Ce document regroupe deux accords entre UNSEEN. et {nom} afin qu'une seule "
              "signature vaille pour les deux. Chacun reste un accord distinct, avec ses propres "
              "conditions."),
        ("li", "**Partie A. Accord de partenariat et d'apport d'affaires** : code de parrainage, "
               "avantage offert aux clients apportés par le Partenaire, et commission du Partenaire "
               "sur les honoraires d'UNSEEN."),
        ("li", f"**Partie B. Contrat de réservation, rendez-vous Hermès** : le rendez-vous privé "
               f"du Partenaire lui-même, au prix total de {prix_fr} euros tout compris, avec un "
               f"acompte de {r['acompte']} euros remboursé intégralement si aucun rendez-vous "
               "n'est obtenu."),
        ("p", "Comme le prévoit l'article 4.5 de la Partie A, le Partenaire ne perçoit aucune "
              "commission de parrainage et ne bénéficie d'aucun avantage de parrainage sur ses "
              "propres réservations, qui relèvent uniquement de la Partie B."),
        ("p", "Chaque partie est rédigée en anglais, puis en français. La version française "
              "prévaut. Une seule signature, sur la dernière page, vaut pour les deux parties "
              "et pour les deux langues."),
        ("saut", None),
    ]


def signatures_paquet(nom_droite_en, nom_droite_fr, nom_signataire=""):
    """Bloc de signature unique pour tout le dossier."""
    return [
        ("h", "Signatures"),
        ("p", "Signed electronically. One signature covers Part A and Part B, in both the English "
              "and the French versions. / Signé par voie électronique. Une seule signature vaut "
              "pour la Partie A et la Partie B, dans les versions anglaise et française."),
        ("signatures", ("For UNSEEN. / Pour UNSEEN.", "Jay Pandea, Founder / fondateur",
                        f"{nom_droite_en} / {nom_droite_fr}", nom_signataire)),
    ]
