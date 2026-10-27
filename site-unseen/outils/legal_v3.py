"""
Mentions légales, compléments du 27/10/2026 (validés par Jay sur le principe) :
paiement plus général, annulation par UNSEEN., délai de remboursement, âge, transferts hors UE,
cookies (polices hébergées sur le site), modification des conditions.
Écrit aussi la page « avant / après » dans Livrables/Maquettes site (évolution)/.

À lancer une seule fois, depuis le dossier du projet :
    python3 site-unseen/outils/legal_v3.py
"""
import html
import re
from pathlib import Path

PAGE = Path(__file__).resolve().parent.parent / "legal.html"
COMPARAISON = PAGE.parent.parent / "Livrables" / "Maquettes site (évolution)" / "14 Mentions légales, compléments (27-10).html"


def p(en, fr, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<p{c} data-en="{html.escape(en)}" data-fr="{html.escape(fr)}">{html.escape(en, quote=False)}</p>'


def h3(en, fr):
    return f'<h3 data-en="{html.escape(en)}" data-fr="{html.escape(fr)}">{html.escape(en, quote=False)}</h3>'


# Paragraphes remplacés : ancien anglais -> (nouvel anglais, nouveau français)
REMPLACES = {
    "Payment is by bank transfer, in euros. Where a client pays in another currency, conversion and transfer costs are borne by the client and the amount credited in euros must match the amount invoiced. Late payment carries interest at the European Central Bank refinancing rate plus ten points, together with the statutory recovery indemnity of forty euros for business clients.":
        ("Payment is made as set out in the proposal or invoice, by bank transfer or any other means agreed with the client, in euros unless agreed otherwise. For business clients, late payment carries interest at the European Central Bank refinancing rate plus ten points, together with the statutory recovery indemnity of forty euros.",
         "Le paiement s'effectue selon les modalités indiquées sur la proposition ou la facture, par virement bancaire ou tout autre moyen convenu avec le client, en euros sauf accord contraire. Pour les clients professionnels, tout retard de paiement porte intérêt au taux de refinancement de la Banque centrale européenne majoré de dix points, outre l'indemnité forfaitaire de recouvrement de quarante euros."),
    "This site sets no advertising or analytics cookies. Your language choice is stored locally in your browser and is never transmitted to us.":
        ("This site sets no cookies, whether for advertising or analytics. Its fonts are served from the site itself, with no call to a third-party service. Your language choice is stored locally in your browser and is never transmitted to us. As with any website, the host records technical connection data, such as the IP address, to deliver the pages and protect the service.",
         "Ce site ne dépose aucun cookie, ni publicitaire ni de mesure d'audience. Ses polices de caractères sont hébergées sur le site lui-même, sans appel à un service tiers. Votre choix de langue est enregistré localement dans votre navigateur et ne nous est jamais transmis. Comme pour tout site, l'hébergeur enregistre des données techniques de connexion, comme l'adresse IP, pour afficher les pages et protéger le service."),
}

# Paragraphes ajoutés après un paragraphe existant (repéré par son anglais)
AJOUTS = [
    ("Amounts already committed with a provider follow",
     p("If UNSEEN. is unable to deliver a confirmed service, the client is informed without delay and the service fees paid for it are refunded in full.",
       "Si UNSEEN. ne peut assurer une prestation confirmée, le client en est informé sans délai et les honoraires versés à ce titre lui sont intégralement remboursés.")
     + "\n      " +
     p("Any refund due by UNSEEN. is made within fourteen days, by the means of payment used by the client unless agreed otherwise. Refunds of amounts held by a provider follow that provider's own terms and timescales.",
       "Tout remboursement dû par UNSEEN. intervient dans un délai de quatorze jours, par le moyen de paiement utilisé par le client, sauf accord contraire. Le remboursement des sommes détenues par un prestataire suit les conditions et les délais propres à celui-ci.")
     + "\n      " +
     p("Our services are reserved for adults with full legal capacity.",
       "Nos prestations sont réservées aux personnes majeures et juridiquement capables.")),
    ("Only the providers strictly necessary",
     "\n      " + h3("Transfers outside the European Union", "Transferts hors de l'Union européenne") + "\n      " +
     p("Some of our technical providers are based outside the European Union: the hosting of this site (GitHub, United States), email (Google) and messaging services such as WhatsApp (Meta). These transfers are covered by the safeguards provided for by the GDPR, in particular the European Commission's adequacy decision on the EU-US Data Privacy Framework and standard contractual clauses.",
       "Certains de nos prestataires techniques sont établis hors de l'Union européenne : l'hébergement de ce site (GitHub, États-Unis), la messagerie électronique (Google) et des messageries comme WhatsApp (Meta). Ces transferts sont encadrés par les garanties prévues par le RGPD, notamment la décision d'adéquation de la Commission européenne relative au cadre de protection des données UE-États-Unis et les clauses contractuelles types.")),
    ("These terms are governed by French law.",
     p("UNSEEN. may update these terms. The terms applicable to a booking are those in force on the date it is accepted.",
       "UNSEEN. peut faire évoluer les présentes conditions. Celles applicables à une commande sont celles en vigueur à la date de son acceptation.")),
]


def paragraphe(page, debut_en):
    """Position (début, fin) de l'élément dont l'anglais commence par debut_en."""
    for m in re.finditer(r'<(p|h3)[^>]*data-en="([^"]*)"[^>]*>.*?</\1>', page, re.S):
        if html.unescape(m.group(2)).startswith(debut_en):
            return m.start(), m.end()
    raise ValueError(debut_en)


def main():
    page = PAGE.read_text(encoding="utf-8")
    assert "Transfers outside the European Union" not in page, "déjà appliqué"
    lignes = []
    for ancien, (en, fr) in REMPLACES.items():
        d, f = paragraphe(page, ancien)
        ancien_fr = html.unescape(re.search(r'data-fr="([^"]*)"', page[d:f]).group(1))
        cls = re.search(r'class="([^"]*)"', page[d:f])
        page = page[:d] + p(en, fr, cls.group(1) if cls else "") + page[f:]
        lignes.append((ancien_fr, fr))
    for apres_en, bloc in AJOUTS:
        d, f = paragraphe(page, apres_en)
        page = page[:f] + "\n      " + bloc.lstrip() + page[f:]
        for fr in re.findall(r'data-fr="([^"]*)"', bloc):
            lignes.append(("(nouveau)", html.unescape(fr)))
    PAGE.write_text(page, encoding="utf-8")

    rangs = "".join(f"<tr><td>{html.escape(a)}</td><td>{html.escape(b)}</td></tr>" for a, b in lignes)
    COMPARAISON.write_text(f"""<!doctype html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Mentions légales, compléments</title>
<style>body{{font-family:-apple-system,system-ui,sans-serif;max-width:1100px;margin:0 auto;padding:24px 16px;color:#1c1b1e;background:#fff}}
table{{width:100%;border-collapse:collapse;margin-top:10px}}th{{text-align:left;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:#8a8083;padding:6px 10px}}
td{{vertical-align:top;padding:12px 10px;border-top:1px solid #eee;font-size:15.5px;line-height:1.55;width:50%}}td:first-child{{color:#8a8083}}td:last-child{{background:#f4eae5}}
@media(max-width:700px){{tr{{display:block;border-top:1px solid #ddd}}th{{display:none}}td{{display:block;width:auto;border:0}}}}</style></head>
<body><h1>Mentions légales : compléments du 27/10/2026</h1><p>Version française (l'anglais suit le même contenu). Rien n'est en ligne avant l'accord de Jay.</p>
<table><tr><th>Avant</th><th>Après</th></tr>{rangs}</table></body></html>""", encoding="utf-8")
    print(f"legal.html complétée ({len(lignes)} changements), comparaison : {COMPARAISON}")


if __name__ == "__main__":
    main()
