"""
Statistiques de visite : Cloudflare Web Analytics (gratuit, sans cookie), installé le 27/10/2026.
Ajoute le petit code de Cloudflare avant </body> dans les 9 pages, puis complète les mentions légales
(cookies et transferts hors UE). Le « token » n'est pas un secret : c'est un identifiant public,
visible dans le code de tout site qui utilise Cloudflare.

    python3 site-unseen/outils/ajouter_cloudflare.py
"""
import html
import re
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from legal_v3 import p, paragraphe  # noqa: E402

TOKEN = "e276d22355ad4ef6a0ed2be285d84a83"
PAGES = ["index.html", "professionals.html", "paris.html", "riviera.html", "ocean-indien.html",
         "saison-ski-2026-2027.html", "formule-1.html", "legal.html", "404.html"]
CODE = ("<!-- Cloudflare Web Analytics --><script defer src='https://static.cloudflareinsights.com/beacon.min.js' "
        f"data-cf-beacon='{{\"token\": \"{TOKEN}\"}}'></script><!-- End Cloudflare Web Analytics -->\n")

COOKIES = ("This site sets no cookies, whether for advertising or analytics. Its fonts are served from the site itself, with no call to a third-party service. "
           "Visits are counted with Cloudflare Web Analytics, a tool that sets no cookie, does not follow visitors from one site to another and builds no individual profile. "
           "Your language choice is stored locally in your browser and is never transmitted to us. "
           "As with any website, the host records technical connection data, such as the IP address, to deliver the pages and protect the service.",
           "Ce site ne dépose aucun cookie, qu'il soit publicitaire ou de mesure d'audience. Ses polices de caractères sont hébergées sur le site lui-même, sans appel à un service tiers. "
           "Les visites sont comptées avec Cloudflare Web Analytics, un outil qui ne dépose aucun cookie, ne suit pas les visiteurs d'un site à l'autre et ne constitue aucun profil individuel. "
           "Votre choix de langue est enregistré localement dans votre navigateur et ne nous est jamais transmis. "
           "Comme pour tout site, l'hébergeur enregistre des données techniques de connexion, comme l'adresse IP, pour afficher les pages et protéger le service.")
TRANSFERTS = ("Some of our technical providers are based outside the European Union: the hosting of this site (GitHub, United States), audience measurement (Cloudflare, United States), "
              "email (Google) and messaging services such as WhatsApp (Meta). These transfers are covered by the safeguards provided for by the GDPR, in particular the European Commission's "
              "adequacy decision on the EU-US Data Privacy Framework and standard contractual clauses.",
              "Certains de nos prestataires techniques sont établis hors de l'Union européenne : l'hébergement de ce site (GitHub, États-Unis), la mesure d'audience (Cloudflare, États-Unis), "
              "la messagerie électronique (Google) et des messageries comme WhatsApp (Meta). Ces transferts sont encadrés par les garanties prévues par le RGPD, notamment la décision d'adéquation "
              "de la Commission européenne relative au cadre de protection des données UE-États-Unis et les clauses contractuelles types.")


def main():
    for nom in PAGES:
        chemin = SITE / nom
        t = chemin.read_text(encoding="utf-8")
        if "Cloudflare Web Analytics -->" not in t:
            i = t.rindex("</body>")
            t = t[:i] + CODE + t[i:]
        if nom == "legal.html":
            for debut, (en, fr) in (("This site sets no cookies", COOKIES), ("Some of our technical providers", TRANSFERTS)):
                d, f = paragraphe(t, debut)
                t = t[:d] + p(en, fr) + t[f:]
        chemin.write_text(t, encoding="utf-8")
        print(nom, "ok")


if __name__ == "__main__":
    main()
