"""
Mentions légales, révision du 27/10/2026 (validée par Jay) :
- hébergeur corrigé (le site est sur GitHub Pages depuis octobre 2026, plus chez Infomaniak) ;
- « Prix et honoraires » : plus de détail du calcul ni de pourcentages (règle : le client voit un prix),
  mais le client reste prévenu quand un prestataire rémunère UNSEEN. ; « Nature de nos prestations »
  n'est PAS modifiée (elle protège UNSEEN. du statut d'agence de voyages) ;
- quelques tournures françaises reprises, date de mise à jour.

À lancer une seule fois, depuis le dossier du projet :
    python3 site-unseen/outils/legal_v2.py
"""
import html
import re
from pathlib import Path

PAGE = Path(__file__).resolve().parent.parent / "legal.html"

# (ancien anglais) : (nouvel anglais ou None pour le garder, nouveau français)
CHANGEMENTS = {
    "Last updated: 1 September 2026": ("Last updated: 27 October 2026", "Dernière mise à jour : 27 octobre 2026"),
    "How we are paid": ("Prices and fees", "Prix et honoraires"),
    "Every request involves two distinct amounts: the cost charged by the third-party provider, passed on exactly as invoiced to us, and our own service fee, which is the only part we earn. Both are stated before any commitment, or presented as a single all-inclusive package price clearly identified as such.":
        ("Every proposal states the price in writing before any commitment. Where a single all-inclusive price is quoted, it is clearly identified as such.",
         "Chaque proposition indique le prix par écrit avant tout engagement. Lorsqu'un prix global tout compris est proposé, il est clairement présenté comme tel."),
    "On certain services, and hotel bookings in particular, UNSEEN. may be paid a commission by the provider. This never increases the price paid by the client. Where such a commission applies, the client is told, and the service fee is reduced accordingly.":
        ("Where a provider pays UNSEEN. in connection with a service, the client is told in the proposal. This never increases the price the client pays.",
         "Lorsqu'un prestataire rémunère UNSEEN. au titre d'une prestation, le client en est informé dans la proposition. Cela n'augmente jamais le prix qu'il paie."),
    "Unless agreed otherwise in writing, one hundred per cent of the provider's cost and fifty per cent of the service fee are payable on booking, with the balance due before performance. No booking is placed with a provider before the corresponding funds have been received: UNSEEN. advances no funds.":
        ("Unless agreed otherwise in writing, a deposit is payable on booking and the balance before performance. No booking is placed with a provider before the corresponding funds have been received: UNSEEN. advances no funds.",
         "Sauf accord écrit contraire, un acompte est exigible à la commande et le solde avant l'exécution. Aucune réservation n'est engagée auprès d'un prestataire avant l'encaissement effectif des sommes correspondantes : UNSEEN. n'avance aucun fonds."),
    # tournures françaises (l'anglais ne change pas)
    "Confidentiality and client discretion": (None, "Confidentialité et discrétion"),
    "The English version is provided for convenience. In the event of any discrepancy, the French version prevails.":
        (None, "La version anglaise est fournie à titre indicatif. En cas de divergence, la version française prévaut."),
    "These terms are governed by French law. Failing an amicable settlement within thirty days of written notice of a dispute, the competent French courts have jurisdiction, without prejudice to the protective rules applicable to consumers.":
        (None, "Les présentes conditions sont régies par le droit français. À défaut de règlement amiable dans les trente jours suivant la notification écrite d'un différend, les juridictions françaises sont seules compétentes, sans préjudice des règles protectrices applicables au consommateur."),
    "Some services, such as a named appointment with a maison or a nominative booking, require an identity document. It is requested only once the service is confirmed, transmitted through a secure expiring link rather than by message, and deleted by the receiving provider within thirty days of performance.":
        (None, "Certaines prestations, comme un rendez-vous nominatif dans une maison de luxe ou une réservation nominative, exigent un document d'identité. Il n'est demandé qu'une fois la prestation confirmée, transmis par un lien sécurisé à durée limitée plutôt que par messagerie, et supprimé par le prestataire destinataire dans les trente jours suivant l'exécution."),
    "UNSEEN. never notifies a change of bank details by email or message alone. Any change is confirmed by three cumulative means: a signed letter in non-editable PDF sent from contact@unseenconciergerie.com; a telephone confirmation, the client calling us on the number stated in the original agreement and never on a number given in the message announcing the change; and the security reference agreed with the client at the first booking. A transfer made without all three is not discharging.":
        (None, "UNSEEN. ne notifie jamais un changement de coordonnées bancaires par simple e-mail ou message. Tout changement est confirmé par trois moyens cumulatifs : un courrier signé en PDF non modifiable envoyé depuis contact@unseenconciergerie.com ; une confirmation téléphonique, le client nous appelant au numéro figurant à son contrat initial et jamais à un numéro indiqué dans le message annonçant le changement ; et la référence de sécurité convenue avec le client lors de la première commande. Un virement effectué sans ces trois conditions n'est pas libératoire."),
}

HEBERGEUR_AVANT = ('<dd>Infomaniak Network SA, Rue Eugène-Marziano 25, 1227 Les Acacias, Genève, Suisse · '
                   '<span class="num">+41 22 820 35 40</span> · infomaniak.com</dd>')
HEBERGEUR_APRES = ('<dd>GitHub, Inc. (GitHub Pages), 88 Colin P. Kelly Jr Street, San Francisco, CA 94107, '
                   '<span data-en="United States" data-fr="États-Unis">United States</span> · github.com</dd>')


def main():
    page = PAGE.read_text(encoding="utf-8")
    assert page.count(HEBERGEUR_AVANT) == 1, "hébergeur introuvable (déjà corrigé ?)"
    page = page.replace(HEBERGEUR_AVANT, HEBERGEUR_APRES)
    for ancien, (nouvel_en, nouveau_fr) in CHANGEMENTS.items():
        # l'apostrophe peut être codée de plusieurs façons : on compare le texte décodé
        trouves = [m.start() for m in re.finditer(r'data-en="([^"]*)"', page) if html.unescape(m.group(1)) == ancien]
        assert len(trouves) == 1, ancien[:50]
        debut = trouves[0]
        # l'attribut data-fr qui suit
        d_fr = page.index('data-fr="', debut)
        f_fr = page.index('"', d_fr + 9)
        en = nouvel_en or ancien
        page = page[:debut] + f'data-en="{html.escape(en)}" ' + f'data-fr="{html.escape(nouveau_fr)}"' + page[f_fr + 1:]
        if nouvel_en:
            # texte affiché par défaut (anglais) : entre la fin de la balise et la balise fermante
            ouv = page.index(">", debut) + 1
            ferm = page.index("</", ouv)
            page = page[:ouv] + html.escape(nouvel_en, quote=False) + page[ferm:]
    PAGE.write_text(page, encoding="utf-8")
    print("legal.html mise à jour")


if __name__ == "__main__":
    main()
